# (cg) Cheater...
%define Werror_cflags %nil

# (aco) Needed for the dri drivers
%define _disable_ld_no_undefined 1

%define git 0
%define relc			0
%define	name			mesa
%define version			7.9
%define rel			1

%define release			%mkrel %{rel}
%define src_type tar.bz2
%define vsuffix			%{expand:}

%if %{relc}
%define release			%mkrel 0.rc%{relc}.%{rel}
%define vsuffix -rc%{relc}
%define src_type tar.bz2
%endif

%if %{git}
%if %{relc}
%define release			%mkrel 0.rc%{relc}.2.git%{git}.%{rel}
%else
%define release			%mkrel 0.git%{git}.%{rel}
%endif
%endif

%define makedepend		%{_bindir}/gccmakedep

%define eglname			mesaegl
%define glname			mesagl
%define gluname			mesaglu
%define glutname		mesaglut
%define glwname			mesaglw
%define eglmajor		1
%define glmajor			1
%define glumajor		1
%define glutmajor		3
%define glwmajor		1
%define libeglname              %mklibname %{eglname} %{eglmajor}
%define libglname		%mklibname %{glname} %{glmajor}
%define libgluname		%mklibname %{gluname} %{glumajor}
%define libglutname		%mklibname %{glutname} %{glutmajor}
%define libglwname		%mklibname %{glwname} %{glwmajor}

%define dridrivers		%mklibname dri-drivers

# Architecture-independent Virtual provides:
%define libeglname_virt		lib%{eglname}
%define libglname_virt		lib%{glname}
%define libgluname_virt		lib%{gluname}
%define libglutname_virt	lib%{glutname}
%define libglwname_virt		lib%{glwname}

%define oldlibglname		%mklibname MesaGL 1
%define oldlibgluname		%mklibname MesaGLU 1
%define oldlibglutname		%mklibname Mesaglut 3

%define mesasrcdir		%{_prefix}/src/Mesa/
%define driver_dir		%{_libdir}/dri

%define enable_egl		0

#FIXME: (for 386/485) unset SSE, MMX and 3dnow flags
#FIXME: (for >=i586)  disable sse
#       SSE seems to have problem on some apps (gtulpas) for probing.
%define	dri_drivers_i386	"i810,i915,i965,mga,mach64,nouveau,r128,r200,r300,r600,radeon,savage,sis,unichrome,tdfx,swrast"
%define	dri_drivers_x86_64	%{dri_drivers_i386}
%define	dri_drivers_ppc		"mach64,r128,r200,r300,radeon,tdfx,swrast"
%define	dri_drivers_ppc64	""
%define	dri_drivers_ia64	"i810,i915,i965,mga,r128,r200,radeon,swrast"
%define	dri_drivers_alpha	"mga,r128,r200,radeon,swrast"
%define	dri_drivers_sparc	"ffb,mach64,mga,radeon,savage,swrast"
%define dri_drivers_mipsel	"mach64,mga,r128,r200,radeon,savage,tdfx"
%define	dri_drivers		%{expand:%{dri_drivers_%{_arch}}}

Name:		%{name}
Version: 	%{version}
Release: 	%{release}
Summary:	OpenGL 2.1 compatible 3D graphics library
Group:		System/Libraries

BuildRequires:	tcl
BuildRequires:	texinfo
BuildRequires:	libxfixes-devel		>= 4.0.3
BuildRequires:	libxt-devel		>= 1.0.5
BuildRequires:	libxmu-devel		>= 1.0.3
BuildRequires:	libx11-devel		>= 1.3.3
BuildRequires:	libxdamage-devel	>= 1.1.1
BuildRequires:	libexpat-devel		>= 2.0.1
BuildRequires:	gccmakedep
BuildRequires:	x11-proto-devel		>= 7.3
BuildRequires:	libdrm-devel		>= 2.4.21

BuildRequires:	libxext-devel		>= 1.1.1
BuildRequires:	libxxf86vm-devel	>= 1.1.0
BuildRequires:	libxi-devel		>= 1.3
BuildRequires:	talloc-devel libxml2-python

