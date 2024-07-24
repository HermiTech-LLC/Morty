# Project Skeleton Framework: Booting OS from Local NAS on Dev Board

## Project Overview
The objective is to boot an operating system (OS) from a local NAS using FUSE in the initramfs. This involves building a custom initramfs with network support and necessary binaries, leveraging Yocto for creating custom Linux distributions. The goal is to develop a robust, scalable, and maintainable solution suitable for various environments.

## 1. Setup and Prerequisites

### 1.1 Tools and Dependencies
- **Dracut** (or an equivalent initramfs tool)
- **Docker** (or any container runtime)
- **A compatible Linux distribution** (e.g., Arch Linux)
- **Local NAS setup** with accessible file share
- **FUSE and related tools**
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

### 3.2 Module Script for FUSE
Create a module script in `modules.d/90fuse/module-setup.sh`:
```bash
#!/bin/bash
check() {
    require_binaries fusermount fuseiso mkisofs || return 1
    return 0
}
depends() {
    return 0
}
install() {
    inst_multiple fusermount fuseiso mkisofs
    return 0
}
```

### 3.3 Building EFI Image
```bash
./dracut.sh --kver <kernel-version> --uefi efi_firmware/EFI/BOOT/BOOTX64.efi --force -l -N --no-hostonly-cmdline --modules "base bash fuse shutdown network" --add-drivers "target_core_mod target_core_file e1000" --kernel-cmdline "ip=dhcp rd.shell=1 console=ttyS0"
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

### 4.3 Adding FUSE Support in Yocto
- Create a new layer for custom recipes:
  ```bash
  bitbake-layers create-layer meta-custom
  bitbake-layers add-layer meta-custom
  ```

- Add a recipe for FUSE in `meta-custom/recipes-support/fuse/fuse_2.9.7.bb`:
  ```bash
  SUMMARY = "Filesystem in Userspace"
  DESCRIPTION = "FUSE (Filesystem in Userspace) is a simple interface for userspace programs to export a virtual filesystem to the Linux kernel."
  LICENSE = "LGPLv2.1"
  SRC_URI = "https://github.com/libfuse/libfuse/releases/download/fuse-2.9.7/fuse-2.9.7.tar.gz"
  
  inherit autotools
  ```

### 4.4 Building Yocto Image with FUSE Support
- Build the custom image with FUSE support:
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
  cp /path/to/yocto/build/tmp/deploy/images/qemux86-64/fuse-binary /path/to/initramfs/usr/bin/
  ```

## 5. Debugging and Adjustments

### 5.1 Networking and Drivers
Configure the network and load necessary drivers:
```bash
modprobe fuse
modprobe e1000
ip link set lo up
ip link set eth0 up
dhclient eth0
ip route add default via <gateway-ip> dev eth0 proto dhcp src <local-ip>
```

### 5.2 Mounting NAS Filesystem
Mount the NAS filesystem using FUSE:
```bash
fuseiso -o url=<nas-url> -o use_path_request_style fuse /sysroot
ls /sysroot
switch_root /sysroot /sbin/init
```

## 6. Resolving Issues

### 6.1 Chroot Method
Modify initramfs's init script to use `chroot`:
```bash
modprobe fuse
modprobe e1000
ip link set lo up
ip link set eth0 up
dhclient eth0
ip route add default via <gateway-ip> dev eth0 proto dhcp src <local-ip>
fuseiso -o url=<nas-url> -o use_path_request_style fuse /sysroot
mount --rbind /sys /sysroot/sys
mount --rbind /dev /sysroot/dev
mount -t proc /proc /sysroot/proc
exec chroot /sysroot /sbin/init
```

## 7. Finalizing and Deployment

### 7.1 Boot from NAS Storage
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

## 9. Additional Considerations

### 9.1 Further Adaptations
- Explore booting from other local storage services (e.g., SSHFS, NFS).
- Implement project-specific changes and optimizations.

### 9.2 Commercialization Potential
Consider adapting the framework for enterprise solutions, focusing on local NAS-based computing and cloud-native environments.

---

This structured plan provides a comprehensive guide for booting an operating system from a local NAS using a development board. It leverages Dracut and Yocto to create a custom initramfs and OS image, ensuring flexibility and scalability for various deployment scenarios.