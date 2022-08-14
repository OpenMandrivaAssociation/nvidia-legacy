%global debug_package %{nil}
%global version_major 470
%global version_minor 141
%global version_patch 03
%global _dracut_conf_d  %{_prefix}/lib/dracut/dracut.conf.d
%global _modprobe_d     %{_prefix}/lib/modprobe.d/
%define _tar_end %{?extension}%{?!extension:gz}
%ifarch x86_64
%global extracted_source %{_builddir}/NVIDIA-Linux-x86_64-%{version}
%endif
%ifarch aarch64
%global extracted_source %{_builddir}/NVIDIA-Linux-aarch64-%{version}
%endif

# =======================================================================================#
# nvidia-driver - modified from https://github.com/NVIDIA/yum-packaging-nvidia-driver
# =======================================================================================#

Summary:	Binary-only driver for nvidia graphics chips, version %{version_major}
Name:		nvidia-legacy
%if %{version_patch}
Version:	%{version_major}.%{version_minor}.%{version_patch}
%else
Version:	%{version_major}.%{version_minor}
%endif
Release:	1
ExclusiveArch:	%{x86_64} %{aarch64}
Url:		http://www.nvidia.com/object/unix.html
Source0:	http://download.nvidia.com/XFree86/Linux-x86_64/%{version}/NVIDIA-Linux-x86_64-%{version}.run
Source1:	http://download.nvidia.com/XFree86/Linux-aarch64/%{version}/NVIDIA-Linux-aarch64-%{version}.run
Source2:	10-nvidia-driver.conf
Source3:	10-nvidia.conf
Source5:	99-nvidia-modules.conf
Source7:	alternate-install-present
Source8:	com.nvidia.driver.metainfo.xml
Source9:	parse-supported-gpus.py

#Patch0:         nvidia-fix-linux-5.10.patch
Group:		Hardware
License:	distributable
%ifarch x86_64 aarch64 ppc64le
BuildRequires:  lib64appstream-glib-devel >= 0.6.3
%endif

BuildRequires: systemd-rpm-macros

Requires:       %{name}-libs%{?_isa} = %{version}
Requires:       %{name}-kmod-common = %{version}

Requires:       x11-server-xorg >= 1.19.0-3


Provides:       %{name} = %{version}
Obsoletes:      xorg-x11-drv-nvidia
Conflicts:      catalyst-x11-drv
Conflicts:      catalyst-x11-drv-legacy
Conflicts:      fglrx-x11-drv
Conflicts:      nvidia-x11-drv
Conflicts:      nvidia-x11-drv-173xx
Conflicts:      nvidia-x11-drv-304xx
Conflicts:      nvidia-x11-drv-340xx
Conflicts:      nvidia-x11-drv-390xx
Conflicts:      xorg-x11-drv-nvidia
Conflicts:      xorg-x11-drv-nvidia-173xx
Conflicts:      xorg-x11-drv-nvidia-304xx
Conflicts:      xorg-x11-drv-nvidia-340xx
Conflicts:      xorg-x11-drv-nvidia-390xx

%description
This is a binary-only driver for nvidia graphics chips.

It is NOT supported.
It may WIPE YOUR HARDDISK, SEND ALL YOUR DATA TO YOUR COMPETITORS,
and worse.
It is developed by a very Anti-Linux company, and source code is not
released so nobody but them can tell what it actually does.

The preferred way to solve the problem is to BOYCOTT NVIDIA!
Alternatively, use the Nouveau driver that comes with the default
installation.

This package should only be used as a last resort.

%ifarch %{x86_64}
%package 32bit
Summary:	Binary-only 32-bit driver for nvidia graphics chips

Requires:   %{name}
Provides:   libGLdispatch0
Provides:   libGL1
Provides:   libEGL1
Provides:   libGLESv2_2
Provides:   libOpenGL0

%description 32bit
This is a 32-bit binary-only driver for nvidia graphics chips.

It is NOT supported.
It may WIPE YOUR HARDDISK, SEND ALL YOUR DATA TO YOUR COMPETITORS,
and worse.
It is developed by a very Anti-Linux company, and source code is not
released so nobody but them can tell what it actually does.

The preferred way to solve the problem is to BOYCOTT NVIDIA!
Alternatively, use the Nouveau driver that comes with the default
installation.

