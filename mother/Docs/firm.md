# Project Skeleton Framework: Booting OS from Local NAS using SSHFS on Dev Board

## Project Overview
The objective is to boot an operating system (OS) from a local NAS using SSHFS in the initramfs. This involves building a custom initramfs with network support and necessary binaries, leveraging Yocto for creating custom Linux distributions. The goal is to develop a robust, scalable, and maintainable solution suitable for various environments.

## 1. Setup and Prerequisites

### 1.1 Tools and Dependencies
- **Dracut** (or an equivalent initramfs tool)
- **Docker** (or any container runtime)
- **A compatible Linux distribution** (e.g., Arch Linux)
- **Local NAS setup** with SSH access
- **SSHFS and related tools**
- **Yocto Project** for building custom Linux distributions

### 1.2 Basic Commands
```bash
# Clone Dracut repository
git clone https://github.com/dracutdevs/dracut

# Run an Arch Linux container
podman run -it --name arch -v ./dracut:/dracut docker.io/archlinux:latest bash
```

## 2. Understanding the OS Boot Process

### 2.1 Boot Process Overview
1. Firmware (BIOS/UEFI) loads the bootloader.
2. Bootloader loads the kernel.
3. Kernel unpacks a temporary filesystem (initramfs).
4. Kernel mounts the real filesystem and switches to the init system.

## 3. Custom Initramfs Creation

### 3.1 Building Custom Initramfs
- Install necessary packages and compile Dracut:
  ```bash
  # Inside the container
  pacman -Syu
  pacman -S linux base-devel
  cd /dracut
  make
  ```

### 3.2 Module Script for SSHFS
Create a module script in `modules.d/90sshfs/module-setup.sh`:
```bash
#!/bin/bash
check() {
    require_binaries sshfs || return 1
    return 0
}
depends() {
    return 0
}
install() {
    inst_multiple sshfs
    return 0
}
```

### 3.3 Building EFI Image
```bash
./dracut.sh --kver <kernel-version> --uefi efi_firmware/EFI/BOOT/BOOTX64.efi --force -l -N --no-hostonly-cmdline --modules "base bash sshfs shutdown network" --add-drivers "target_core_mod target_core_file e1000" --kernel-cmdline "ip=dhcp rd.shell=1 console=ttyS0"
```

## 4. Yocto Project Integration

### 4.1 Setting Up Yocto Project
- Clone the Poky repository and set up the environment:
  ```bash
  git clone git://git.yoctoproject.org/poky.git
  cd poky
  source oe-init-build-env
  ```

### 4.2 Configuring Yocto Build
- Edit `conf/local.conf` to customize the build:
  ```bash
  # Example configuration changes
  MACHINE = "qemux86-64"
  DISTRO = "poky"
  ```

### 4.3 Adding SSHFS Support in Yocto
- Create a new layer for custom recipes:
  ```bash
  bitbake-layers create-layer meta-custom
  bitbake-layers add-layer meta-custom
  ```

- Add a recipe for SSHFS in `meta-custom/recipes-support/sshfs/sshfs_3.7.1.bb`:
  ```bash
  SUMMARY = "SSH Filesystem"
  DESCRIPTION = "SSHFS (SSH Filesystem) allows for mounting remote directories over SSH."
  LICENSE = "GPLv2"
  SRC_URI = "https://github.com/libfuse/sshfs/releases/download/sshfs-3.7.1/sshfs-3.7.1.tar.xz"
  
  inherit autotools
  ```

### 4.4 Building Yocto Image with SSHFS Support
- Build the custom image with SSHFS support:
  ```bash
  bitbake core-image-minimal
  ```

### 4.5 Integrating Yocto Build with Initramfs
- Extract the Yocto build output and integrate with initramfs:
  ```bash
  mkdir -p /path/to/initramfs
  cd /path/to/initramfs
  cp /path/to/yocto/build/tmp/deploy/images/qemux86-64/core-image-minimal-qemux86-64.tar.bz2 .
  tar -xjf core-image-minimal-qemux86-64.tar.bz2
  ```

- Ensure necessary binaries are included in the initramfs:
  ```bash
  cp /path/to/yocto/build/tmp/deploy/images/qemux86-64/sshfs-binary /path/to/initramfs/usr/bin/
  ```

