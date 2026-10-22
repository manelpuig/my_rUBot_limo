# Traspàs de context: LIMO real amb Foxy i PCs Humble

## Objectiu

Aquest document conserva el context necessari per continuar la revisió i la
millora de `my_rUBot_limo` des d'un altre ordinador o una conversa nova de
Codex.

L'objectiu és deixar un repositori reproduïble, segur i funcional per al robot
real, sense trencar el bringup que actualment funciona a la Jetson Nano. Els
canvis s'han de fer de manera incremental i validar primer al worktree de
refactorització.

## Estat de Git

- Repositori original: `my_rUBot_limo`
- Branca protegida de treball habitual: `main`
- Worktree de refactorització: `my_rUBot_limo-refactor`
- Branca de refactorització: `refactor/real-limo-bringup-humble`
- Commit de partida de les dues branques: `ebd8856f4b89ccd1daac121e8c5d6ee4f8b1e7e4`
- Missatge del commit de partida: `limo base rf2o`

No s'han de fer canvis directament a `main`. Tota la feina d'aquesta revisió
s'ha de fer a la branca i al worktree de refactorització. En el moment de crear
aquest document, no s'havia publicat la branca nova al remot.

## Plataforma real declarada pel propietari

- Robot AgileX LIMO sense braç.
- Ordinador embarcat: NVIDIA Jetson Nano.
- Sistema operatiu declarat: Ubuntu 22.04 natiu.
- ROS 2 instal·lat a la Jetson: Foxy.
- Base configurada amb cinemàtica Mecanum per defecte.
- LiDAR: YDLidar.
- Càmera RGB-D: Orbbec DaBai.
- El bringup actual executat a la Jetson funciona correctament.
- PCs de control: Ubuntu 22.04 amb ROS 2 Humble natiu.
- Robot i PCs comparteixen la mateixa xarxa de laboratori.

### Punt que cal confirmar abans de canviar el bringup

ROS 2 Foxy es va distribuir oficialment per Ubuntu 20.04. La combinació
declarada Ubuntu 22.04 + Foxy pot correspondre a una compilació des de fonts,
un contenidor o una identificació inexacta de la versió del sistema. Com que el
bringup funciona, no s'ha de migrar ni substituir res fins que s'hagi capturat
la configuració real.

També cal comprovar si la comunicació Foxy-Humble ja funciona de manera estable,
quin RMW/DDS utilitza cada ordinador i si tots dos tenen el mateix
`ROS_DOMAIN_ID`.

## Inventari rellevant del repositori

### Nucli del robot

- `limo_base`: comunicació amb la base mòbil i publicació de l'odometria.
- `limo_msgs`: missatges específics del LIMO.
- `limo_description`: URDF, meshes i descripció del robot.
- `limo_bringup`: launch files que agrupen la base i els sensors.

### Sensors

- `YDLidar-SDK`: SDK natiu del LiDAR.
- `ydlidar_ros2_driver`: driver ROS 2 del YDLidar.
- `OrbbecSDK_ROS2/orbbec_camera`: driver de la càmera Orbbec, versió 1.5.12.
- `OrbbecSDK_ROS2/orbbec_camera_msgs`: missatges del driver Orbbec.
- `OrbbecSDK_ROS2/orbbec_description`: descripció de la càmera.

La branca 1.x del driver Orbbec s'ha de conservar inicialment perquè la DaBai
és una càmera de generació anterior. No s'ha d'actualitzar automàticament a la
branca 2.x sense verificar abans la compatibilitat exacta del dispositiu.

### Odometria i localització opcionals

- `rf2o_laser_odometry`: odometria a partir del LiDAR.
- `csm`: paquet present al repositori però aparentment no integrat en el
  bringup actual.

### Simulació i aplicacions

- `limo_car`: simulació i recursos associats; no hauria de ser una dependència
  obligatòria del bringup del robot real.
- `limo_visions`: exemples o aplicacions de visió.
- `yolov5_ros2`: integració de YOLOv5 i pesos del model.

## Resultat de la revisió inicial

El repositori correspon parcialment a l'ecosistema oficial d'AgileX, però
barreja codi de diferents distribucions ROS, simulació, drivers de tercers,
aplicacions docents i configuració Docker. En l'estat actual no és completament
reproduïble des d'una instal·lació neta.

### Bringup i TF

- `limo_bringup/launch/humble/limo_start.launch.py` arrenca conjuntament la
  base, RF2O, YDLidar i Orbbec. El nou disseny ha de permetre activar cada bloc
  per separat.