BuildRequires:	libglew-devel
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot
URL:		http://www.mesa3d.org
%if %{git}
# (cg) Current commit ref: origin/mesa_7_5_branch
Source0:	%{name}-%{git}.tar.bz2
%else
Source0:	ftp://ftp.freedesktop.org/pub/mesa/%version/MesaLib-%{version}%{vsuffix}.%{src_type}
Source2:	ftp://ftp.freedesktop.org/pub/mesa/%version/MesaGLUT-%{version}%{vsuffix}.%{src_type}
%endif
Source3:	make-git-snapshot.sh
Source5:	mesa-driver-install


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
Patch201: 0201-revert-fix-glxinitializevisualconfigfromtags-handling.patch

# Patches "liberated" from Fedora: 
# http://cvs.fedoraproject.org/viewvc/rpms/mesa/devel/
# git format-patch --start-number 300 mdv-cherry-picks..mdv-redhat
Patch300: 0300-RH-mesa-7.1-nukeglthread-debug-v1.1.patch
Patch301: 0301-RH-mesa-7.1-link-shared-v1.7.patch

# Mandriva patches
# git format-patch --start-number 900 mdv-redhat..mdv-patches
Patch902: 0902-remove-unfinished-GLX_ARB_render_texture.patch
Patch903: 0903-Fix-NULL-pointer-dereference-in-viaXMesaWindowMoved.patch

Patch2004:     mesa_652_mips.patch

License:	MIT
Requires:	%{libglname} = %{version}-%{release}
Provides:	hackMesa = %{version}
Obsoletes:	hackMesa <= %{version}
Provides:	Mesa = %{version}
Obsoletes:	Mesa < %{version}

%if %{enable_egl}
%package -n	%{libeglname}
Summary:	Files for Mesa (EGL libs)
Group:		System/Libraries
Provides:	%{libeglname_virt} = %{version}-%{release}

%package -n	%{libeglname}-devel
Summary:	Development files for Mesa (EGL libs)
Group:		Development/C
Requires:	%{name} = %{version}
Provides:	EGL-devel
%endif

%package -n	%{libglname}
Summary:	Files for Mesa (GL and GLX libs)
Group:		System/Libraries
Obsoletes:	%{oldlibglname} < 6.4 
Provides:	%{oldlibglname} = %{version}-%{release}
Provides:	%{libglname_virt} = %{version}-%{release}
Requires:	%{dridrivers} >= %{version}-%{release}

# (anssi) Forces the upgrade of x11-server-common to happen before
# alternatives removal, which allows x11-server-common to grab the symlink.
Conflicts:	x11-server-common < 1.3.0.0-17

%package -n	%{dridrivers}
Summary:	Mesa DRI drivers
Group:		System/Libraries
Conflicts:	%{_lib}MesaGL1 < 7.7-5

%package -n	%{dridrivers}-experimental
Summary:	Mesa DRI - unstable experimental drivers
Group:		System/Libraries
# for dri driver directory
Requires:       %{dridrivers}

%package -n	%{libglname}-devel
Summary:	Development files for Mesa (OpenGL compatible 3D lib)
Group:		Development/C
Requires:	%{name} = %{version}
# (gc) /usr/lib/pkgconfig/glut.pc depends on /usr/lib/pkgconfig/{x11,xmu,xi}.pc (Requires.private) and pkg-config --list-all
# goes wild without these deps
Requires:	libx11-devel libxmu-devel libxi-devel
Provides:	lib%{glname}-devel = %{version}-%{release}
Provides:	%{glname}-devel = %{version}-%{release}
Provides:	GL-devel
Obsoletes:	%{oldlibglname}-devel < 6.4
Provides:	%{oldlibglname}-devel = %{version}-%{release}
Provides:	libMesaGL-devel = %{version}-%{release}
Provides:	MesaGL-devel = %{version}-%{release}

%package -n	%{libgluname}
Summary:	Files for Mesa (GLU libs)
Group:		System/Libraries
Obsoletes:	%{oldlibgluname} < 6.4
Provides:	%{oldlibgluname} = %{version}-%{release}
Provides:	%{libgluname_virt} = %{version}-%{release}

