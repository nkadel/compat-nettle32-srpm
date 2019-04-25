Name:           compat-nettle32
Version:        3.2
Release:        0.3%{?dist}
Summary:        A low-level cryptographic library

Group:          Development/Libraries
License:        LGPLv3+ or GPLv2+
URL:            http://www.lysator.liu.se/~nisse/nettle/
#Source0:        http://www.lysator.liu.se/~nisse/archive/%%{name}-%%{version}.tar.gz
Source0:	https://src.fedoraproject.org/lookaside/pkgs/nettle/nettle-%{version}-hobbled.tar.xz
Patch0:		nettle-3.1.1-remove-ecc-testsuite.patch
Patch1:		nettle-3.2-version-h.patch

BuildRequires:  gmp-devel m4 texinfo-tex
BuildRequires:	libtool, automake, autoconf, gettext-devel

Requires(post): info
Requires(preun): info


%package devel
Summary:        Development headers for a low-level cryptographic library
Group:          Development/Libraries
Requires:       %{name} = %{version}-%{release}
Requires:       gmp-devel%{?_isa}
Conflicts:      nettle-devel

%description
Nettle is a cryptographic library that is designed to fit easily in more
or less any context: In crypto toolkits for object-oriented languages
(C++, Python, Pike, ...), in applications like LSH or GNUPG, or even in
kernel space.

%description devel
Nettle is a cryptographic library that is designed to fit easily in more
or less any context: In crypto toolkits for object-oriented languages
(C++, Python, Pike, ...), in applications like LSH or GNUPG, or even in
kernel space.  This package contains the files needed for developing 
applications with nettle.


%prep
%setup -q -n nettle-%{version}
# Disable -ggdb3 which makes debugedit unhappy
sed s/ggdb3/g/ -i configure
sed 's/ecc-192.c//g' -i Makefile.in
sed 's/ecc-224.c//g' -i Makefile.in
%patch0 -p1
%patch1 -p1

%build
autoreconf -ifv
%configure --enable-shared --disable-arm-neon --enable-fat
%make_build


%install
make install DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
make install-shared DESTDIR=$RPM_BUILD_ROOT INSTALL="install -p"
#mkdir -p $RPM_BUILD_ROOT%{_infodir}
#install -p -m 644 nettle.info $RPM_BUILD_ROOT%{_infodir}/nettle-3.2.info
rm -f $RPM_BUILD_ROOT%{_libdir}/*.a
rm -f $RPM_BUILD_ROOT%{_infodir}/dir
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/libnettle.so.6.*
chmod 0755 $RPM_BUILD_ROOT%{_libdir}/libhogweed.so.4.*

# Rename some files to avoid conflicts with base packages
mv $RPM_BUILD_ROOT%{_infodir}/nettle.info $RPM_BUILD_ROOT%{_infodir}/nettle-3.2.info
mv $RPM_BUILD_ROOT%{_bindir}/nettle-lfib-stream $RPM_BUILD_ROOT%{_bindir}/nettle-lfib-stream-3.2
mv $RPM_BUILD_ROOT%{_bindir}/pkcs1-conv $RPM_BUILD_ROOT%{_bindir}/pkcs1-conv-3.2
mv $RPM_BUILD_ROOT%{_bindir}/sexp-conv $RPM_BUILD_ROOT%{_bindir}/sexp-conv-3.2
mv $RPM_BUILD_ROOT%{_bindir}/nettle-hash $RPM_BUILD_ROOT%{_bindir}/nettle-hash-3.2
mv $RPM_BUILD_ROOT%{_bindir}/nettle-pbkdf2 $RPM_BUILD_ROOT%{_bindir}/nettle-pbkdf2-3.2

mkdir -p $RPM_BUILD_ROOT%{_includedir}/%{name}
mv $RPM_BUILD_ROOT%{_includedir}/nettle $RPM_BUILD_ROOT%{_includedir}/%{name}/
mkdir -p $RPM_BUILD_ROOT%{_libdir}/%{name}/pkgconfig/
#mv $RPM_BUILD_ROOT%{_libdir}/libnettle.so $RPM_BUILD_ROOT%{_libdir}/%{name}
#mv $RPM_BUILD_ROOT%{_libdir}/libhogweed.so $RPM_BUILD_ROOT%{_libdir}/%{name}
mv $RPM_BUILD_ROOT%{_libdir}/pkgconfig/nettle.pc $RPM_BUILD_ROOT%{_libdir}/%{name}/pkgconfig/
mv $RPM_BUILD_ROOT%{_libdir}/pkgconfig/hogweed.pc $RPM_BUILD_ROOT%{_libdir}/%{name}/pkgconfig/
sed -r -i 's#^(includedir=.*)#\1/%{name}#' $RPM_BUILD_ROOT%{_libdir}/%{name}/pkgconfig/nettle.pc
sed -r -i 's#^(includedir=.*)#\1/%{name}#' $RPM_BUILD_ROOT%{_libdir}/%{name}/pkgconfig/hogweed.pc
#sed -r -i 's#^(libdir=.*)#\1/%{name}#' $RPM_BUILD_ROOT%{_libdir}/%{name}/pkgconfig/nettle.pc
#sed -r -i 's#^(libdir=.*)#\1/%{name}#' $RPM_BUILD_ROOT%{_libdir}/%{name}/pkgconfig/hogweed.pc

%check
make check

%files
%doc AUTHORS NEWS README TODO
%license COPYINGv2 COPYING.LESSERv3
%{_infodir}/nettle-3.2.info.gz
%{_bindir}/nettle-lfib-stream-3.2
%{_bindir}/pkcs1-conv-3.2
%{_bindir}/sexp-conv-3.2
%{_bindir}/nettle-hash-3.2
%{_bindir}/nettle-pbkdf2-3.2
%{_libdir}/libnettle.so.6
%{_libdir}/libnettle.so.6.*
%{_libdir}/libhogweed.so.4
%{_libdir}/libhogweed.so.4.*

%files devel
%doc descore.README nettle.html nettle.pdf
%{_includedir}/%{name}/nettle
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/pkgconfig
%{_libdir}/%{name}/pkgconfig/*.pc
%{_libdir}/lib*.so

%post
/sbin/install-info %{_infodir}/nettle-3.2.info %{_infodir}/dir || :
/sbin/ldconfig

%preun
if [ $1 = 0 ]; then
  /sbin/install-info --delete %{_infodir}/nettle-3.2.info %{_infodir}/dir || :
fi

%postun -p /sbin/ldconfig



%changelog
* Thu Apr 25 2019 Nico Kadel-Garcia <nkadel@gmail.com> - 3.2-0.3
- Conflict with nettle-devel

* Fri Jul 29 2016 Nikos Mavrogiannopoulos <nmav@redhat.com> - 3.2-2
- Imported nettle 3.2 from fedora 24.

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Wed Feb 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.15-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Thu Apr 10 2008 Ian Weller <ianweller@gmail.com> 1.15-5
- Moved static lib to -static

* Mon Mar 24 2008 Ian Weller <ianweller@gmail.com> 1.15-4
- Added libraries and ldconfig

* Mon Feb 18 2008 Ian Weller <ianweller@gmail.com> 1.15-3
- Added provides -static to -devel

* Sun Feb 17 2008 Ian Weller <ianweller@gmail.com> 1.15-2
- Removed redundant requires
- Removed redundant documentation between packages
- Fixed license tag
- Fixed -devel description
- Added the static library back to -devel
- Added make clean

* Fri Feb 08 2008 Ian Weller <ianweller@gmail.com> 1.15-1
- First package build.
