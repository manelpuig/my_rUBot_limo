# LIMO ROS 2 Humble -- Robot + PC Communication Guide

## 1️⃣ On the Robot (ARM) -- Run Docker Compose

### Step 1: Go to the folder containing `docker-compose.yaml`


### Step 2: Verify PC IP inside docker-compose.yaml

Ensure these environment variables are set:

``` yaml
environment:
  - ROS_DOMAIN_ID=1
  - RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
  - ROS_AUTOMATIC_DISCOVERY_RANGE=OFF
  - ROS_STATIC_PEERS=192.168.1.16   # ⚠️ Replace with your PC IP
  - CYCLONEDDS_URI=file:///config/cyclonedds_robot.xml
```

### Step 3: Start the container

If you want GUI on the robot, use:
``` bash
xhost +local:root
```

Then start the container:
``` bash
docker compose up
```

### Step 4: Verify container is running

``` bash
docker ps
```

------------------------------------------------------------------------

## 2️⃣ On the PC (Ubuntu Host) -- Configure Communication

Edit your `.bashrc` and add the following lines at the end:

``` bash
# ROS 2 – LIMO Robot Communication
export ROS_DOMAIN_ID=1
export RMW_IMPLEMENTATION=rmw_cyclonedds_cpp
export ROS_AUTOMATIC_DISCOVERY_RANGE=OFF
export ROS_STATIC_PEERS=192.168.1.14   # ⚠️ Replace with robot IP
```

Save and apply:

``` bash
source ~/.bashrc
```

------------------------------------------------------------------------

## 3️⃣ Test Communication

On the robot (inside container):

``` bash
ros2 topic list
```

On the PC:

``` bash
ros2 topic list
```

If communication works correctly, you should see robot topics from the
PC.

------------------------------------------------------------------------

## 4️⃣ Important Notes

-   Both robot and PC must use the SAME:
    -   ROS_DOMAIN_ID
    -   RMW_IMPLEMENTATION
-   Robot must point to PC IP in ROS_STATIC_PEERS
-   PC must point to Robot IP in ROS_STATIC_PEERS
-   Both machines must be in the same local network

------------------------------------------------------------------------

## 5️⃣ Stop the Robot Container

``` bash
docker compose down
```

------------------------------------------------------------------------

**This setup provides deterministic unicast DDS communication using
CycloneDDS.**