%package -n	%{libgluname}-devel
Summary:	Development files for GLU libs
Group:		Development/C
Requires:	%{libgluname} = %{version}-%{release}
Provides:	lib%{gluname}-devel = %{version}-%{release}
Provides:	%{gluname}-devel = %{version}-%{release}
Obsoletes:	%{oldlibgluname}-devel < 6.4
Provides:	%{oldlibgluname}-devel = %{version}-%{release}
Provides:	libMesaGLU-devel = %{version}-%{release}
Provides:	MesaGLU-devel = %{version}-%{release} 

%package -n	%{libglutname}
Summary:	Files for Mesa (glut libs)
Group:		System/Libraries
Requires:	%{libgluname} = %{version}-%{release}
Provides:	Mesa-common = %{version}-%{release} hackMesa-common = %{version}
Obsoletes:	Mesa-common <= %{version} hackMesa-common <= %{version}
Obsoletes:	%{oldlibglutname} < 6.4
Provides:	%{oldlibglutname} = %{version}-%{release}
Provides:	%{libglutname_virt} = %{version}-%{release}

%package -n	%{libglutname}-devel
Summary:	Development files for glut libs
Group:		Development/C
Requires:	%{libglutname} = %{version}-%{release} %{libgluname}-devel = %{version}-%{release}
Provides:	lib%{glutname}-devel = %{version}-%{release} 
Provides:	%{glutname}-devel = %{version}-%{release} 
Obsoletes:	%{oldlibglutname}-devel < 6.4
Provides:	%{oldlibglutname}-devel = %{version}-%{release}
Provides:	libMesaGLUT-devel = %{version}-%{release}
Provides:	MesaGLUT-devel = %{version}-%{release}

%package -n	%{libglwname}
Summary:	Files for Mesa (glw libs)
Group:		System/Libraries
Provides:	Mesa-common = %{version}-%{release} hackMesa-common = %{version}
Obsoletes:	Mesa-common <= %{version} hackMesa-common <= %{version}
Provides:	%{libglwname_virt} = %{version}-%{release}

%package -n	%{libglwname}-devel
Summary:	Development files for glw libs
Group:		Development/C
Requires:	%{libglwname} = %{version}-%{release}
Provides:	lib%{glwname}-devel = %{version}-%{release} 
Provides:	%{glwname}-devel = %{version}-%{release} 

%package	common-devel
Summary:	Meta package for mesa devel
Group:		Development/C
Provides:	Mesa-common-devel = %{version}-%{release} 
Provides:	hackMesa-common-devel = %{version}
Obsoletes:	Mesa-common-devel < %{version} 
Obsoletes:	hackMesa-common-devel < %{version}
Requires:	%{libglname}-devel = %{version}
Requires:	%{libglwname}-devel = %{version}
Requires:	%{libgluname}-devel = %{version}
Requires:	%{libglutname}-devel = %{version}


%description
Mesa is an OpenGL 2.1 compatible 3D graphics library.

%description common-devel
Mesa common metapackage devel

%if %{enable_egl}
%description -n	%{libeglname}
Mesa is an OpenGL 2.1 compatible 3D graphics library.
EGL parts.

%description -n	%{libeglname}-devel
Mesa is an OpenGL 2.1 compatible 3D graphics library.
EGL development parts.
%endif

%description -n	%{libglname}
Mesa is an OpenGL 2.1 compatible 3D graphics library.
GL and GLX parts.

%description -n %{dridrivers}
Mesa is an OpenGL 2.1 compatible 3D graphics library.
DRI drivers.

%description -n %{dridrivers}-experimental
Mesa is an OpenGL 2.1 compatible 3D graphics library.
Experimental unstable DRI drivers.

This package contains experimental DRI drivers for NVIDIA cards, for
OpenGL acceleration with nouveau driver. These drivers are not stable
and may crash your system. Please do not report bugs encountered with
these drivers.

%description -n	%{libglname}-devel
Mesa is an OpenGL 2.1 compatible 3D graphics library.