This package should only be used as a last resort.
%endif

%package libs
Summary:        Libraries for %{name}
Requires(post): ldconfig
%ifnarch ppc64le
Requires:       libvdpau1 >= 0.5
%endif
Requires:           libglvnd

%ifnarch aarch64 ppc64le
Requires:       vulkan-loader
%endif

Obsoletes:      xorg-x11-drv-nvidia-gl
Obsoletes:      xorg-x11-drv-nvidia-libs
Obsoletes:		nvidia-kernel-modules-desktop
Obsoletes:		nvidia-kernel-modules-desktop-clang
Obsoletes:		nvidia-kernel-modules-desktop-gcc
Obsoletes:		nvidia-kernel-modules-rc-desktop
Obsoletes:		nvidia-kernel-modules-server
Obsoletes:		nvidia-kernel-modules-server-clang
Obsoletes:		nvidia-kernel-modules-server-gcc
Obsoletes:		nvidia-kernel-modules-rc-server
Conflicts:      nvidia-x11-drv-libs
Conflicts:      nvidia-x11-drv-libs-96xx
Conflicts:      nvidia-x11-drv-libs-173xx
Conflicts:      nvidia-x11-drv-libs-304xx
Conflicts:      nvidia-x11-drv-libs-340xx
Conflicts:      nvidia-x11-drv-libs-390xx
Conflicts:      xorg-x11-drv-nvidia-gl
Conflicts:      xorg-x11-drv-nvidia-libs
Conflicts:      xorg-x11-drv-nvidia-libs-173xx
Conflicts:      xorg-x11-drv-nvidia-libs-304xx
Conflicts:      xorg-x11-drv-nvidia-libs-340xx
Conflicts:      xorg-x11-drv-nvidia-libs-390xx
%ifarch %{ix86}
Conflicts:      nvidia-x11-drv-32bit
Conflicts:      nvidia-x11-drv-32bit-96xx
Conflicts:      nvidia-x11-drv-32bit-173xx
Conflicts:      nvidia-x11-drv-32bit-304xx
Conflicts:      nvidia-x11-drv-32bit-340xx
Conflicts:      nvidia-x11-drv-32bit-390xx
%endif

%description libs
This package provides the shared libraries for %{name}.

%package cuda-libs
Summary:        Libraries for %{name}-cuda
Requires(post): ldconfig

%description cuda-libs
This package provides the CUDA libraries for %{name}-cuda.

%package NvFBCOpenGL
Summary:        NVIDIA OpenGL-based Framebuffer Capture libraries
# Loads libnvidia-encode.so at runtime
Requires:       %{name}-cuda-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description NvFBCOpenGL
This library provides a high performance, low latency interface to capture and
optionally encode the composited framebuffer of an X screen. NvFBC and NvIFR are
private APIs that are only available to NVIDIA approved partners for use in
remote graphics scenarios.

%package NVML
Summary:        NVIDIA Management Library (NVML)
Requires(post): ldconfig
Provides:       cuda-nvml%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description NVML
A C-based API for monitoring and managing various states of the NVIDIA GPU
devices. It provides a direct access to the queries and commands exposed via
nvidia-smi. The run-time version of NVML ships with the NVIDIA display driver,
and the SDK provides the appropriate header, stub libraries and sample
applications. Each new version of NVML is backwards compatible and is intended
to be a platform for building 3rd party applications.

%package cuda
Summary:        CUDA integration for %{name}
Conflicts:      xorg-x11-drv-nvidia-cuda
Requires:       %{name}-cuda-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}
%ifnarch aarch64
Requires:       nvidia-persistenced = %{?epoch:%{epoch}:}%{version}
%endif
Requires:       opencl-filesystem
Requires:       ocl-icd

%description cuda
This package provides the CUDA integration components for %{name}.

%package devel
Summary:        Development files for %{name}
Conflicts:      xorg-x11-drv-nvidia-devel
Conflicts:      xorg-x11-drv-nvidia-devel-173xx
Conflicts:      xorg-x11-drv-nvidia-devel-304xx
Conflicts:      xorg-x11-drv-nvidia-devel-340xx
Conflicts:      xorg-x11-drv-nvidia-devel-390xx
Requires:       %{name}-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-cuda-libs%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires:       %{name}-NvFBCOpenGL%{?_isa} = %{?epoch:%{epoch}:}%{version}-%{release}