- La base pot publicar `odom -> base_link` mentre RF2O també intenta publicar
  aquesta transformació. Només hi ha d'haver una autoritat per cada TF.
- El launch del YDLidar publica `base_link -> laser_link` amb una alçada i el
  launch general en publica una altra amb una alçada diferent. Cal conservar
  una sola transformació, definida a la descripció del robot o en un únic
  publicador estàtic.
- El launch de bringup consulta `limo_car` encara que no utilitza el resultat;
  el bringup real no ha de dependre del paquet de simulació.
- L'argument `pub_tf` està definit però no s'utilitza de manera coherent.

### Base i cinemàtica

- `limo_base/launch/limo_base.launch.py` conté millores locals respecte del
  launch original, però fixa el port `ttyTHS0` i passa `use_mcnamu=True`.
- El codi del driver deixa de seguir el mode notificat per la base quan
  `use_mcnamu` és cert. Per a aquest robot, Mecanum ha de continuar sent el
  valor per defecte, però ha de ser un paràmetre explícit i documentat.
- Cal confirmar el port real i preferir un àlies `udev` estable, per exemple
  `/dev/ttylimo`, en lloc de dependre del nom assignat durant cada arrencada.

### Dependències declarades

S'han detectat dependències utilitzades pel build o en execució que no estan
declarades completament als manifests:

- `limo_base`: `sensor_msgs` i `tf2_geometry_msgs`.
- `limo_visions`: `sensor_msgs` i `image_transport`.
- `rf2o_laser_odometry`: `nav_msgs`.
- `ydlidar_ros2_driver`: `rmw` i la dependència efectiva del YDLidar SDK.
- `limo_bringup`: dependències d'execució dels paquets que inclou als launch.
- `yolov5_ros2`: dependències Python com PyTorch i OpenCV no reproduïdes per
  les instruccions generals d'instal·lació.

### Docker i DDS

- El `docker-compose.yaml` revisat acaba amb `sleep infinity`; aixecar el
  contenidor no arrenca automàticament els nodes del robot.
- `ROS_AUTOMATIC_DISCOVERY_RANGE=OFF` entra en conflicte amb l'objectiu de
  descobrir altres ordinadors.
- La configuració CycloneDDS desactiva multicast però no defineix peers
  estàtics, cosa que pot impedir el descobriment.
- Les imatges `latest` amb `pull_policy: always` no són reproduïbles.
- `privileged`, xarxa de host i X11 donen més accés del necessari per a un
  bringup de producció.

La plataforma real és nativa, no Docker. Per tant, Docker s'ha de considerar
una eina opcional de build o desenvolupament i no la font principal de la
configuració del robot.

### Documentació, seguretat i mida

- La documentació barreja ROS 1 (`rosrun`, `rostopic`), Foxy, Humble,
  simulació i robot real.
- El README principal no documenta un procediment complet de bringup real.
- `src/limo_ros2/setup.sh` habilita SSH insegur, contrasenya de root coneguda i
  `PermitEmptyPasswords`. No s'ha d'utilitzar al robot; cal eliminar-lo o
  traslladar-lo a una zona històrica clarament marcada.
- `.gitignore` conté accidentalment línies d'un script de shell/heredoc.
- Hi ha arxius grans o duplicats: `limo_pi.zip`, meshes repetits, binaris
  Orbbec per diverses arquitectures i pesos de YOLO.

## Decisions de disseny acordades

1. Preservar com a baseline el bringup Foxy que ja funciona a la Jetson.
2. Separar clarament el rol del robot Foxy del rol dels PCs Humble.
3. Mantenir Mecanum com a cinemàtica predeterminada, però configurable.
4. No fer que la simulació, RF2O, Orbbec o les aplicacions de visió siguin
   dependències obligatòries del bringup mínim de la base.
5. Tenir una única autoritat per cada transformació TF.
6. Fer canvis petits, revisables i amb un commit independent per bloc.
7. No fusionar a `main` fins que les proves al robot real siguin satisfactòries.

## Informació pendent de capturar a la Jetson

Executar i conservar la sortida de:

```bash
lsb_release -a
uname -a
head -n 1 /etc/nv_tegra_release 2>/dev/null
printenv ROS_DISTRO
printenv RMW_IMPLEMENTATION
printenv ROS_DOMAIN_ID
ros2 doctor --report
ros2 pkg list | sort
```

