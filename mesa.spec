# (cg) Cheater...
%define Werror_cflags %{nil}

# (aco) Needed for the dri drivers
%define _disable_ld_no_undefined 1
%define _disable_lto 1

%define git %{nil}
%define git_branch %(echo %{version} |cut -d. -f1-2)

# (tpg) starting version 11.1.1 this may fully support OGL 4.1
%define opengl_ver 3.3

%define relc 4

# bootstrap option: Build without requiring an X server
# (which in turn requires mesa to build)
%bcond_without hardware
%bcond_with gcc
%bcond_with bootstrap
%bcond_without vdpau
%bcond_without va
%bcond_without wayland
%bcond_without egl
%bcond_without opencl
%bcond_without tfloat
# Broken as of 10.4.0-rc1 -- re-enable by default when fixed
%bcond_with openvg
%ifarch %arm mips sparc aarch64
%bcond_with intel
%else
%bcond_without intel
%endif
# Sometimes it's necessary to disable r600 while bootstrapping
# an LLVM change (such as the r600 -> AMDGPU rename)
%bcond_without r600

%if "%{relc}" != ""
%define vsuffix -rc%{relc}
%else
%define vsuffix %{nil}
%endif

%define osmesamajor	8
%define libosmesa	%mklibname osmesa %{osmesamajor}
%define devosmesa	%mklibname osmesa -d

%define eglmajor	1
%define eglname		egl
%define libegl		%mklibname %{eglname} %{eglmajor}
%define devegl		%mklibname %{eglname} -d

%define glmajor		1
%define glname		gl
%define libgl		%mklibname %{glname} %{glmajor}
%define devgl		%mklibname %{glname} -d

%define glesv1major	1
%define glesv1name	glesv1
%define libglesv1	%mklibname %{glesv1name}_ %{glesv1major}
%define devglesv1	%mklibname %{glesv1name} -d

%define glesv2major	2
%define glesv2name	glesv2
%define libglesv2	%mklibname %{glesv2name}_ %{glesv2major}
%define devglesv2	%mklibname %{glesv2name} -d

%define devglesv3	%mklibname glesv3 -d

%define d3dmajor	1
%define d3dname		d3dadapter9
%define libd3d		%mklibname %{d3dname} %{d3dmajor}
%define devd3d		%mklibname %{d3dname} -d

%define openvgmajor	1
%define openvgname	openvg
%define libopenvg	%mklibname %{openvgname} %{openvgmajor}
%define devopenvg	%mklibname %{openvgname} -d

%define glapimajor	0
%define glapiname	glapi
%define libglapi	%mklibname %{glapiname} %{glapimajor}
%define devglapi	%mklibname %{glapiname} -d

%define dridrivers	%mklibname dri-drivers

%define gbmmajor	1
%define gbmname		gbm
%define libgbm		%mklibname %{gbmname} %{gbmmajor}
%define devgbm		%mklibname %{gbmname} -d

%define xatrackermajor	2
%define xatrackername	xatracker
%define libxatracker	%mklibname %xatrackername %{xatrackermajor}
%define devxatracker	%mklibname %xatrackername -d

%define clmajor		1
%define clname		opencl
%define libcl		%mklibname %clname %clmajor
%define devcl		%mklibname %clname -d

%define waylandeglmajor	1
%define waylandeglname	wayland-egl
%define libwaylandegl	%mklibname %{waylandeglname} %{waylandeglmajor}
%define devwaylandegl	%mklibname %{waylandeglname} -d

%define libvadrivers	%mklibname va-drivers

%define mesasrcdir	%{_prefix}/src/Mesa/
%define driver_dir	%{_libdir}/dri

#FIXME: (for 386/485) unset SSE, MMX and 3dnow flags
#FIXME: (for >=i586)  disable sse
#       SSE seems to have problem on some apps (gtulpas) for probing.
%define	dri_drivers_i386	"i915,i965,nouveau,r200,radeon,swrast"
%define	dri_drivers_x86_64	%{dri_drivers_i386}
%define	dri_drivers_ppc		"r200,radeon,swrast"
%define	dri_drivers_ppc64	""
%define	dri_drivers_ia64	"i915,i965,mga,r200,radeon,swrast"
%define	dri_drivers_alpha	"r200,radeon,swrast"
%define	dri_drivers_sparc	"ffb,radeon,swrast"
%define dri_drivers_mipsel	"r200,radeon,swrast"
%define dri_drivers_arm		"nouveau,r200,radeon,swrast"
%define dri_drivers_aarch64	"nouveau,r200,radeon,swrast"
%define	dri_drivers		%{expand:%{dri_drivers_%{_arch}}}