## 5. Debugging and Adjustments

### 5.1 Networking and Drivers
Configure the network and load necessary drivers:
```bash
modprobe e1000
ip link set lo up
ip link set eth0 up
dhclient eth0
ip route add default via <gateway-ip> dev eth0 proto dhcp src <local-ip>
```

### 5.2 Mounting NAS Filesystem using SSHFS
Mount the NAS filesystem using SSHFS:
```bash
sshfs user@nas-ip:/path/to/share /sysroot -o allow_other
ls /sysroot
switch_root /sysroot /sbin/init
```

## 6. Resolving Issues

### 6.1 Chroot Method
Modify initramfs's init script to use `chroot`:
```bash
modprobe e1000
ip link set lo up
ip link set eth0 up
dhclient eth0
ip route add default via <gateway-ip> dev eth0 proto dhcp src <local-ip>
sshfs user@nas-ip:/path/to/share /sysroot -o allow_other
mount --rbind /sys /sysroot/sys
mount --rbind /dev /sysroot/dev
mount -t proc /proc /sysroot/proc
exec chroot /sysroot /sbin/init
```

## 7. Finalizing and Deployment

### 7.1 Boot from NAS Storage using SSHFS
Ensure proper symlink handling:
```bash
mkdir /sysroot/sysroot
mount --rbind /sysroot /sysroot/sysroot
```

### 7.2 Adjust Timeouts and Settings
Adjust necessary timeouts and settings:
```bash
# Example systemd configuration
[Unit]
Description=Serial device ttyS0
DefaultDependencies=no
Before=sysinit.target
JobTimeoutSec=infinity

# Login timeout adjustment
echo "LOGIN_TIMEOUT=0" >> /etc/login.defs
```

### 7.3 Deployment on Real Hardware
- Adjust driver settings for the target hardware.
- Modify display settings for compatibility.
- Configure network topology to match the deployment environment.

## 8. Post-Deployment

### 8.1 Utility Installation and Debugging
Install necessary utilities and perform debugging:
```bash
echo "nameserver 1.1.1.1" > /etc/resolv.conf
pacman -Sy <utility>
```

### 8.2 Real Hardware Adjustments
Load additional drivers if needed:
```bash
# Example modprobe for network and input devices
modprobe r8169
modprobe hid_usb
```

## 9. Adaptations and Commercialization

### 9.1 Further Adaptations
- **Booting from Other Storage Services:** Explore booting from other local storage services such as NFS.
- **Security Enhancements:** Implement robust security measures for network communications and NAS access.
  - Use encryption for data in transit and at rest.
  - Configure firewalls and access controls to limit exposure.
  - Regularly update and patch all components to mitigate vulnerabilities.
- **Scalability:** Ensure the solution can scale to accommodate larger networks and more devices.
  - Design the architecture to handle increased load.
  - Use efficient algorithms and data structures to improve performance.
  - Monitor resource usage and optimize as needed.
- **User-Friendly Interfaces:** Develop user-friendly GUIs for configuration and management.
  - Provide clear documentation and support resources.
  - Design intuitive interfaces that simplify complex tasks.
  - Gather user feedback to continuously improve usability.
- **Support and Maintenance:** Provide ongoing support and regular updates to ensure reliability and security.
  - Establish a support team to assist users with issues.
  - Release regular updates to fix bugs and add new features.
  - Implement a system for tracking and addressing user feedback.

### 9.2 Commercialization Potential
Consider adapting the framework for enterprise solutions, focusing on local NAS-based computing and cloud-native environments. This includes:
- **Enhanced Security:** Implement robust security measures for network communications and NAS access.
- **Scalability:** Ensure the solution can scale to accommodate larger networks and more devices.
- **User-Friendly Interfaces:** Develop user-friendly GUIs for configuration and management.
- **Support and Maintenance:** Provide ongoing support and regular updates to ensure reliability and security.

---

This structured plan provides a comprehensive guide for booting an operating system from a local NAS using SSHFS on a development board. It leverages Dracut and Yocto to create a custom initramfs and OS image, ensuring flexibility and scalability for various deployment scenarios. The inclusion of adaptations and commercialization potential ensures the framework is robust and adaptable for both personal and enterprise use.
