FROM manelpuig/ros2-humble-ub-limo-base:theconstructai

SHELL ["/bin/bash", "-c"]
ENV DEBIAN_FRONTEND=noninteractive

# ------------------------------------------------------------
# Fix ROS2 apt source "Signed-By" conflicts in base image
# ------------------------------------------------------------
RUN set -eux; \
    apt-get update || true; \
    apt-get install -y --no-install-recommends ca-certificates curl gnupg; \
    rm -rf /var/lib/apt/lists/*; \
    \
    find /etc/apt/sources.list.d -maxdepth 1 -type f \
      \( -name "*ros2*.list" -o -name "*ros*.list" \) \
      -print -exec mv -f {} {}.disabled \; || true; \
    \
    mkdir -p /etc/apt/keyrings; \
    curl -fsSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key \
      | gpg --dearmor -o /etc/apt/keyrings/ros-archive-keyring.gpg; \
    chmod 644 /etc/apt/keyrings/ros-archive-keyring.gpg; \
    \
    . /etc/os-release; \
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu ${UBUNTU_CODENAME} main" \
      > /etc/apt/sources.list.d/ros2.list; \
    apt-get update; \
    rm -rf /var/lib/apt/lists/*

# -----------------------------
# 1) Deps
# -----------------------------
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      x11-apps libgl1-mesa-glx libgl1-mesa-dri libglu1-mesa mesa-utils \
      libqt5x11extras5 libxkbcommon-x11-0 libx11-6 libxext6 libxrender1 libxtst6 \
      \
      libusb-1.0-0 libusb-1.0-0-dev libudev-dev udev usbutils v4l-utils \
      \
      build-essential cmake git unzip iputils-ping net-tools \
      python3-pip python3-rosdep python3-colcon-common-extensions python3-serial \
      \
      ros-humble-rmw-cyclonedds-cpp \
      ros-humble-rviz2 \
      ros-humble-joint-state-publisher \
      ros-humble-tf-transformations \
      ros-humble-teleop-twist-keyboard \
      ros-humble-rosbridge-server \
      \
      ros-humble-image-transport \
      ros-humble-image-transport-plugins \
      ros-humble-compressed-image-transport \
      \
      ros-humble-rqt \
      ros-humble-rqt-image-view \
      ros-humble-rqt-common-plugins \
      \
      ros-humble-tf2-eigen \
      ros-humble-turtlesim \
      ros-humble-diagnostic-updater \
      ros-humble-backward-ros \
      nlohmann-json3-dev \
    ; \
    rm -rf /var/lib/apt/lists/*

# -----------------------------
# Patch custom launch files (source tree)
# -----------------------------
RUN test -d /root/agilex_ws/src/limo_ros2/limo_base/launch
RUN test -d /root/agilex_ws/src/limo_ros2/limo_bringup/launch/humble

COPY ./limo_base.launch.py \
  /root/agilex_ws/src/limo_ros2/limo_base/launch/limo_base.launch.py

COPY ./limo_start.launch.py \
  /root/agilex_ws/src/limo_ros2/limo_bringup/launch/humble/limo_start.launch.py

# -----------------------------
# 3) Ignore astra package
# -----------------------------
RUN set -eux; \
    if [ -d /root/agilex_ws/src/ros2_astra_camera ]; then \
      touch /root/agilex_ws/src/ros2_astra_camera/COLCON_IGNORE; \
    fi

# -----------------------------
# 4) Build + install YDLidar-SDK to /usr/local
# -----------------------------
RUN set -eux; \
    cd /root/agilex_ws/src/YDLidar-SDK; \
    rm -rf build; \
    mkdir -p build; \
    cd build; \
    cmake .. -DCMAKE_BUILD_TYPE=Release -DBUILD_SHARED_LIBS=ON -DCMAKE_INSTALL_PREFIX=/usr/local; \
    make -j"$(nproc)"; \
    make install; \
    ldconfig

# -----------------------------
# 5) Build ROS2 workspace
# -----------------------------
RUN set -eux; \
    source /opt/ros/humble/setup.bash; \
    cd /root/agilex_ws; \
    rm -rf build install log; \
    colcon build --symlink-install; \
    rm -rf /root/.ros/log || true

# -----------------------------
# Environment setup (.bashrc)
# -----------------------------
RUN echo "source /opt/ros/humble/setup.bash" >> /root/.bashrc && \
    echo "source /root/agilex_ws/install/setup.bash" >> /root/.bashrc && \
    echo "cd /root/agilex_ws" >> /root/.bashrc

CMD ["/bin/bash"]