%define short_ver %(if [ `echo %{version} |cut -d. -f3` = "0" ]; then echo %{version} |cut -d. -f1-2; else echo %{version}; fi)

Summary:	OpenGL %{opengl_ver} compatible 3D graphics library
Name:		mesa
Version:	12.0.0
%if "%{relc}%{git}" == ""
Release:	1
%else
%if "%{relc}" != ""
%if "%{git}" != ""
Release:	%{?relc:0.rc%{relc}}.0.%{git}.1
%else
Release:	%{?relc:0.rc%{relc}}.6
%endif
%else
Release:	%{?git:0.%{git}.}1
%endif
%endif
Group:		System/Libraries
License:	MIT
Url:		http://www.mesa3d.org
%if "%{git}" != ""
Source0:	%{name}-%{git_branch}-%{git}.tar.xz
%else
Source0:	ftp://ftp.freedesktop.org/pub/mesa/%{version}/mesa-%{version}%{vsuffix}.tar.xz
%endif
Source3:	make-git-snapshot.sh
Source5:	mesa-driver-install
Source100:	%{name}.rpmlintrc

%define dricoremajor	1
%define dricorename	dricore
%define devdricore	%mklibname %{dricorename} -d
%define libdricore	%mklibname %{dricorename} 9
Obsoletes:	%{libdricore} < %{EVRD}
Obsoletes:	%{devdricore} < %{EVRD}
Obsoletes:	%{name}-xorg-drivers < %{EVRD}
Obsoletes:	%{name}-xorg-drivers-radeon < %{EVRD}
Obsoletes:	%{name}-xorg-drivers-nouveau < %{EVRD}

# https://bugs.freedesktop.org/show_bug.cgi?id=74098
Patch1:	mesa-10.2-clang-compilefix.patch

Patch2: mesa-11.1.1-clang-3.8.patch

# fedora patches
Patch15: mesa-9.2-hardware-float.patch

# Instructions to setup your repository clone
# git://git.freedesktop.org/git/mesa/mesa
# git checkout mesa_7_5_branch
# git branch mdv-cherry-picks
# git am ../02??-*.patch
# git branch mdv-redhat
# git am ../03??-*.patch
# git branch mdv-patches
# git am ../09??-*.patch

# In order to update to the branch via patches, issue this command:
# git format-patch --start-number 100 mesa_7_5_1..mesa_7_5_branch | sed 's/^0\([0-9]\+\)-/Patch\1: 0\1-/'

# Cherry picks
# git format-patch --start-number 200 mesa_7_5_branch..mdv-cherry-picks

# Mandriva & Mageia patches

# git format-patch --start-number 100 mesa_7_5_1..mesa_7_5_branch | sed 's/^0\([0-9]\+\)-/Patch\1: 0\1-/'
Patch201: 0201-revert-fix-glxinitializevisualconfigfromtags-handling.patch

# Direct3D patchset -- https://wiki.ixit.cz/d3d9
#
# git clone git://anongit.freedesktop.org/git/mesa/mesa
# git remote add ixit https://github.com/iXit/Mesa-3D
# git fetch ixit
# git checkout -b d3d9 ixit/master
# git rebase origin/master
# git format-patch origin/master
# ( for i in 00*.patch; do PN=`echo $i |cut -b1-4 |sed 's,^0*,,g'`; echo Patch$((PN+1000)): $i; done ) >patchlist
# Currently empty -- current D3D9 bits have been merged into 10.4.0-rc1
# Leaving the infrastructure in place for future updates.

# https://bugs.freedesktop.org/show_bug.cgi?id=89599
#Patch203:	mesa-10.5.2-hide-few-symbols-to-workaround-clang.patch
# (tpg) this patch is only a workaround for https://bugs.freedesktop.org/show_bug.cgi?id=93454
# real fix is in one of millions commits in llvm git related to https://llvm.org/bugs/show_bug.cgi?id=24990
Patch204:	mesa-11.1.0-fix-SSSE3.patch
Patch206:	mesa-11.2-arm-no-regparm.patch
Patch207:	mesa-12.0-rc4-llvm-3.9.patch

