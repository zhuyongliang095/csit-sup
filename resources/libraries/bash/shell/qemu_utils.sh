#!/bin/bash
# Copyright (c) 2018 Cisco and/or its affiliates.
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at:
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

function qemu_utils.qemu_delete {
    # Deletes the QEMU directory
    # QEMU install directory
    qemu_install_dir=$1
    # QEMU install version
    qemu_install_ver=$2

    [ -d ${qemu_install_dir}/${qemu_install_ver} ] && \
        sudo rm -r ${qemu_install_dir}/${qemu_install_ver} && \
        echo "${qemu_install_dir}/${qemu_install_ver} removed"
}

function qemu_utils.qemu_install {
    # Downloads and installs QEMU
    # QEMU install directory
    qemu_install_dir=$1
    # QEMU install version
    qemu_install_ver=$2
    # QEMU patch
    qemu_patch=$3
    # Force install (if true then remove previous installation; default false)
    force_install=${4:-false}
    # QEMU repo URL
    qemu_package_url="http://download.qemu-project.org/${qemu_install_ver}.tar.xz"

    if [ $force_install ]; then
        # Cleanup QEMU dir
        qemu_utils.qemu_delete $qemu_install_dir $qemu_install_ver
    else
        # Test if QEMU was installed previously
        test -d $qemu_install_dir && \
            { echo "Qemu already installed: $qemu_install_dir"; exit 0; }
    fi

    tmp_dir=$(mktemp -d) || \
        { echo "Failed to create temporary working dir"; exit 1; }
    trap "rm -r ${tmp_dir}" EXIT

    # Download QEMU source code if no local copy exists
    if [ ! -f /opt/${qemu_install_ver}.tar.xz ]; then
        sudo wget -e use_proxy=yes -P /opt -q ${qemu_package_url} || \
            { echo "Failed to download ${qemu_install_ver}"; exit 1; }
    fi
    tar --strip-components 1 -xvJf ${tmp_dir}/${qemu_install_ver}.tar.xz -C ${tmp_dir} && \
        { echo "Failed to exctract ${qemu_install_ver}.tar.xz"; exit 1; }

    cd ${tmp_dir}
    sudo mkdir -p ${qemu_install_dir} || \
        { echo "Failed to create ${qemu_install_dir}"; exit 1; }

    # Apply additional patches
    if [ $qemu_patch ]
    then
        chmod +x ${SCRIPT_DIR}/qemu_patches/${qemu_install_ver}/*
        run-parts --verbose --report  ${SCRIPT_DIR}/qemu_patches/${qemu_install_ver}
    fi

    # Build
    sudo ./configure --target-list=x86_64-softmmu --prefix=${qemu_install_dir}/${qemu_install_ver} || \
        { echo "Failed to configure ${qemu_install_ver}"; exit 1; }
    sudo make -j`nproc` || \
        { echo "Failed to compile ${qemu_install_ver}"; exit 1; }
    sudo make install || \
        { echo "Failed to install ${qemu_install_ver}"; exit 1; }

    echo "QEMU ${qemu_install_ver} ready"
}