%description devel
This package provides the development files of the %{name} package.

# =======================================================================================#
# dkms-nvidia - modified from https://github.com/NVIDIA/yum-packaging-dkms-nvidia
# =======================================================================================#

%package dkms-kmod
License:        NVIDIA License
Summary:        NVIDIA display driver kernel module. **This is an unsupported proprietary driver. Use with caution!
URL:            http://www.nvidia.com/object/unix.html

# Package is not noarch as it contains pre-compiled binary code
ExclusiveArch:  x86_64 ppc64le aarch64
Source10:   dkms-nvidia.conf

BuildRequires:  sed

Provides:       dkms-kmod = %{version}
Requires:       kmod-common = %{version}
Requires:       dkms

%description dkms-kmod
This package provides the proprietary Nvidia kernel driver modules.
The modules are rebuilt through the DKMS system when a new kernel or modules
become available.

%package -n kmod-headers
Summary:        NVIDIA header files for precompiled streams
AutoReq:        0
Conflicts:      kmod-nvidia-latest-dkms

%description -n kmod-headers
NVIDIA header files for precompiled streams

# =======================================================================================#
# nvidia-kmod-common - modified from https://github.com/NVIDIA/yum-packaging-nvidia-kmod-common
# =======================================================================================#

%package kmod-common
Summary:        Common file for NVIDIA's proprietary driver kernel modules
License:        NVIDIA License
URL:            http://www.nvidia.com/object/unix.html

BuildArch:      noarch
Source4:	60-nvidia.rules
Source6:	99-nvidia.conf
Source11:   nvidia.conf

BuildRequires:  systemd-rpm-macros

Requires:       nvidia-kmod = %{?epoch:%{epoch}:}%{version}
Provides:       nvidia-kmod-common = %{?epoch:%{epoch}:}%{version}
Requires:       nvidia-driver = %{?epoch:%{epoch}:}%{version}
Obsoletes:      cuda-nvidia-kmod-common

%description kmod-common
This package provides the common files required by all NVIDIA kernel module
package variants.

# =======================================================================================#
# nvidia-persistenced - modified from https://github.com/NVIDIA/yum-packaging-nvidia-persistenced
# =======================================================================================#

%package persistenced
Summary:        A daemon to maintain persistent software state in the NVIDIA driver
URL:            http://www.nvidia.com/object/unix.html
ExclusiveArch:  %{ix86} x86_64 ppc64le aarch64

Source12:        https://download.nvidia.com/XFree86/nvidia-persistenced/nvidia-persistenced-%{version}.tar.%{_tar_end}
Source13:        nvidia-persistenced.service
Source14:        nvidia-persistenced.init

BuildRequires:  gcc
BuildRequires:  lib64tirpc-devel
BuildRequires:  m4

BuildRequires:      systemd
Requires(post):     systemd
Requires(preun):    systemd
Requires(postun):   systemd

Requires(pre):      shadow-utils
Requires:           %{name}-cuda = %{version}

%description persistenced
The nvidia-persistenced utility is used to enable persistent software state in the NVIDIA
driver. When persistence mode is enabled, the daemon prevents the driver from
releasing device state when the device is not in use. This can improve the
startup time of new clients in this scenario.

%prep
rm -rf %{extracted_source}
rm -rf nvidia-persistenced-%{version}
# persistenced
%setup -T -b 12 -q -n nvidia-persistenced-%{version}
# Remove additional CFLAGS added when enabling DEBUG
sed -i -e '/+= -O0 -g/d' utils.mk


# end persistenced

cd %{_builddir}

%ifarch %{x86_64}
sh %{S:0} --extract-only
%endif
%ifarch %{aarch64}
sh %{S:1} --extract-only
%endif
cp -f %{SOURCE10} %{extracted_source}/kernel/dkms.conf
sed -i -e 's/__VERSION_STRING/%{version}/g' %{extracted_source}/kernel/dkms.conf

cd %{extracted_source}

# Create symlinks for shared objects
ldconfig -vn .

# Required for building gstreamer 1.0 NVENC plugins
ln -sf libnvidia-encode.so.%{version} libnvidia-encode.so
# Required for building ffmpeg 3.1 Nvidia CUVID
ln -sf libnvcuvid.so.%{version} libnvcuvid.so

