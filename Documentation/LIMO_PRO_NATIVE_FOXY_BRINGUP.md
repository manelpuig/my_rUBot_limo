# LIMO Pro: bringup natiu amb ROS 2 Foxy

## Abast

Aquesta guia cobreix el bringup de baix nivell del robot real:

- AgileX LIMO Pro sense braç.
- NVIDIA Jetson Orin Nano, arquitectura AArch64.
- Ubuntu 20.04.6 LTS.
- ROS 2 Foxy natiu, sense Docker.
- Base Mecanum, YDLidar i Orbbec DaBai.

La navegació, SLAM, RViz i les aplicacions s'executaran en un PC de la mateixa
xarxa amb Ubuntu 22.04 i ROS 2 Humble. Aquest flux s'ha de validar per separat.

## Principis del bringup

- `limo_base` publica la interfície pública a `/odom` i conserva
  `/wheel/odom` com a estimació crua de les rodes.
- `limo_base` és l'únic publicador predeterminat de
  `odom -> base_footprint`.
- `robot_state_publisher` publica `base_footprint -> base_link` i els TF fixos
  dels sensors.
- El driver YDLidar és l'únic propietari de `base_link -> laser_link`.
- RF2O està desactivat per defecte. Quan s'activa, publica `/rf2o/odom` però no TF.
- El TF de muntatge de la càmera queda desactivat fins que es mesuri l'extrínseca.

## Dades que encara s'han de confirmar

- Model exacte del YDLidar.
- Port efectiu de la base després d'una arrencada neta.
- Posició i orientació mesurades del LiDAR respecte de `base_link`.
- Posició i orientació mesurades de la DaBai respecte de `base_link`.
- Ordre exacte dels workspaces dels quals es fa `source` al robot funcional.

El valor predeterminat `laser_z:=0.02` conserva el valor del launcher del driver
que ja existia. No s'ha de considerar una calibració del muntatge real.

## Preparació

En una shell nova:

```bash
source /opt/ros/foxy/setup.bash
cd ~/agilex_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install
source install/setup.bash
```

El YDLidar SDK s'ha d'instal·lar abans de compilar `ydlidar_ros2_driver`. El seu
`CMakeLists.txt` requereix que CMake pugui trobar `ydlidar_sdk`.

## Comprovació prèvia

```bash
bash scripts/limo_preflight.sh
```

Es poden comprovar ports alternatius sense modificar fitxers:

```bash
LIMO_BASE_DEVICE=/dev/ttylimo \
LIMO_LIDAR_DEVICE=/dev/ydlidar \
bash scripts/limo_preflight.sh
```

L'script només inspecciona el sistema; no instal·la paquets ni canvia permisos.

## Arrencada incremental

Primer, amb el robot elevat i les rodes sense contacte amb el terra, arrencar
només la base:

```bash
ros2 launch limo_bringup limo_robot_base.launch.py
```

Comprovar:

```bash
ros2 topic list
ros2 topic echo /limo_status
ros2 topic hz /odom
ros2 topic hz /wheel/odom
ros2 topic hz /imu
```

Arrencar només el LiDAR:

```bash
ros2 launch limo_bringup limo_robot_lidar.launch.py
ros2 topic hz /scan
```

Arrencar només la càmera:

```bash
ros2 launch limo_bringup limo_robot_camera.launch.py
```

Finalment, arrencar base i sensors:

```bash
ros2 launch limo_bringup limo_robot_bringup.launch.py
```

Opcions habituals:

```bash
ros2 launch limo_bringup limo_robot_bringup.launch.py \
  base_port:=ttyTHS0 \
  use_lidar:=true \
  use_camera:=true \
  use_rf2o:=false
```

Per reduir càrrega USB, CPU o xarxa:

```bash
ros2 launch limo_bringup limo_robot_bringup.launch.py \
  enable_point_cloud:=false
```

## RF2O opcional

RF2O estima odometria comparant escanejos 2D consecutius. No forma part del
bringup mínim. Per provar-lo sense crear un segon propietari de TF:

```bash
ros2 launch limo_bringup limo_robot_bringup.launch.py use_rf2o:=true
ros2 topic echo /rf2o/odom
```

La fusió de `/wheel/odom`, `/imu` i `/rf2o/odom` queda fora d'aquesta primera
versió.

## Validació de TF

Amb el bringup complet:

```bash
ros2 run tf2_tools view_frames
ros2 run tf2_ros tf2_echo odom base_footprint
ros2 run tf2_ros tf2_echo base_footprint base_link
ros2 run tf2_ros tf2_echo base_link laser_link
```

Hi ha d'haver una sola autoritat per transformació. No s'ha d'activar el TF de
muntatge de la càmera fins que s'hagin mesurat els sis valors de l'extrínseca.

## Comunicació amb el PC Humble

Robot i PC han d'utilitzar el mateix `ROS_DOMAIN_ID` i una configuració DDS
compatible. Primer s'ha de validar el descobriment amb topics petits
(`/limo_status`, `/odom`, `/scan`) abans de transmetre imatges o núvols de
punts. La interoperabilitat Foxy-Humble s'ha de provar a la xarxa real del
laboratori; no s'assumeix com a validada només perquè els nodes arrenquin.