BuildRequires:	flex
BuildRequires:	bison
BuildRequires:	gccmakedep
BuildRequires:	libxml2-python
BuildRequires:	makedepend
BuildRequires:	llvm-devel >= 3.3
BuildRequires:	pkgconfig(expat)
BuildRequires:	elfutils-devel
BuildRequires:	python2-mako
BuildRequires:	pkgconfig(libdrm) >= 2.4.56
BuildRequires:	pkgconfig(libudev) >= 186
BuildRequires:	pkgconfig(talloc)
BuildRequires:	pkgconfig(x11)		>= 1.3.3
BuildRequires:	pkgconfig(xdamage)	>= 1.1.1
BuildRequires:	pkgconfig(xext)		>= 1.1.1
BuildRequires:	pkgconfig(xfixes)	>= 4.0.3
BuildRequires:	pkgconfig(xi)		>= 1.3
BuildRequires:	pkgconfig(xmu)		>= 1.0.3
BuildRequires:	pkgconfig(xproto)
BuildRequires:	pkgconfig(xt)		>= 1.0.5
BuildRequires:	pkgconfig(xxf86vm)	>= 1.1.0
BuildRequires:	pkgconfig(xshmfence)	>= 1.1
%if %{with opencl}
BuildRequires:	pkgconfig(libclc)
BuildRequires:	clang-devel clang
%endif
BuildRequires:	pkgconfig(xvmc)
%if %{with vdpau}
BuildRequires:	pkgconfig(vdpau)	>= 0.4.1
%endif
%if %{with va}
BuildRequires:	pkgconfig(libva)	>= 0.31.0
%endif
%if %{with wayland}
BuildRequires:	pkgconfig(wayland-client)
BuildRequires:  pkgconfig(wayland-server)
%endif

# package mesa
Requires:	libGL.so.%{glmajor}%{_arch_tag_suffix}

%description
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.

%libpackage XvMCgallium 1

%package -n	%{dridrivers}
Summary:	Mesa DRI drivers
Group:		System/Libraries
%if %{with r600}
Requires:	%{dridrivers}-radeon = %{EVRD}
%endif
%ifnarch %{armx}
Requires:	%{dridrivers}-intel = %{EVRD}
%endif
Requires:	%{dridrivers}-nouveau = %{EVRD}
Requires:	%{dridrivers}-swrast = %{EVRD}
Requires:	%{dridrivers}-virtio = %{EVRD}
%ifarch %{armx}
Requires:	%{dridrivers}-freedreno = %{EVRD}
%endif
Provides:	dri-drivers = %{EVRD}

%description -n %{dridrivers}
DRI and XvMC drivers.

%package -n	%{dridrivers}-radeon
Summary:	DRI Drivers for AMD/ATI Radeon graphics chipsets
Group:		System/Libraries
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2
Conflicts:	libva-vdpau-driver
%define __noautoreq '.*llvmradeon.*'

%description -n %{dridrivers}-radeon
DRI and XvMC drivers for AMD/ATI Radeon graphics chipsets

%package -n	%{dridrivers}-vmwgfx
Summary:	DRI Drivers for VMWare guest OS
Group:		System/Libraries
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2

%description -n %{dridrivers}-vmwgfx
DRI and XvMC drivers for VMWare guest Operating Systems.

%ifnarch %arm
%package -n	%{dridrivers}-intel
Summary:	DRI Drivers for Intel graphics chipsets
Group:		System/Libraries
Conflicts:	libva-vdpau-driver
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2

%description -n %{dridrivers}-intel
DRI and XvMC drivers for Intel graphics chipsets
%endif

%package -n	%{dridrivers}-nouveau
Summary:	DRI Drivers for NVIDIA graphics chipsets using the Nouveau driver
Group:		System/Libraries
Conflicts:	libva-vdpau-driver
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2

%description -n %{dridrivers}-nouveau
DRI and XvMC drivers for Nvidia graphics chipsets

%package -n	%{dridrivers}-swrast
Summary:	DRI Drivers for software rendering
Group:		System/Libraries
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2

%description -n %{dridrivers}-swrast
Generic DRI driver using CPU rendering

%package -n	%{dridrivers}-virtio
Summary:	DRI Drivers for virtual environments
Group:		System/Libraries
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2

%description -n %{dridrivers}-virtio
Generic DRI driver for virtual environments.

%ifarch %{armx}
%package -n	%{dridrivers}-freedreno
Summary:	DRI Drivers for software rendering
Group:		System/Libraries
Conflicts:	%{mklibname dri-drivers} < 9.1.0-0.20130130.2

%description -n %{dridrivers}-freedreno
DRI and XvMC drivers for Adreno graphics chipsets
%endif

%package -n	%{libosmesa}
Summary:	Mesa offscreen rendering library
Group:		System/Libraries

%description -n %{libosmesa}
Mesa offscreen rendering libraries for rendering OpenGL into
application-allocated blocks of memory.

%package -n	%{devosmesa}
Summary:	Development files for libosmesa
Group:		Development/C
Requires:	%{libosmesa} = %{version}-%{release}