# Required for building against CUDA
ln -sf libcuda.so.%{version} libcuda.so

# Required for building additional applications agains the driver stack
ln -sf libnvidia-ml.so.%{version}               libnvidia-ml.so
ln -sf libnvidia-ptxjitcompiler.so.%{version}   libnvidia-ptxjitcompiler.so
ln -sf libnvidia-nvvm.so.%{version}             libnvidia-nvvm.so
%ifnarch %{ix86}
ln -sf libnvidia-cfg.so.%{version}              libnvidia-cfg.so
%endif
%ifnarch ppc64le
ln -sf libnvidia-fbc.so.%{version}              libnvidia-fbc.so
%endif

# libglvnd indirect entry point
ln -sf libGLX_nvidia.so.%{version} libGLX_indirect.so.0

cat ./nvidia_icd.json > nvidia_icd.%{_target_cpu}.json

%build
cd %{_builddir}/nvidia-persistenced-%{version}
export CFLAGS="%{optflags} -I%{_includedir}/tirpc"
export LDFLAGS="%{?__global_ldflags} -ltirpc"
make %{?_smp_mflags} \
    DEBUG=1 \
    LIBS="-ldl -ltirpc" \
    NV_VERBOSE=1 \
    PREFIX=%{_prefix} \
    STRIP_CMD=true

%install
cd %{_builddir}/nvidia-persistenced-%{version}
%make_install \
    NV_VERBOSE=1 \
    PREFIX=%{_prefix} \
    STRIP_CMD=true

mkdir -p %{buildroot}%{_sharedstatedir}/nvidia-persistenced

# Systemd unit files
install -p -m 644 -D %{SOURCE13} %{buildroot}%{_unitdir}/nvidia-persistenced.service

cd %{extracted_source}
mkdir -p %{buildroot}%{_datadir}/glvnd/egl_vendor.d/
mkdir -p %{buildroot}%{_datadir}/vulkan/icd.d/
mkdir -p %{buildroot}%{_datadir}/egl/egl_external_platform.d/
mkdir -p %{buildroot}%{_includedir}/nvidia/GL/
mkdir -p %{buildroot}%{_libdir}/vdpau/

