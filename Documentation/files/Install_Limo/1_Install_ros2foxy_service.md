# Automatic LIMO Pro bringup service

This guide creates one `systemd` service that starts the LIMO Pro bringup when
the robot boots.

Expected configuration:

- User: `agilex`
- Workspace: `/home/agilex/limo_refactor_ws`
- Ubuntu 20.04 with ROS 2 Foxy
- Mecanum base, YDLidar and Orbbec DaBai
- `ROS_DOMAIN_ID=10`

## 1. Test the bringup manually

Do not enable the service until the normal bringup works:

```bash
source /opt/ros/foxy/setup.bash
source /home/agilex/limo_refactor_ws/install/setup.bash
ros2 launch limo_bringup limo_robot_bringup.launch.py
```

Stop it with `Ctrl+C` after checking the base and sensors.

## 2. Install the service files

```bash
cd /home/agilex/limo_refactor_ws/Documentation/files/Install_Limo

sudo install -m 0755 start_limo_bringup.sh \
  /usr/local/bin/start_limo_bringup

sudo install -m 0644 limo-bringup.env \
  /etc/default/limo-bringup

sudo install -m 0644 limo-bringup.service \
  /etc/systemd/system/limo-bringup.service
```

Edit the configuration if the workspace, ports or ROS domain are different:

```bash
sudo nano /etc/default/limo-bringup
```

The robot and control PC must use the same `ROS_DOMAIN_ID`.

## 3. Test the start script

```bash
sudo -u agilex \
  bash -c 'set -a; source /etc/default/limo-bringup; set +a; exec /usr/local/bin/start_limo_bringup'
```

In another robot terminal, check:

```bash
source /opt/ros/foxy/setup.bash
source /home/agilex/limo_refactor_ws/install/setup.bash
export ROS_DOMAIN_ID=10

ros2 node list
ros2 topic echo /limo_status
ros2 topic hz /wheel/odom
ros2 topic hz /scan
```

Stop the manual test with `Ctrl+C`.

## 4. Enable automatic startup

```bash
sudo systemctl daemon-reload
sudo systemctl enable --now limo-bringup.service
```

Check the service and logs:

```bash
systemctl status limo-bringup.service --no-pager
journalctl -u limo-bringup.service -f
```

If the complete launcher exits with an error, `systemd` retries after five
seconds.

## 5. Test after reboot

```bash
sudo reboot
```

After reconnecting to the robot:

```bash
systemctl status limo-bringup.service --no-pager
journalctl -u limo-bringup.service -b --no-pager
```

From the Humble control PC, using `ROS_DOMAIN_ID=10`:

```bash
ros2 node list
ros2 topic echo /limo_status
ros2 topic hz /scan
```

## 6. Service commands

```bash
sudo systemctl stop limo-bringup.service
sudo systemctl start limo-bringup.service
sudo systemctl restart limo-bringup.service
sudo systemctl disable --now limo-bringup.service
```

## 7. Update the robot workspace

```bash
sudo systemctl stop limo-bringup.service

cd /home/agilex/limo_refactor_ws
git pull --ff-only
source /opt/ros/foxy/setup.bash
colcon build --symlink-install --packages-up-to limo_bringup

sudo systemctl start limo-bringup.service
systemctl status limo-bringup.service --no-pager
```

If a service file changed, install it again and run:

```bash
sudo systemctl daemon-reload
sudo systemctl restart limo-bringup.service
```

## Common errors

- Missing `install/setup.bash`: build the workspace first.
- Cannot open `ttyTHS0`: check the port, permissions and `dialout` group.
- Missing `/dev/ydlidar`: check the USB connection and `udev` rule.
- Missing DaBai camera: check USB power and Orbbec `udev` rules.
- The PC cannot see ROS topics: check the network and `ROS_DOMAIN_ID`.