%description -n %{devosmesa}
This package contains the headers needed to compile programs against
the Mesa offscreen rendering library.

%if %{with va}
%package -n	%{libvadrivers}
Summary:	Mesa libVA video acceleration drivers
Group:		System/Libraries

%description -n %{libvadrivers}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
libVA drivers for video acceleration
%endif

%package -n	%{libgl}
Summary:	Files for Mesa (GL and GLX libs)
Group:		System/Libraries
Suggests:	%{dridrivers} >= %{version}-%{release}
%if %{with tfloat}
Requires:	%mklibname txc-dxtn
%endif
Obsoletes:	%{_lib}mesagl1 < %{version}-%{release}
Requires:	%{_lib}udev1

%description -n %{libgl}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
GL and GLX parts.

%package -n	%{devgl}
Summary:	Development files for Mesa (OpenGL compatible 3D lib)
Group:		Development/C
%ifarch armv7hl
# This will allow to install proprietary libGL library for ie. imx
Requires:	libGL.so.%{glmajor}%{_arch_tag_suffix}
# This is to prevent older version of being installed to satisfy dependency
Conflicts:	%{libgl} < %{version}-%{release}
%else
Requires:	%{libgl} = %{version}-%{release}
%endif
Obsoletes:	%{_lib}mesagl1-devel < 8.0
Obsoletes:	%{_lib}gl1-devel < %{version}-%{release}

%description -n %{devgl}
This package contains the headers needed to compile Mesa programs.