# dkms-kmod
# Create empty tree
mkdir -p %{buildroot}%{_usrsrc}/dkms-kmod-%{version}/
cp -fr kernel/* %{buildroot}%{_usrsrc}/dkms-kmod-%{version}/

mkdir -p %{buildroot}%{_udevrulesdir}
mkdir -p %{buildroot}%{_modprobe_d}/
mkdir -p %{buildroot}%{_dracut_conf_d}/
mkdir -p %{buildroot}%{_unitdir}
mkdir -p %{buildroot}%{_presetdir}

# Blacklist nouveau and load nvidia-uvm:
install -p -m 0644 %{SOURCE11} %{buildroot}%{_modprobe_d}/

# Avoid Nvidia modules getting in the initrd:
install -p -m 0644 %{SOURCE6} %{buildroot}%{_dracut_conf_d}/

# UDev rules:
# https://github.com/NVIDIA/nvidia-modprobe/blob/master/modprobe-utils/nvidia-modprobe-utils.h#L33-L46
# https://github.com/negativo17/nvidia-driver/issues/27
install -p -m 644 %{SOURCE4} %{buildroot}%{_udevrulesdir}

%ifarch x86_64 aarch64 ppc64le

mkdir -p %{buildroot}%{_bindir}
mkdir -p %{buildroot}%{_datadir}/nvidia/
mkdir -p %{buildroot}%{_libdir}/nvidia/wine/
mkdir -p %{buildroot}%{_libdir}/xorg/modules/drivers/
mkdir -p %{buildroot}%{_libdir}/xorg/modules/extensions/
mkdir -p %{buildroot}%{_mandir}/man1/
mkdir -p %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/
mkdir -p %{buildroot}%{_sysconfdir}/nvidia/
mkdir -p %{buildroot}%{_sysconfdir}/OpenCL/vendors/

mkdir -p %{buildroot}%{_datadir}/vulkan/implicit_layer.d/
mkdir -p %{buildroot}%{_unitdir}/
mkdir -p %{buildroot}%{_systemd_util_dir}/system-sleep/

mkdir -p %{buildroot}%{_datadir}/appdata/

# OpenCL config
install -p -m 0755 nvidia.icd %{buildroot}%{_sysconfdir}/OpenCL/vendors/

# Binaries
install -p -m 0755 nvidia-{debugdump,smi,cuda-mps-control,cuda-mps-server,bug-report.sh} %{buildroot}%{_bindir}

%ifarch x86_64
mkdir -p %{buildroot}%{_dbus_systemd_dir}/
# not present in 470
#install -p -m 0755 nvidia-powerd %%{buildroot}%%{_bindir}
cp -r %{extracted_source}/32/* %{buildroot}%{_prefix}/lib/
%endif

# Man pages
install -p -m 0644 nvidia-{smi,cuda-mps-control}*.gz %{buildroot}%{_mandir}/man1/

# install AppData and add modalias provides
install -p -m 0644 %{SOURCE8} %{buildroot}%{_datadir}/appdata/
fn=%{buildroot}%{_datadir}/appdata/com.nvidia.driver.metainfo.xml
%{SOURCE9} supported-gpus/supported-gpus.json | xargs appstream-util add-provide ${fn} modalias

install -p -m 0644 %{SOURCE3} %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/10-nvidia.conf
sed -i -e 's|@LIBDIR@|%{_libdir}|g' %{buildroot}%{_sysconfdir}/X11/xorg.conf.d/10-nvidia.conf

# X stuff
install -p -m 0755 nvidia_drv.so %{buildroot}%{_libdir}/xorg/modules/drivers/
install -p -m 0755 libglxserver_nvidia.so.%{version} %{buildroot}%{_libdir}/xorg/modules/extensions/libglxserver_nvidia.so

# NVIDIA specific configuration files
install -p -m 0644 nvidia-application-profiles-%{version}-key-documentation \
    %{buildroot}%{_datadir}/nvidia/
install -p -m 0644 nvidia-application-profiles-%{version}-rc \
    %{buildroot}%{_datadir}/nvidia/

%endif

# alternate-install-present file triggers runfile warning
%ifnarch %{ix86}
install -m 0755 -d %{buildroot}/usr/lib/nvidia/
install -p -m 0644 %{SOURCE7} %{buildroot}/usr/lib/nvidia/
%endif

# gsp.bin
install -m 0755 -d %{buildroot}/lib/firmware/nvidia/%{version}/
%ifarch x86_64 aarch64
install -p -m 0644 firmware/gsp.bin %{buildroot}/lib/firmware/nvidia/%{version}/
%endif

# Vulkan and EGL loaders
install -p -m 0644 nvidia_icd.%{_target_cpu}.json %{buildroot}%{_datadir}/vulkan/icd.d/
install -p -m 0644 10_nvidia.json %{buildroot}%{_datadir}/glvnd/egl_vendor.d/

# GBM files
%ifnarch %{ix86}
# not present in 470
#install -p -m 0644 15_nvidia_gbm.json %%{buildroot}%%{_datadir}/egl/egl_external_platform.d/
mkdir -p %{buildroot}%{_libdir}/gbm/
ln -sf %{_libdir}/libnvidia-allocator.so.1 %{buildroot}%{_libdir}/gbm/nvidia-drm_gbm.so
%endif

# NGX Proton/Wine library
%ifarch x86_64
cp -a *.dll %{buildroot}%{_libdir}/nvidia/wine/
%endif

# Unique libraries
cp -a lib*GL*_nvidia.so* libcuda.so* libnv*.so* %{buildroot}%{_libdir}/
cp -a libnvcuvid.so* %{buildroot}%{_libdir}/
cp -a libvdpau_nvidia.so* %{buildroot}%{_libdir}/vdpau/
%ifarch x86_64 aarch64
cp -a libnvoptix.so* %{buildroot}%{_libdir}/
%endif

# nvidia-powerd
%ifarch x86_64
# not present in 470
#install -p -m 0644 nvidia-dbus.conf %%{buildroot}%%{_dbus_systemd_dir}/
#install -p -m 0644 systemd/system/nvidia-powerd.service %%{buildroot}%%{_unitdir}/
%endif

# Systemd units and script for suspending/resuming
%ifnarch %{ix86}
install -p -m 0644 systemd/system/nvidia-hibernate.service %{buildroot}%{_unitdir}/
install -p -m 0644 systemd/system/nvidia-resume.service %{buildroot}%{_unitdir}/
install -p -m 0644 systemd/system/nvidia-suspend.service %{buildroot}%{_unitdir}/
install -p -m 0755 systemd/nvidia-sleep.sh %{buildroot}%{_bindir}/
install -p -m 0755 systemd/system-sleep/nvidia %{buildroot}%{_systemd_util_dir}/system-sleep/
%endif


%post
%systemd_post nvidia-hibernate.service
%systemd_post nvidia-resume.service
%systemd_post nvidia-suspend.service

%ifarch x86_64
# not present in 470
#%%systemd_post nvidia-powerd.service
%endif

%preun
%systemd_preun nvidia-hibernate.service
%systemd_preun nvidia-resume.service
%systemd_preun nvidia-suspend.service

%ifarch x86_64
# not present in 470
#%%systemd_preun nvidia-powerd.service
%endif

%postun
%systemd_postun nvidia-hibernate.service
%systemd_postun nvidia-resume.service
%systemd_postun nvidia-suspend.service

%ifarch x86_64
# not present in 470
#%%systemd_postun nvidia-powerd.service
%endif

%ldconfig_scriptlets libs

%ldconfig_scriptlets cuda-libs

%ldconfig_scriptlets NvFBCOpenGL

%ldconfig_scriptlets NVML

%ifnarch %{ix86}

%files
#%license LICENSE
#%doc NVIDIA_Changelog README.txt html

%dir %{_sysconfdir}/nvidia
%{_bindir}/nvidia-bug-report.sh
%{_datadir}/appdata/com.nvidia.driver.metainfo.xml
%{_datadir}/nvidia
%{_libdir}/xorg/modules/extensions/libglxserver_nvidia.so
%{_libdir}/xorg/modules/drivers/nvidia_drv.so
%{_bindir}/nvidia-sleep.sh
%{_systemd_util_dir}/system-sleep/nvidia
%{_unitdir}/nvidia-hibernate.service
%{_unitdir}/nvidia-resume.service
%{_unitdir}/nvidia-suspend.service
/lib/firmware/nvidia/%{version}
%ifnarch %{ix86}
/usr/lib/nvidia/alternate-install-present
%endif

# nvidia-powerd
%ifarch x86_64
# not present in 470
#%%{_unitdir}/nvidia-powerd.service
#%%config(noreplace) %%{_dbus_systemd_dir}/nvidia-dbus.conf
%endif

# X.org configuration files
%config(noreplace) %{_sysconfdir}/X11/xorg.conf.d/10-nvidia.conf

%files cuda
%{_sysconfdir}/OpenCL/vendors/*
%{_bindir}/nvidia-cuda-mps-control
%{_bindir}/nvidia-cuda-mps-server
%{_bindir}/nvidia-debugdump
%ifarch x86_64
# not found in 470
#%%{_bindir}/nvidia-powerd
%endif
%{_bindir}/nvidia-smi
%{_mandir}/man1/nvidia-cuda-mps-control.1.*
%{_mandir}/man1/nvidia-smi.*

%endif

%files devel
%{_includedir}/nvidia/
%{_libdir}/libnvcuvid.so
%{_libdir}/libnvidia-encode.so
%{_libdir}/libnvidia-ml.so
%{_libdir}/libnvidia-ptxjitcompiler.so
%{_libdir}/libnvidia-nvvm.so
%ifnarch %{ix86}
%{_libdir}/libnvidia-cfg.so
%endif
%ifnarch ppc64le
%{_libdir}/libnvidia-fbc.so
%endif

%files libs
%{_datadir}/glvnd/egl_vendor.d/10_nvidia.json
%{_datadir}/vulkan/icd.d/nvidia_icd.%{_target_cpu}.json
%{_libdir}/libnvidia-cbl.so.%{version}
%{_libdir}/libnvidia-egl-wayland.so.1.1.7
%{_libdir}/libnvidia-ifr.so.*
%{_libdir}/libnvidia-nvvm.so.4.0.0
%{_libdir}/libEGL_nvidia.so.0
%{_libdir}/libEGL_nvidia.so.%{version}
%{_libdir}/libGLESv1_CM_nvidia.so.1
%{_libdir}/libGLESv1_CM_nvidia.so.%{version}
%{_libdir}/libGLESv2_nvidia.so.2
%{_libdir}/libGLESv2_nvidia.so.%{version}
%{_libdir}/libGLX_nvidia.so.0
%{_libdir}/libGLX_nvidia.so.%{version}
%ifarch x86_64 ppc64le aarch64
%{_libdir}/libnvidia-cfg.so.1
%{_libdir}/libnvidia-cfg.so.%{version}
# not found in 470
#%%{_libdir}/libnvidia-egl-gbm.so.1
#%%{_libdir}/libnvidia-egl-gbm.so.1.1.0
%{_libdir}/gbm/nvidia-drm_gbm.so
# not found in 470
#%%{_datadir}/egl/egl_external_platform.d/15_nvidia_gbm.json
%endif
%{_libdir}/libnvidia-eglcore.so.%{version}
%{_libdir}/libnvidia-glcore.so.%{version}
%{_libdir}/libnvidia-glsi.so.%{version}
%ifarch x86_64 aarch64
# Raytracing
%{_libdir}/libnvidia-rtcore.so.%{version}
%{_libdir}/libnvoptix.so.1
%{_libdir}/libnvoptix.so.%{version}
%{_libdir}/libnvidia-ngx.so.1
%{_libdir}/libnvidia-ngx.so.%{version}
%endif
# Wine libraries
%ifarch x86_64
%dir %{_libdir}/nvidia
%dir %{_libdir}/nvidia/wine
%{_libdir}/nvidia/wine/*.dll
%endif

%{_libdir}/libnvidia-tls.so.%{version}
%{_libdir}/vdpau/libvdpau_nvidia.so.1
%{_libdir}/vdpau/libvdpau_nvidia.so.%{version}
%{_libdir}/libnvidia-allocator.so.1
%{_libdir}/libnvidia-allocator.so.%{version}
%{_libdir}/libnvidia-egl-wayland.so.1
# not found in 470
#%%{_libdir}/libnvidia-egl-wayland.so.1.1.9
%{_libdir}/libnvidia-glvkspirv.so.%{version}
%{_libdir}/libnvidia-gtk2.so.%{version}
%{_libdir}/libnvidia-gtk3.so.%{version}

%files cuda-libs
%{_libdir}/libcuda.so
%{_libdir}/libcuda.so.1
%{_libdir}/libcuda.so.%{version}
%{_libdir}/libnvcuvid.so.1
%{_libdir}/libnvcuvid.so.%{version}
%ifnarch ppc64le aarch64
%{_libdir}/libnvidia-compiler.so.%{version}
%endif
%{_libdir}/libnvidia-encode.so.1
%{_libdir}/libnvidia-encode.so.%{version}
%{_libdir}/libnvidia-nvvm.so.4
# not found in 470
#%%{_libdir}/libnvidia-nvvm.so.%%{version}
%{_libdir}/libnvidia-opticalflow.so.1
%{_libdir}/libnvidia-opticalflow.so.%{version}
%{_libdir}/libnvidia-opencl.so.1
%{_libdir}/libnvidia-opencl.so.%{version}
%{_libdir}/libnvidia-ptxjitcompiler.so.1
%{_libdir}/libnvidia-ptxjitcompiler.so.%{version}
%ifnarch %{ix86}
%{_libdir}/libnvidia-vulkan-producer.so.%{version}
%endif
%ifarch x86_64
# not found in 470
#%%{_libdir}/libnvidia-wayland-client.so.%%{version}
%endif

%files NvFBCOpenGL
%ifnarch ppc64le
%{_libdir}/libnvidia-fbc.so.1
%{_libdir}/libnvidia-fbc.so.%{version}
%endif

%files NVML
%{_libdir}/libnvidia-ml.so.1
%{_libdir}/libnvidia-ml.so.%{version}

%ifarch %{x86_64}
%files 32bit
%{_prefix}/lib/libnvidia-allocator.so.%{version}
%{_prefix}/lib/libnvidia-glcore.so*
%{_prefix}/lib/libGLX_nvidia.so*
%{_prefix}/lib/libEGL_nvidia.so*
%{_prefix}/lib/libnvidia-eglcore.so*
%{_prefix}/lib/libGLESv1_CM_nvidia.so*
%{_prefix}/lib/libGLESv2_nvidia.so*
%{_prefix}/lib/libnvidia-ifr.so.*
%{_prefix}/lib/libnvidia-glsi.so*
%{_prefix}/lib/libcuda.so*
%{_prefix}/lib/libnvcuvid.so*
%{_prefix}/lib/libnvidia-ml.so*
%{_prefix}/lib/libnvidia-opticalflow.so.%{version}
%{_prefix}/lib/libnvidia-ptxjitcompiler.so*
%{_prefix}/lib/libnvidia-tls.so*
%{_prefix}/lib/libnvidia-compiler.so*
%{_prefix}/lib/libnvidia-opencl.so*
%{_prefix}/lib/libnvidia-encode.so*
%{_prefix}/lib/libnvidia-fbc.so*
%{_prefix}/lib/libvdpau_nvidia.so*
%{_prefix}/lib/libnvidia-glvkspirv.so*
%{_prefix}/lib/libEGL.so.1
%{_prefix}/lib/libEGL.so.1.1.0
%{_prefix}/lib/libGL.so.1
%{_prefix}/lib/libGL.so.1.7.0
%{_prefix}/lib/libGLESv1_CM.so.1
%{_prefix}/lib/libGLESv1_CM.so.1.2.0
%{_prefix}/lib/libGLESv2.so.2
%{_prefix}/lib/libGLESv2.so.2.1.0
%{_prefix}/lib/libGLX.so.0
%{_prefix}/lib/libGLdispatch.so.0
%{_prefix}/lib/libOpenCL.so.1
%{_prefix}/lib/libOpenCL.so.1.0.0
%{_prefix}/lib/libOpenGL.so.0
%{_prefix}/lib/libglvnd_install_checker/glvnd_check
%{_prefix}/lib/libglvnd_install_checker/libGLX_installcheck.so.0
%{_prefix}/lib/libnvidia-allocator.so.1
%{_prefix}/lib/libnvidia-opticalflow.so.1
%endif

%post dkms-kmod
dkms add -m %{name}-dkms-kmod -v %{version} -q || :
# Rebuild and make available for the currently running kernel
dkms build -m %{name}-dkms-kmod -v %{version} -q || :
dkms install -m %{name}-dkms-kmod -v %{version} -q --force || :

%preun dkms-kmod
# Remove all versions from DKMS registry
dkms remove -m %{name}-dkms-kmod -v %{version} -q --all || :

%files dkms-kmod
%{_usrsrc}/dkms-kmod-%{version}

%files -n kmod-headers
%{_usrsrc}/dkms-kmod-%{version}

%post kmod-common
sed -i 's/GRUB_CMDLINE_LINUX_DEFAULT="/GRUB_CMDLINE_LINUX_DEFAULT="rd.driver.blacklist=nouveau /' %{_sysconfdir}/default/grub
/sbin/depmod -a
/usr/bin/dracut -f
%{_sbindir}/update-grub2

%postun kmod-common
sed -i 's/rd.driver.blacklist=nouveau //g' %{_sysconfdir}/default/grub
/sbin/depmod -a
/usr/bin/dracut -f
%{_sbindir}/update-grub2

%files kmod-common
%{_dracut_conf_d}/99-nvidia.conf
%{_modprobe_d}/nvidia.conf
%{_udevrulesdir}/60-nvidia.rules

%pre persistenced
getent group nvidia-persistenced >/dev/null || groupadd -r nvidia-persistenced
getent passwd nvidia-persistenced >/dev/null || \
    useradd -r -g nvidia-persistenced -d /var/run/nvidia-persistenced -s /sbin/nologin \
    -c "NVIDIA persistent software state" nvidia-persistenced
exit 0

%post  persistenced
%systemd_post nvidia-persistenced.service

%preun persistenced
%systemd_preun nvidia-persistenced.service

%postun persistenced
%systemd_postun_with_restart nvidia-persistenced.service

%files persistenced
#%license COPYING
%{_mandir}/man1/nvidia-persistenced.1.*
%{_bindir}/nvidia-persistenced
%{_unitdir}/nvidia-persistenced.service
%attr(750,nvidia-persistenced,nvidia-persistenced) %{_sharedstatedir}/nvidia-persistenced
