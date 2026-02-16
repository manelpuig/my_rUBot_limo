FROM ros:humble-ros-base

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive

# -----------------------------
# 1) System deps + ROS tools
# -----------------------------
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      ca-certificates curl gnupg \
      build-essential cmake git unzip pkg-config \
      python3-pip python3-rosdep python3-colcon-common-extensions python3-serial \
      iputils-ping net-tools \
      \
      # X11 / OpenGL (RViz/RQt)
      x11-apps libgl1-mesa-glx libgl1-mesa-dri libglu1-mesa mesa-utils \
      libqt5x11extras5 libxkbcommon-x11-0 libx11-6 libxext6 libxrender1 libxtst6 \
      \
      # USB / udev / video (important for cameras)
      libusb-1.0-0 libusb-1.0-0-dev libudev-dev udev usbutils v4l-utils \
      \
      # OpenCV dev (often needed by camera drivers)
      libopencv-dev \
      \
      # ROS middleware + tools (your original set)
      ros-humble-rmw-cyclonedds-cpp \
      ros-humble-rviz2 \
      ros-humble-joint-state-publisher \
      ros-humble-tf-transformations \
      ros-humble-teleop-twist-keyboard \
      ros-humble-rosbridge-server \
      ros-humble-image-transport \
      ros-humble-image-transport-plugins \
      ros-humble-compressed-image-transport \
      ros-humble-rqt \
      ros-humble-rqt-image-view \
      ros-humble-rqt-common-plugins \
      ros-humble-tf2-eigen \
      ros-humble-turtlesim \
      ros-humble-diagnostic-updater \
      ros-humble-backward-ros \
      nlohmann-json3-dev \
      \
      # --- add-ons to fix your rosdep/apt failures ---
      ros-humble-xacro \
      ros-humble-joint-state-publisher-gui \
      ros-humble-rqt-robot-steering \
      ros-humble-vision-msgs \
      ros-humble-image-publisher \
      ros-humble-camera-info-manager \
      \
      # Nav2 + Cartographer (remove if not needed)
      ros-humble-nav2-bringup \
      ros-humble-cartographer \
      ros-humble-cartographer-ros \
      \
      # System deps that rosdep couldn't locate
      libgflags-dev \
      libgoogle-glog-dev \
    ; \
    rm -rf /var/lib/apt/lists/*

# -----------------------------
# 2) rosdep init/update (safe)
# -----------------------------
RUN set -eux; \
    if [ ! -f /etc/ros/rosdep/sources.list.d/20-default.list ]; then \
      rosdep init; \
    fi; \
    rosdep update

# -----------------------------
# 3) Copy workspace zip + unpack
#    limo_pi.zip must contain a folder "limo_pi/" with "src/" inside
# -----------------------------
WORKDIR /root
COPY limo_pi.zip /root/limo_pi.zip

RUN set -eux; \
    unzip -q /root/limo_pi.zip -d /root; \
    rm -f /root/limo_pi.zip; \
    test -d /root/limo_pi/src

# -----------------------------
# 3b) Clone OrbbecSDK_ROS2 into the workspace (needed for libOrbbecSDK)
# -----------------------------
RUN set -eux; \
    cd /root/limo_pi/src; \
    if [ ! -d OrbbecSDK_ROS2 ]; then \
      git clone --branch main https://github.com/orbbec/OrbbecSDK_ROS2.git; \
    fi

# -----------------------------
# 4) Optional: Build & install YDLidar-SDK (if present)
# -----------------------------
RUN set -eux; \
    if [ -d /root/limo_pi/src/YDLidar-SDK ]; then \
      cd /root/limo_pi/src/YDLidar-SDK; \
      rm -rf build; mkdir -p build; cd build; \
      cmake .. -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=/usr/local; \
      make -j"$(nproc)"; \
      make install; \
      ldconfig; \
    else \
      echo "YDLidar-SDK not found in workspace, skipping."; \
    fi

# -----------------------------
# 5) rosdep install + colcon build
# -----------------------------
RUN set -eux; \
    set +u; source /opt/ros/humble/setup.bash; set -u; \
    cd /root/limo_pi; \
    rosdep update; \
    rosdep install --from-paths src --ignore-src -r -y \
      --skip-keys "libgazebo_ros gazebo rviz yolov5 cmake_modules nav2_recoveries"; \
    rm -rf build install log; \
    colcon build --symlink-install --packages-skip limo_car; \
    ldconfig; \
    rm -rf /root/.ros/log || true

# -----------------------------
# 6) Environment setup (.bashrc)
# -----------------------------
RUN set -eux; \
    echo 'set +u; source /opt/ros/humble/setup.bash; set -u' >> /root/.bashrc; \
    echo 'source /root/limo_pi/install/setup.bash' >> /root/.bashrc; \
    echo 'cd /root/limo_pi' >> /root/.bashrc

CMD ["/bin/bash"]
