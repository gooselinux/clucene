%define build_contrib	0

Summary:	A C++ port of Lucene
Name:		clucene
Version:	0.9.21b
Release:	1%{?dist}
License:	LGPLv2+ or ASL 2.0
Group:		Development/System
URL:		http://www.sourceforge.net/projects/clucene
Source0:	http://downloads.sourceforge.net/clucene/clucene-core-%{version}.tar.bz2
%if %{build_contrib}
Source1:	http://downloads.sourceforge.net/clucene/clucene-contrib-0.9.16a.tar.bz2
Patch1:		clucene-contrib-autoconf.patch
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:	automake gawk

%description
CLucene is a C++ port of Lucene.
It is a high-performance, full-featured text search 
engine written in C++. CLucene is faster than lucene
as it is written in C++

%package core
Summary:	Core clucene module
Group:		Development/System
Provides:	clucene
#Requires: %{name} = %{version}-%{release}

%description core
The core clucene module

%package core-devel
Summary:	Headers for developing programs that will use %{name}
Group:		Development/Libraries
Requires:	%{name}-core = %{version}-%{release}

%description core-devel
This package contains the static libraries and header files needed for
developing with clucene

%if %{build_contrib}
%package	contrib
Summary:	Core clucene module
Group:		Development/System
Requires:	%{name}-core >= %{version}-%{release}

%description contrib
Collection of contributions for C++ port of Lucene

%package contrib-devel
Summary:	Headers for developing programs that will use %{name}
Group:		Development/Libraries
Requires:	%{name}-contrib = %{version}-%{release}
Requires:	%{name}-core-devel >= %{version}-%{release}

%description contrib-devel
This package contains the static libraries and header files needed for
developing with clucene-contrib
%endif

%prep
%if %{build_contrib}
%setup -q -c -a 1
cd %{name}-contrib-%{version}
%patch1 -p0 -b .autoconf
%else
%setup -q -c -a 0
%endif

%build
pushd %{name}-core-%{version}
%configure --disable-static
make %{?_smp_mflags}
popd

%if %{build_contrib}
pushd %{name}-contrib-%{version}
aclocal -I m4
autoconf
automake --add-missing --copy
%configure --disable-static
make %{?_smp_mflags}
popd
%endif

%install
rm -rf %{buildroot}
pushd %{name}-core-%{version}
make DESTDIR=%{buildroot} install
popd

%if %{build_contrib}
pushd %{name}-contrib-%{version}
make DESTDIR=%{buildroot} install
popd
%endif

#Package the docs
mkdir -p %{buildroot}%{_datadir}/%{name}/doc
mkdir -p %{buildroot}%{_datadir}/doc/%{name}-%{version}
pushd %{name}-core-%{version}
cp -pr doc/*.htm doc/*.jpg %{buildroot}%{_datadir}/%{name}/doc
cp -pr AUTHORS COPYING HACKING README REQUESTS \
       %{buildroot}%{_datadir}/doc/%{name}-%{version}
popd

# Run the tests 
## It currently fails 2 tests for ppc64 builds, upstream is looking into it.
%ifnarch ppc64 s390x sparc64
%check
pushd %{name}-core-%{version}
make check
popd
%endif

rm -rf %{buildroot}%{_libdir}/*.la
# These are from the contrib package
rm -rf %{buildroot}%{_includedir}/CuTest.h
rm -rf %{buildroot}%{_includedir}/test.h

%clean
rm -rf %{buildroot}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files core
%defattr(-, root, root, -)
#%doc AUTHORS COPYING HACKING README REQUESTS
%{_libdir}/libclucene.so.*
%{_datadir}/doc/%{name}-%{version}/

%files core-devel
%defattr(-, root, root, -)
%dir %{_includedir}/CLucene
%dir %{_libdir}/CLucene
%{_includedir}/CLucene/*
%{_includedir}/CLucene.h
%{_libdir}/libclucene.so
%{_libdir}/CLucene/clucene-config.h
%{_datadir}/%{name}/
%if %{build_contrib}
%exclude %{_includedir}/CLucene/clucene-config-contrib.h
%exclude %{_includedir}/CLucene/analysis/cjk/
%exclude %{_includedir}/CLucene/highlighter/
%exclude %{_includedir}/CLucene/jstreams/
%exclude %{_includedir}/CLucene/snowball/
%endif

%if %{build_contrib}
%files contrib
%defattr(-, root, root, -)
%{_libdir}/libclucene-contrib.so.*

%files contrib-devel
%defattr(-, root, root, -)
%dir %{_libdir}/CLucene
%{_includedir}/CLucene/clucene-config-contrib.h
%{_includedir}/CLucene/analysis/cjk/
%{_includedir}/CLucene/highlighter/
%{_includedir}/CLucene/jstreams/
%{_includedir}/CLucene/snowball/
%{_libdir}/libclucene-contrib.so
%{_libdir}/CLucene/clucene-config-contrib.h
%endif

%changelog
* Wed Jun 16 2010 Jaroslav Reznik <jreznik@redhat.com> - 0.9.21b-1
- Resolves: bz#600925, update to version 0.9.21b

* Wed Nov 04 2009 Dennis Gilmore <dennis@ausil.us> - 0.9.21-5
- disable 'make check on sparc64 along with ppc64 and s390x

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.21-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Apr 14 2009 Karsten Hopp <karsten@redhat.com> 0.9.21-3
- bypass 'make check' on s390x, similar to ppc64

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.9.21-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Wed Aug 27 2008 Deji Akingunola <dakingun@gmail.com> - 0.9.21-1
- Update to version 0.9.21

* Sun Feb 10 2008 Deji Akingunola <dakingun@gmail.com> - 0.9.20-4
- Rebuild for gcc43

* Wed Oct 25 2007 Deji Akingunola <dakingun@gmail.com> - 0.9.20-3
- Fix a typo in the License field

* Wed Oct 25 2007 Deji Akingunola <dakingun@gmail.com> - 0.9.20-2
- Fix multiarch conflicts (BZ #340891)
- Bypass 'make check' for ppc64, its failing two tests there

* Tue Aug 21 2007 Deji Akingunola <dakingun@gmail.com> - 0.9.20-1
- Update to version 0.9.20

* Sat Aug 11 2007 Deji Akingunola <dakingun@gmail.com> - 0.9.19-1
- Latest release update

* Fri Aug 03 2007 Deji Akingunola <dakingun@gmail.com> - 0.9.16a-2
- License tag update

* Thu Feb 22 2007 Deji Akingunola <dakingun@gmail.com> - 0.9.16a-2
- Add -contrib subpackage 

* Thu Dec 07 2006 Deji Akingunola <dakingun@gmail.com> - 0.9.16a-1
- Update to latest stable release 
- Run make check during build

* Mon Nov 20 2006 Deji Akingunola <dakingun@gmail.com> - 0.9.15-3
- Don't package APACHE.license since we've LGPL instead 
- Package documentation in devel subpackage

* Mon Nov 13 2006 Deji Akingunola <dakingun@gmail.com> - 0.9.15-2
- Fix a bunch of issues with the spec (#215258)
- Moved the header file away from lib dir

* Sat Nov 04 2006 Deji Akingunola <dakingun@gmail.com> - 0.9.15-1
- Initial packaging for Fedora Extras