%if %{with egl}
%package -n	%{libegl}
Summary:	Files for Mesa (EGL libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaegl1 < 8.0

%description -n %{libegl}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
EGL parts.

%package -n	%{devegl}
Summary:	Development files for Mesa (EGL libs)
Group:		Development/C
Requires:	%{libegl} = %{version}-%{release}
Obsoletes:	%{_lib}mesaegl1-devel < 8.0
Obsoletes:	%{_lib}egl1-devel < %{version}-%{release}

%description -n %{devegl}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
EGL development parts.
%endif

%package -n %{libglapi}
Summary:	Files for mesa (glapi libs)
Group:		System/Libraries

%description -n %{libglapi}
This package provides the glapi shared library used by gallium.

%package -n %{devglapi}
Summary:	Development files for glapi libs
Group:		Development/C
Requires:	%{libglapi} = %{version}-%{release}
Obsoletes:	%{_lib}glapi0-devel < %{version}-%{release}

%description -n %{devglapi}
This package contains the headers needed to compile programs against
the glapi shared library.

%if ! %{with bootstrap}
%package -n %{libxatracker}
Summary:	Files for mesa (xatracker libs)
Group:		System/Libraries

%description -n %{libxatracker}
This package provides the xatracker shared library used by gallium.
 
%package -n %{devxatracker}
Summary:	Development files for xatracker libs
Group:		Development/C
Requires:	%{libxatracker} = %{version}-%{release}

%description -n %{devxatracker}
This package contains the headers needed to compile programs against
the xatracker shared library.
%endif

%package -n %{libglesv1}
Summary:	Files for Mesa (glesv1 libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaglesv1_1 < 8.0

%description -n %{libglesv1}
OpenGL ES is a low-level, lightweight API for advanced embedded graphics using
well-defined subset profiles of OpenGL.

This package provides the OpenGL ES library version 1.

%package -n %{devglesv1}
Summary:	Development files for glesv1 libs
Group:		Development/C
Requires:	%{libglesv1} = %{version}-%{release}
Obsoletes:	%{_lib}mesaglesv1_1-devel < 8.0
Obsoletes:	%{_lib}glesv1_1-devel < %{version}-%{release}

%description -n %{devglesv1}
This package contains the headers needed to compile OpenGL ES 1 programs.

%package -n %{libglesv2}
Summary:	Files for Mesa (glesv2 libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaglesv2_2 < 8.0

%description -n %{libglesv2}
OpenGL ES is a low-level, lightweight API for advanced embedded graphics using
well-defined subset profiles of OpenGL.

This package provides the OpenGL ES library version 2.

%package -n %{devglesv2}
Summary:	Development files for glesv2 libs
Group:		Development/C
Requires:	%{libglesv2} = %{version}-%{release}
Obsoletes:	%{_lib}mesaglesv2_2-devel < 8.0
Obsoletes:	%{_lib}glesv2_2-devel < %{version}-%{release}

%description -n %{devglesv2}
This package contains the headers needed to compile OpenGL ES 2 programs.

%package -n %{devglesv3}
Summary:	Development files for glesv3 libs
Group:		Development/C
# there is no pkgconfig
Provides:	glesv3-devel = %{version}-%{release}

%description -n %{devglesv3}
This package contains the headers needed to compile OpenGL ES 3 programs.

%package -n %{libd3d}
Summary:	Mesa Gallium Direct3D 9 state tracker
Group:		System/Libraries

%description -n %{libd3d}
OpenGL ES is a low-level, lightweight API for advanced embedded graphics using
well-defined subset profiles of OpenGL.

This package provides Direct3D 9 support.

%package -n %{devd3d}
Summary:	Development files for Direct3D 9 libs
Group:		Development/C
Requires:	%{libd3d} = %{version}-%{release}
Provides:	d3d-devel = %{EVRD}

%description -n %{devd3d}
This package contains the headers needed to compile Direct3D 9 programs.

%package -n %{libopenvg}
Summary:	Files for MESA (OpenVG libs)
Group:		System/Libraries
Obsoletes:	%{_lib}mesaopenvg1 < 8.0

%description -n %{libopenvg}
OpenVG is a royalty-free, cross-platform API that provides a low-level hardware
acceleration interface for vector graphics libraries such as Flash and SVG.

%package -n %{devopenvg}
Summary:	Development files for OpenVG libs
Group:		Development/C
Requires:	%{libopenvg} = %{version}-%{release}
Requires:	%{devegl} = %{version}-%{release}
Obsoletes:	%{_lib}mesaopenvg1-devel < 8.0

%description -n %{devopenvg}
Development files for OpenVG library.

%if %{with opencl}
%package -n %{libcl}
Summary:	OpenCL libs
Group:		System/Libraries

%description -n %{libcl}
Open Computing Language (OpenCL) is a framework for writing programs that
execute across heterogeneous platforms consisting of central processing units
(CPUs), graphics processing units (GPUs), DSPs and other processors.

OpenCL includes a language (based on C99) for writing kernels (functions that
execute on OpenCL devices), plus application programming interfaces (APIs) that
are used to define and then control the platforms. OpenCL provides parallel
computing using task-based and data-based parallelism. OpenCL is an open
standard maintained by the non-profit technology consortium Khronos Group.
It has been adopted by Intel, Advanced Micro Devices, Nvidia, and ARM Holdings.

%package -n %{devcl}
Summary:	Development files for OpenCL libs
Group:		Development/Other
Requires:	%{libcl} = %{version}-%{release}
Provides:	%{clname}-devel = %{version}-%{release}

%description -n %{devcl}
Development files for the OpenCL library
%endif

%if %{with vdpau}
%package -n	%{_lib}vdpau-driver-nouveau
Summary:	VDPAU plugin for nouveau driver
Group:		System/Libraries
Requires:	%{_lib}vdpau1

%description -n %{_lib}vdpau-driver-nouveau
This packages provides a VPDAU plugin to enable video acceleration
with the nouveau driver.

%package -n	%{_lib}vdpau-driver-r300
Summary:	VDPAU plugin for r300 driver
Group:		System/Libraries
Requires:	%{_lib}vdpau1

%description -n %{_lib}vdpau-driver-r300
This packages provides a VPDAU plugin to enable video acceleration
with the r300 driver.

%package -n	%{_lib}vdpau-driver-r600
Summary:	VDPAU plugin for r600 driver
Group:		System/Libraries
Requires:	%{_lib}vdpau1

%description -n %{_lib}vdpau-driver-r600
This packages provides a VPDAU plugin to enable video acceleration
with the r600 driver.

%package -n	%{_lib}vdpau-driver-radeonsi
Summary:	VDPAU plugin for radeonsi driver
Group:		System/Libraries
Requires:	%{_lib}vdpau1

%description -n %{_lib}vdpau-driver-radeonsi
This packages provides a VPDAU plugin to enable video acceleration
with the radeonsi driver.

%package -n	%{_lib}vdpau-driver-softpipe
Summary:	VDPAU plugin for softpipe driver
Group:		System/Libraries
Requires:	%{_lib}vdpau1

%description -n %{_lib}vdpau-driver-softpipe
This packages provides a VPDAU plugin to enable video acceleration
with the softpipe driver.
%endif

%if %{with egl}
%package -n %{libgbm}
Summary:	Files for Mesa (gbm libs)
Group:		System/Libraries

%description -n %{libgbm}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
GBM (Graphics Buffer Manager) parts.

%package -n %{devgbm}
Summary:	Development files for Mesa (gbm libs)
Group:		Development/C
Requires:	%{libgbm} = %{version}-%{release}

%description -n %{devgbm}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
GBM (Graphics Buffer Manager) development parts.
%endif

%if %{with wayland}
%package -n %{libwaylandegl}
Summary:	Files for Mesa (Wayland EGL libs)
Group:		System/Libraries

%description -n %{libwaylandegl}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
Wayland EGL platform parts.

%package -n %{devwaylandegl}
Summary:	Development files for Mesa (Wayland EGL libs)
Group:		Development/C
Requires:	%{libwaylandegl} = %{version}-%{release}

%description -n %{devwaylandegl}
Mesa is an OpenGL %{opengl_ver} compatible 3D graphics library.
Wayland EGL platform development parts.
%endif

%package	common-devel
Summary:	Meta package for mesa devel
Group:		Development/C
Requires:	pkgconfig(glu)
Requires:	pkgconfig(glut)
Requires:	%{devgl} = %{version}-%{release}
Requires:	%{devegl} = %{version}-%{release}
Requires:	%{devglapi} = %{version}-%{release}
Requires:	%{devglesv1} = %{version}-%{release}
Requires:	%{devglesv2} = %{version}-%{release}
Suggests:	%{devd3d} = %{version}-%{release}

%description common-devel
Mesa common metapackage devel

%prep
%if "%{git}" != ""
%setup -qn %{name}-%{git_branch}-%{git}
%else
%setup -qn mesa-%{version}%{vsuffix}
%endif
sed -i -e 's,HAVE_COMPAT_SYMLINKS=yes,HAVE_COMPAT_SYMLINKS=no,g' configure.ac

%apply_patches
chmod +x %{SOURCE5}

#sed -i 's/CFLAGS="$CFLAGS -Werror=implicit-function-declaration"//g' configure.ac
#sed -i 's/CFLAGS="$CFLAGS -Werror=missing-prototypes"//g' configure.ac

autoreconf -vfi

# Duplicate source tree for OSMesa, since building both versions out-of-tree
# would break build. - Anssi 12/2012
all=$(ls)
mkdir -p build-osmesa
cp -a $all build-osmesa

%build
%if %{with gcc}
export CC=gcc
export CXX=g++
%endif
export CFLAGS="%{optflags} -fno-optimize-sibling-calls -Ofast"
export CXXFLAGS="%{optflags} -fno-optimize-sibling-calls -Ofast"
%ifarch x86_64
# Mesa uses SSSE3 asm instructions -- clang errors out if we don't allow them
# (tpg) disable for now
# see bug https://bugs.freedesktop.org/show_bug.cgi?id=93454
#export CFLAGS="$CFLAGS -mssse3"
#export CXXFLAGS="$CXXFLAGS -mssse3"
%endif

GALLIUM_DRIVERS="swrast,virgl"
%if %{with hardware}
GALLIUM_DRIVERS="$GALLIUM_DRIVERS,svga,r300,nouveau"
%if %{with r600}
GALLIUM_DRIVERS="$GALLIUM_DRIVERS,r600,radeonsi"
%endif
%if %{with intel}
# (tpg) i915 got removed as it does not load on wayland
# http://wayland.freedesktop.org/building.html
GALLIUM_DRIVERS="$GALLIUM_DRIVERS,ilo"
%endif
%ifarch %{armx}
GALLIUM_DRIVERS="$GALLIUM_DRIVERS,freedreno"
%endif
%endif

%configure \
	--enable-dri \
	--enable-dri3 \
	--enable-glx \
	--enable-glx-tls \
	--with-dri-driverdir=%{driver_dir} \
	--with-dri-drivers="%{dri_drivers}" \
%if %{with egl}
	--enable-egl \
	--enable-gbm \
	--enable-shared-glapi \
%else
	--disable-egl \
%endif
%if %{with wayland}
	--with-egl-platforms=x11,drm,wayland,surfaceless \
%else
	--with-egl-platforms=x11,drm,surfaceless \
%endif
	--enable-gles1 \
	--enable-gles2 \
%if %{with openvg}
	--enable-openvg \
%endif
%if %{with opencl}
	--enable-opencl \
%endif
	--enable-xvmc \
%if %{with vdpau}
	--enable-vdpau \
%else
	--disable-vdpau \
%endif
%if %{with va}
	--enable-va \
%else
	--disable-va \
%endif
%if %{with hardware}
	--with-gallium-drivers=$GALLIUM_DRIVERS \
%if ! %{with bootstrap}
	--enable-xa \
%endif
	--enable-nine \
	--enable-gallium-llvm \
	--enable-llvm-shared-libs \
%else
	--disable-gallium-llvm \
	--with-gallium-drivers=swrast \
%endif
%if %{with tfloat}
	--enable-texture-float  \
%endif
	# end of configure options

# Build OSMesa separately, since we want to build OSMesa without shared-glapi,
# since doing that causes OSMesa to miss the OpenGL symbols.
# See e.g. https://bugs.launchpad.net/ubuntu/+source/mesa/+bug/1066599
# -Anssi 12/2012

pushd build-osmesa
%configure \
	--enable-osmesa \
	--disable-dri \
	--disable-glx \
	--disable-egl \
	--disable-shared-glapi \
	--disable-gles1 \
	--disable-gles2 \
	--without-gallium-drivers
popd

%make
%ifarch i686
%make -C build-osmesa OSMESA_LIB_DEPS="-ldl -lpthread -L%{_libdir}/clang/$(clang --version |head -n1 |awk '{print $3;}')/lib/linux -lclang_rt.builtins-i686"
%else
%ifarch %{ix86}
%make -C build-osmesa OSMESA_LIB_DEPS="-ldl -lpthread -L%{_libdir}/clang/$(clang --version |head -n1 |awk '{print $3;}')/lib/linux -lclang_rt.builtins-i386"
%else
%make -C build-osmesa
%endif
%endif

%install
%makeinstall_std -C build-osmesa
%makeinstall_std

# FIXME: strip will likely break the hardlink
# (blino) hardlink libGL files in %{_libdir}/mesa
# to prevent proprietary driver installers from removing them
mkdir -p %{buildroot}%{_libdir}/mesa
pushd %{buildroot}%{_libdir}/mesa
for l in ../libGL.so.*; do cp -a $l .; done
popd

%ifarch armv7hl
ln -sf libGL.so.%{glmajor} %{buildroot}%{_libdir}/libGL.so
%endif

%ifarch %{x86_64}
mkdir -p %{buildroot}%{_prefix}/lib/dri
%endif

# .so files are not needed by vdpau
rm -f %{buildroot}%{_libdir}/vdpau/libvdpau_*.so

# .la files are not needed by mesa
find %{buildroot} -name '*.la' |xargs rm -f

# use swrastg if built (Anssi 12/2011)
[ -e %{buildroot}%{_libdir}/dri/swrastg_dri.so ] && mv %{buildroot}%{_libdir}/dri/swrast{g,}_dri.so


%files
%doc docs/README.*
%config(noreplace) %{_sysconfdir}/drirc

%files -n %{dridrivers}

%files -n %{dridrivers}-radeon
%{_libdir}/dri/r?00_dri.so
%{_libdir}/dri/radeon_dri.so
%{_libdir}/gallium-pipe/pipe_r?00.so
%if %{with r600}
%{_libdir}/dri/r600_drv_video.so
%{_libdir}/libXvMCr?00.so.*
%{_libdir}/dri/radeonsi_dri.so
%{_libdir}/dri/radeonsi_drv_video.so
%{_libdir}/gallium-pipe/pipe_radeonsi.so
%endif

%files -n %{dridrivers}-vmwgfx
%{_libdir}/dri/vmwgfx_dri.so
%{_libdir}/gallium-pipe/pipe_vmwgfx.so

%ifnarch %{armx}
%files -n %{dridrivers}-intel
%{_libdir}/dri/i9?5_dri.so
%{_libdir}/dri/ilo_dri.so
%{_libdir}/gallium-pipe/pipe_i9?5.so
%endif

%files -n %{dridrivers}-nouveau
%{_libdir}/dri/nouveau*_dri.so
%{_libdir}/dri/nouveau_drv_video.so
%{_libdir}/gallium-pipe/pipe_nouveau.so
%{_libdir}/libXvMCnouveau.so.*

%files -n %{dridrivers}-swrast
%{_libdir}/dri/swrast_dri.so
%{_libdir}/dri/kms_swrast_dri.so
%{_libdir}/gallium-pipe/pipe_swrast.so

%files -n %{dridrivers}-virtio
%{_libdir}/dri/virtio_gpu_dri.so

%ifarch %{armx}
%files -n %{dridrivers}-freedreno
%{_libdir}/dri/kgsl_dri.so
%{_libdir}/dri/msm_dri.so
%{_libdir}/gallium-pipe/pipe_msm.so
%endif

%files -n %{libosmesa}
%{_libdir}/libOSMesa.so.%{osmesamajor}*

%files -n %{devosmesa}
%dir %{_includedir}/GL
%{_includedir}/GL/osmesa.h
%{_libdir}/libOSMesa.so
%{_libdir}/pkgconfig/osmesa.pc

%if %{with va}
%files -n %{libvadrivers}
%endif

%files -n %{libgl}
%{_libdir}/libGL.so.*
%dir %{_libdir}/mesa
%{_libdir}/mesa/libGL.so.%{glmajor}*
%dir %{_libdir}/dri
%dir %{_libdir}/gallium-pipe

%if %{with egl}
%files -n %{libegl}
%{_libdir}/libEGL.so.%{eglmajor}*
%endif

%files -n %{libglapi}
%{_libdir}/libglapi.so.%{glapimajor}*

%if ! %{with bootstrap}
%files -n %{libxatracker}
%{_libdir}/libxatracker.so.%{xatrackermajor}*
%endif

%files -n %{libglesv1}
%{_libdir}/libGLESv1_CM.so.%{glesv1major}*

%files -n %{libglesv2}
%{_libdir}/libGLESv2.so.%{glesv2major}*

%files -n %{libd3d}
%dir %{_libdir}/d3d
%{_libdir}/d3d/d3dadapter9.so.%{d3dmajor}*

%if %{with openvg}
%files -n %{libopenvg}
%{_libdir}/libOpenVG.so.%{openvgmajor}*
%endif

%if %{with opencl}
%files -n %{libcl}
%{_libdir}/libOpenCL.so.%{clmajor}*
%endif

%if %{with egl}
%files -n %{libgbm}
%{_libdir}/libgbm.so.%{gbmmajor}*
%endif

%if %{with wayland}
%files -n %{libwaylandegl}
%{_libdir}/libwayland-egl.so.%{waylandeglmajor}*
%endif

%files -n %{devgl}
%dir %{_includedir}/GL
%{_includedir}/GL/gl.h
%{_includedir}/GL/glcorearb.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/gl_mangle.h
%{_includedir}/GL/wglext.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glxext.h
%{_includedir}/GL/glx_mangle.h
%{_includedir}/GL/mesa_glinterop.h
%{_libdir}/libGL.so
%{_libdir}/libXvMC*.so
%{_libdir}/pkgconfig/gl.pc
%{_libdir}/pkgconfig/dri.pc

#FIXME: check those headers
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h

%files common-devel
# meta devel pkg

%if %{with egl}
%files -n %{devegl}
%{_includedir}/EGL
%{_includedir}/KHR
%{_libdir}/libEGL.so
%{_libdir}/pkgconfig/egl.pc
%endif

%files -n %{devglapi}
%{_libdir}/libglapi.so

#vdpau enblaed
%if %{with vdpau}
%files -n %{_lib}vdpau-driver-nouveau
%{_libdir}/vdpau/libvdpau_nouveau.so.*

%files -n %{_lib}vdpau-driver-r300
%{_libdir}/vdpau/libvdpau_r300.so.*

%if %{with r600}
%files -n %{_lib}vdpau-driver-r600
%{_libdir}/vdpau/libvdpau_r600.so.*

%files -n %{_lib}vdpau-driver-radeonsi
%{_libdir}/vdpau/libvdpau_radeonsi.so.*
%endif

%files -n %{_lib}vdpau-driver-softpipe
%endif

%if ! %{with bootstrap}
%files -n %{devxatracker}
%{_libdir}/libxatracker.so
%{_includedir}/xa_*.h
%{_libdir}/pkgconfig/xatracker.pc
%endif

%files -n %{devglesv1}
%{_includedir}/GLES
%{_libdir}/libGLESv1_CM.so
%{_libdir}/pkgconfig/glesv1_cm.pc

%files -n %{devglesv2}
%{_includedir}/GLES2
%{_libdir}/libGLESv2.so
%{_libdir}/pkgconfig/glesv2.pc

%files -n %{devglesv3}
%{_includedir}/GLES3

%files -n %{devd3d}
%{_includedir}/d3dadapter
%{_libdir}/d3d/d3dadapter9.so
%{_libdir}/pkgconfig/d3d.pc

%if %{with openvg}
%files -n %{devopenvg}
%{_includedir}/VG
%{_libdir}/libOpenVG.so
%{_libdir}/pkgconfig/vg.pc
%endif

%if %{with opencl}
%files -n %{devcl}
%{_includedir}/CL
%{_libdir}/libOpenCL.so
%endif

%if %{with egl}
%files -n %{devgbm}
%{_includedir}/gbm.h
%{_libdir}/libgbm.so
%{_libdir}/pkgconfig/gbm.pc
%endif

%if %{with wayland}
%files -n %{devwaylandegl}
%{_libdir}/libwayland-egl.so
%{_libdir}/pkgconfig/wayland-egl.pc
%endif