This package contains the headers needed to compile Mesa programs.

%description -n	%{libgluname}
GLU is the OpenGL Utility Library.
It provides a number of functions upon the base OpenGL library to provide
higher-level drawing routines from the more primitive routines provided by
OpenGL.

%description -n	%{libgluname}-devel
This package contains the headers needed to compile programs with GLU.

%description -n	%{libglutname}
GLUT (OpenGL Utility Toolkit) is a addon library for OpenGL programs. It
provides them utilities to define and control windows, input from the keyboard
and the mouse, drawing some geometric primitives (cubes, spheres, ...).
GLUT can even create pop-up windows.

%description -n	%{libglutname}-devel
Mesa is an OpenGL 2.1 compatible 3D graphics library.
glut parts.

This package contains the headers needed to compile Mesa programs.

%description -n	%{libglwname}
GLw adds Motif bindings to the OpenGL "canvas" (Xt/Motif/OpenGL widget code).

%description -n	%{libglwname}-devel
Mesa is an OpenGL 2.1 compatible 3D graphics library.
GLw parts.

This package contains the headers needed to compile Mesa programs.

%prep
%if %{git}
%setup -q -n mesa-%{git}
%else
%setup -q -n Mesa-%{version}%{vsuffix} -b2
%endif

%patch201 -p1

%patch300 -p1
## (Anssi 03/2010) FIXME: Currently results in either missing NEEDED tag or
## NEEDED tag with '../../../../../lib/libdricore.so', while NEEDED tag of libdricore.so
## is wanted.
#%patch301 -p1

%patch902 -p1
%patch903 -p1

%patch2004 -p1

%if %{enable_egl}
# (cg) Need to fix this post 7.4.1 - patch not yet migrated
#patch1001 -p1
%endif

chmod +x %{SOURCE5}

# for dri-drivers-experimental
cat > README.install.urpmi <<EOF
This package contains experimental DRI drivers for NVIDIA cards, for
OpenGL acceleration with nouveau driver. These drivers are not stable
and may crash your system. Please do not report bugs encountered with
these drivers.
EOF

%build
#%if %{git}
#./autogen.sh -v
#%endif

# Required by patch200:
autoreconf -vfi

LIB_DIR=%{_lib}
INCLUDE_DIR=$RPM_BUILD_ROOT%{_includedir}
DRI_DRIVER_DIR="%{driver_dir}"
export LIB_DIR INCLUDE_DIR DRI_DRIVER_DIR

%configure2_5x	--with-driver=dri \
		--with-dri-driverdir=%{driver_dir} \
		--with-dri-drivers="%{dri_drivers}" \
                --with-state-trackers=dri \
                --enable-gallium-nouveau \
%if %{enable_egl}
		--enable-egl \
%else
		--disable-egl \
%endif
		--with-demos

# (cg) Parallel build breaks the dricore shared stuff.
make -j 1

%install
rm -rf %{buildroot}
make DESTDIR=$RPM_BUILD_ROOT install

mkdir -p $RPM_BUILD_ROOT%{_bindir}


# (blino) hardlink libGL files in %{_libdir}/mesa
# to prevent proprietary driver installers from removing them
mkdir -p $RPM_BUILD_ROOT%{_libdir}/mesa
pushd $RPM_BUILD_ROOT%{_libdir}/mesa
for l in ../libGL.so.*; do cp -a $l .; done
popd