També cal registrar:

- Ordre exacta que arrenca el bringup funcional.
- Workspaces dels quals es fa `source` i el seu ordre.
- Ports reals de la base, YDLidar i Orbbec.
- Regles `udev` existents.
- Nodes, topics i transforms TF quan el sistema està funcionant.
- Paràmetres efectius de `limo_base`, YDLidar i Orbbec.
- RMW/DDS i `ROS_DOMAIN_ID` de la Jetson i del PC Humble.
- Si els topics són visibles en les dues direccions entre Foxy i Humble.

## Pla de treball proposat

Cada fase ha de quedar en un commit separat i no ha de començar fins que
l'anterior s'hagi verificat.

1. **Baseline funcional**
   - Capturar les dades pendents de la Jetson.
   - Documentar l'ordre de bringup actual i els topics esperats.
   - Crear una prova manual curta que permeti decidir si el comportament s'ha
     conservat.
2. **Manifests i build**
   - Corregir dependències ROS declarades sense canviar comportament.
   - Validar `rosdep`, `colcon build` i `colcon test` en entorns nets per Foxy
     i Humble quan sigui aplicable.
3. **Bringup mínim de la base**
   - Fer explícits el port, la cinemàtica i la publicació de TF.
   - Mantenir Mecanum per defecte.
4. **YDLidar i arbre TF**
   - Fer el LiDAR opcional.
   - Eliminar la transformació duplicada de `laser_link`.
   - Verificar freqüència, orientació i timestamps del `LaserScan`.
5. **Orbbec DaBai**
   - Fer la càmera opcional i mantenir el driver compatible actual.
   - Verificar serial, topics, resolució, FPS i alineació de profunditat.
6. **RF2O i localització**
   - Desactivar RF2O per defecte.
   - Definir clarament qui publica `odom -> base_link` quan s'activa.
7. **PC Humble i DDS**
   - Documentar el procediment de control i RViz des del PC.
   - Provar descobriment, QoS i compatibilitat dels missatges Foxy-Humble.
8. **Neteja i documentació**
   - Separar robot real, simulació i aplicacions opcionals.
   - Corregir `.gitignore` i retirar scripts insegurs.
   - Decidir què fer amb binaris, pesos i assets grans o duplicats.
   - Reescriure el README i les guies amb instruccions diferenciades.

## Criteris de validació final

- La Jetson arrenca la base Mecanum sense errors després d'una arrencada neta.
- El robot es pot controlar a baixa velocitat amb les rodes elevades abans de
  provar-lo a terra.
- Base, LiDAR i càmera es poden arrencar i aturar independentment.
- No existeixen publicadors TF duplicats.
- Els frames, timestamps i freqüències són coherents.
- El PC Humble descobreix els nodes i topics necessaris de la Jetson Foxy.
- RViz mostra correctament robot, LiDAR, càmera i odometria.
- La connexió es recupera després de reiniciar el robot i de reconnectar USB.
- Una instal·lació neta pot resoldre dependències i compilar seguint només la
  documentació del repositori.
- `main` continua intacta fins a completar les proves de maquinari.

## Referències oficials consultades

- AgileX LIMO ROS 2 Humble:
  <https://github.com/agilexrobotics/limo_ros2/tree/humble>
- Manual LIMO Pro ROS 2 Foxy:
  <https://github.com/agilexrobotics/limo_pro_doc/blob/master/Limo%20Pro%20Ros2%20Foxy%20user%20manual(EN).md>
- Driver ROS 2 de YDLidar:
  <https://github.com/YDLIDAR/ydlidar_ros2_driver>
- Driver ROS 2 d'Orbbec:
  <https://github.com/orbbec/OrbbecSDK_ROS2>
- Descobriment dinàmic de ROS 2:
  <https://github.com/ros2/ros2_documentation/blob/rolling/source/Developer-Tools/Introspection-and-analysis/Improved-Dynamic-Discovery.rst>
- Configuració de CycloneDDS:
  <https://cyclonedds.io/docs/cyclonedds/latest/config/runtime_config.html>

## Instrucció per reprendre la feina amb Codex

Obrir el repositori al worktree de la branca de refactorització i indicar:

> Continua la revisió del LIMO utilitzant
> `Documentation/CODEX_HANDOFF.md` com a context principal. Conserva el
> bringup Foxy funcional, no modifiquis `main` i valida cada fase abans de
> continuar.

