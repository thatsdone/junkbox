#!/bin/bash
set -x
#
# setup-libvirt-raspios.sh
#
# Define and create an ARM KVM using virt-install (under libvirt management).
#
# Regarding the virtual hardware, roughly speaking, the below is similar to
# Raspberry Pi Zero W.
# kernel and dtb can be downloaded from below.
#   * https://github.com/dhruvvyas90/qemu-rpi-kernel
# image can be downloaded from below (or mirrow).
#   * https://downloads.raspberrypi.org/raspios_lite_armhf/images/
#
# TODO:
#  * use '--wait' or '--noautoconsole'
#  * use bridge network and mac option (for dhcp environment)
#  * Consider disk expansion at installation time.
#  * etc.
#
DIR=YOUR_IMAGE_PATH
IMAGE=${DIR}/2021-01-11-raspios-buster-armhf-lite.img
DTB=${DIR}/versatile-pb-buster.dtb
KERNEL=${DIR}/kernel-qemu-4.19.50-buster

NAME=${NAME:-raspios-kvm1}

ARCH=${ARCH:-arm6l}
CPU=${CPU:-arm1176}
MACHINE=${MACHINE:-versatilepb}
VCPUS=${VCPUS:-1}
MEMORY=${MEMORY:-256}
#NETWORK=${NETWORK:-user}
NETWORK=${NETWORK:-bridge=br0}


virt-install \
    --name ${NAME} \
    --arch ${ARCH} \
    --machine ${MACHINE} \
    --cpu ${CPU} \
    --vcpus ${VCPUS} \
    --memory ${MEMORY} \
    --import \
    --disk ${IMAGE},format=raw,bus=virtio \
    --network user,model=virtio \
    --video vga \
    --graphics vnc \
    --serial pty \
    --rng device=/dev/urandom,model=virtio \
    --boot "dtb=${DTB},kernel=${KERNEL},kernel_args=root=/dev/vda2 panic=1 rootfstype=ext4 rw console=ttyAMA0" \
    --events on_reboot=destroy \
    --noautoconsole

echo Now, you can access to the VM via 'virsh console '${NAME}