# clean any .la file with still reference to tmppath.
perl -pi -e "s|\S+$RPM_BUILD_DIR\S*||g" $RPM_BUILD_ROOT/%{_libdir}/*.la

%ifarch %{x86_64}
mkdir -p $RPM_BUILD_ROOT%{_prefix}/lib/dri
%endif

# (cg) I'm not really sure about these files, but they do conflict in some capacity so I'll
#      just trash them for now.
rm -f $RPM_BUILD_ROOT%{_includedir}/GL/{glew,glxew,wglew}.h

%clean
rm -fr $RPM_BUILD_ROOT

%if %{enable_egl}
%if %mdkversion < 200900
%post -n %{libeglname} -p /sbin/ldconfig
%endif
%if %mdkversion < 200900
%postun -n %{libeglname} -p /sbin/ldconfig
%endif
%endif

%if %mdkversion < 200900
%post -n %{libglname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%postun -n %{libglname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libgluname} -p /sbin/ldconfig 
%endif

%if %mdkversion < 200900
%postun -n %{libgluname} -p /sbin/ldconfig
%endif

%if %mdkversion < 200900
%post -n %{libglutname} -p /sbin/ldconfig 
%endif

%if %mdkversion < 200900
%postun -n %{libglutname} -p /sbin/ldconfig
%endif

%files
%defattr(-,root,root)
%doc docs/COPYING docs/README.*

%if %{enable_egl}
%files -n %{libeglname}
%defattr(-,root,root)
%{_libdir}/libEGL.so.1*
%{_libdir}/libegldri.so.1*

%files -n %{libeglname}-devel
%defattr(-,root,root)
%{_libdir}/libEGL.so
%{_libdir}/libegldri.so
%{_includedir}/gles/egl*.h
%endif

%files -n %{libglname}
%defattr(-,root,root)
%doc docs/COPYING
%{_libdir}/libGL.so.*
%dir %{_libdir}/mesa
%{_libdir}/mesa/libGL.so.*

%files -n %{dridrivers}
%defattr(-,root,root)
%doc docs/COPYING
%ifnarch ppc64
%dir %{_libdir}/dri
#%{_libdir}/dri/libdricore.so
%{_libdir}/dri/*_dri.so
%exclude %{_libdir}/dri/nouveau_dri.so
%exclude %{_libdir}/dri/nouveau_vieux_dri.so
%endif

%files -n %{dridrivers}-experimental
%defattr(-,root,root)
%doc docs/COPYING
%doc README.install.urpmi
%{_libdir}/dri/nouveau_dri.so
%{_libdir}/dri/nouveau_vieux_dri.so

%files -n %{libglname}-devel
%defattr(-,root,root)
%doc docs/COPYING
%{_includedir}/GL/gl.h
%{_includedir}/GL/glext.h
%{_includedir}/GL/gl_mangle.h
%{_includedir}/GL/osmesa.h
%{_includedir}/GL/wglext.h
%{_includedir}/GL/glx.h
%{_includedir}/GL/glxext.h
%{_includedir}/GL/glx_mangle.h
%{_libdir}/libGL.so
%_libdir/pkgconfig/*.pc

#FIXME: check those headers
%{_includedir}/GL/glfbdev.h
%{_includedir}/GL/vms_x_fix.h
%{_includedir}/GL/wmesa.h
%dir %{_includedir}/GL/internal
%{_includedir}/GL/internal/dri_interface.h

%files -n %{libgluname}
%defattr(-,root,root)
%doc docs/COPYING
%{_libdir}/libGLU.so.*

%files -n %{libglutname}
%defattr(-,root,root)
%doc docs/COPYING
%{_libdir}/libglut.so.*

%files -n %{libglwname}
%defattr(-,root,root)
%doc docs/COPYING
%{_libdir}/libGLw.so.*


%files -n %{libgluname}-devel
%defattr(-,root,root)
%doc docs/COPYING
%{_includedir}/GL/glu.h
%{_includedir}/GL/glu_mangle.h
%{_includedir}/GL/mesa_wgl.h
%{_libdir}/libGLU.so

%files -n %{libglutname}-devel
%defattr(-,root,root)
%doc docs/COPYING
%{_includedir}/GL/glut.h
%{_includedir}/GL/glutf90.h
%{_libdir}/libglut.so

%files common-devel
%defattr(-,root,root)

%files -n %{libglwname}-devel
%defattr(-,root,root)
%doc docs/COPYING
%{_includedir}/GL/GLwDrawA.h
%{_includedir}/GL/GLwDrawAP.h
%{_includedir}/GL/GLwMDrawA.h
%{_includedir}/GL/GLwMDrawAP.h
%{_libdir}/libGLw.so

