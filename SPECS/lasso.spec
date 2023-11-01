%global with_java 1
%global with_php 0
%global with_perl 1
%global with_python 1
%global with_python2 0
%global with_python3 0
%global with_wsf 0
%global obsolete_old_lang_subpackages 0

%if %{with_php}
%if "%{php_version}" < "5.6"
%global ini_name     %{name}.ini
%else
%global ini_name     40-%{name}.ini
%endif
%endif

%if (0%{?fedora} > 0 && 0%{?fedora} <= 29) || (0%{?rhel} > 0 && 0%{?rhel} <= 7)
  %global obsolete_old_lang_subpackages 1
%endif

%if %{with_python}
  %if (0%{?fedora} > 0 && 0%{?fedora} < 32) || (0%{?rhel} > 0 && 0%{?rhel} <= 7)
    %global with_python2 1
  %endif

  %if 0%{?fedora} || 0%{?rhel} >= 8
    %global with_python3 1
  %endif
%endif

%global configure_args %{nil}
%global configure_args %{configure_args} 

%if !%{with_java}
  %global configure_args %{configure_args} --disable-java
%endif

%if !%{with_perl}
  %global configure_args %{configure_args} --disable-perl
%endif

%if %{with_php}
  %global configure_args %{configure_args} --enable-php5=yes --with-php5-config-dir=%{php_inidir}
%else
  %global configure_args %{configure_args} --enable-php5=no
%endif

%if %{with_wsf}
  %global configure_args %{configure_args} --enable-wsf --with-sasl2=%{_prefix}/sasl2
%endif

%if !%{with_python}
  %global configure_args %{configure_args} --disable-python
%endif


Summary: Liberty Alliance Single Sign On
Name: lasso
Version: 2.6.0
Release: 13%{?dist}
License: GPLv2+
Group: System Environment/Libraries
Source: http://dev.entrouvert.org/lasso/lasso-%{version}.tar.gz

Patch1: use-specified-python-interpreter.patch
Patch2: build-scripts-py3-compatible.patch
Patch3: duplicate-python-LogoutTestCase.patch
Patch4: versioned-python-configure.patch
Patch5: 0005-tests-use-self-generated-certificate-to-sign-federat.patch
Patch6: 0006-Fix-ECP-signature-not-found-error-when-only-assertio.patch
Patch7: 0007-PAOS-Do-not-populate-Destination-attribute.patch
Patch8: 0008-Fix-signature-checking-on-unsigned-response-with-mul.patch
Patch9: 0009-lasso_saml20_login_process_response_status_and_asser.patch

BuildRequires: libtool autoconf automake

# The Lasso build system requires python, especially the binding generators
%if %{with_python2}
BuildRequires: python2
BuildRequires: python2-lxml
BuildRequires: python2-six
%endif

%if %{with_python3}
BuildRequires: python3
BuildRequires: python3-lxml
BuildRequires: python3-six
%endif

%if %{with_wsf}
BuildRequires: cyrus-sasl-devel
%endif
BuildRequires: gtk-doc, libtool-ltdl-devel
BuildRequires: glib2-devel, swig
BuildRequires: libxml2-devel, openssl-devel 
BuildRequires: xmlsec1-devel >= 1.2.25-4, xmlsec1-openssl-devel >= 1.2.25-4
BuildRequires: zlib-devel, check-devel
BuildRequires: libtool autoconf automake
Url: http://lasso.entrouvert.org/

Requires: xmlsec1 >= 1.2.25-4

%description
Lasso is a library that implements the Liberty Alliance Single Sign On
standards, including the SAML and SAML2 specifications. It allows to handle
the whole life-cycle of SAML based Federations, and provides bindings
for multiple languages.

%package devel
Summary: Lasso development headers and documentation
Group: Development/Libraries
Requires: %{name}%{?_isa} = %{version}-%{release}

%description devel
This package contains the header files, static libraries and development
documentation for Lasso.

%if %{with_perl}
%package -n perl-%{name}
Summary: Liberty Alliance Single Sign On (lasso) Perl bindings
Group: Development/Libraries
BuildRequires: perl-devel
BuildRequires: perl(ExtUtils::MakeMaker)
BuildRequires: perl(Test::More)
BuildRequires: perl(Error)
Requires: perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n perl-%{name}
Perl language bindings for the lasso (Liberty Alliance Single Sign On) library.
%endif

%if %{with_java}
%package -n java-%{name}
Summary: Liberty Alliance Single Sign On (lasso) Java bindings
Group: Development/Libraries
BuildRequires: java-devel
BuildRequires: jpackage-utils
Requires: java-headless
Requires: jpackage-utils
Requires: %{name}%{?_isa} = %{version}-%{release}
%if %{obsolete_old_lang_subpackages}
Provides: %{name}-java = %{version}-%{release}
Provides: %{name}-java%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-java < %{version}-%{release}
%endif

%description -n java-%{name}
Java language bindings for the lasso (Liberty Alliance Single Sign On) library.
%endif

%if %{with_php}
%package -n php-%{name}
Summary: Liberty Alliance Single Sign On (lasso) PHP bindings
Group: Development/Libraries
BuildRequires: php-devel, expat-devel
Requires: %{name}%{?_isa} = %{version}-%{release}
Requires: php(zend-abi) = %{php_zend_api}
Requires: php(api) = %{php_core_api}

%description -n php-%{name}
PHP language bindings for the lasso (Liberty Alliance Single Sign On) library.

%endif

%if %{with_python2}
%package -n python2-%{name}
%{?python_provide:%python_provide python2-%{name}}
Summary: Liberty Alliance Single Sign On (lasso) Python bindings
Group: Development/Libraries
BuildRequires: python2-devel
Requires: python2
Requires: %{name}%{?_isa} = %{version}-%{release}
%if %{obsolete_old_lang_subpackages}
Provides: %{name}-python = %{version}-%{release}
Provides: %{name}-python%{?_isa} = %{version}-%{release}
Obsoletes: %{name}-python < %{version}-%{release}
%endif

%description -n python2-%{name}
Python language bindings for the lasso (Liberty Alliance Single Sign On)
library.
%endif

%if %{with_python3}
%package -n python3-%{name}
%{?python_provide:%python_provide python3-%{name}}
Summary: Liberty Alliance Single Sign On (lasso) Python bindings
Group: Development/Libraries
BuildRequires: python3-devel
%{?__python3:Requires: %{__python3}}
Requires: %{name}%{?_isa} = %{version}-%{release}

%description -n python3-%{name}
Python language bindings for the lasso (Liberty Alliance Single Sign On)
library.
%endif

%prep
%setup -q -n %{name}-%{version}

%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1

# Remove any python script shebang lines (unless they refer to python3)
sed -i -E -e '/^#![[:blank:]]*(\/usr\/bin\/env[[:blank:]]+python[^3]?\>)|(\/usr\/bin\/python[^3]?\>)/d' \
  `grep -r -l -E '^#![[:blank:]]*(/usr/bin/python[^3]?)|(/usr/bin/env[[:blank:]]+python[^3]?)' *`

%build
./autogen.sh
%if 0%{?with_python2}
  %configure %{configure_args} --with-python=%{__python2}
  pushd lasso
  make %{?_smp_mflags} CFLAGS="%{optflags}"
  popd
  pushd bindings/python
  make %{?_smp_mflags} CFLAGS="%{optflags}"
  make check
  mkdir py2
  mv lasso.py .libs/_lasso.so py2
  popd
  make clean
%endif

%if 0%{?with_python3}
  %configure %{configure_args} --with-python=%{__python3}
%else
  %configure %{configure_args}
%endif
make %{?_smp_mflags} CFLAGS="%{optflags}"

%check
make check

%install
#install -m 755 -d %{buildroot}%{_datadir}/gtk-doc/html

make install exec_prefix=%{_prefix} DESTDIR=%{buildroot}
find %{buildroot} -type f -name '*.la' -exec rm -f {} \;
find %{buildroot} -type f -name '*.a' -exec rm -f {} \;

%if 0%{?with_python2}
  # Install Python 2 files saved from first build
  install -d -m 0755 %{buildroot}/%{python2_sitearch}
  install -m 0644 bindings/python/py2/lasso.py %{buildroot}/%{python2_sitearch}
  install -m 0755 bindings/python/py2/_lasso.so %{buildroot}/%{python2_sitearch}
%endif

# Perl subpackage
%if %{with_perl}
find %{buildroot} \( -name perllocal.pod -o -name .packlist \) -exec rm -v {} \;

find %{buildroot}/usr/lib*/perl5 -type f -print |
        sed "s@^%{buildroot}@@g" > %{name}-perl-filelist
if [ "$(cat %{name}-perl-filelist)X" = "X" ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit -1
fi
%endif

# PHP subpackage
%if %{with_php}
install -m 755 -d %{buildroot}%{_datadir}/php/%{name}
mv %{buildroot}%{_datadir}/php/lasso.php %{buildroot}%{_datadir}/php/%{name}

# rename the PHP config file when needed (PHP 5.6+)
if [ "%{name}.ini" != "%{ini_name}" ]; then
  mv %{buildroot}%{php_inidir}/%{name}.ini \
     %{buildroot}%{php_inidir}/%{ini_name}
fi
%endif

# Remove bogus doc files
rm -fr %{buildroot}%{_defaultdocdir}/%{name}

%post -p /sbin/ldconfig

%postun -p /sbin/ldconfig

%files
%{_libdir}/liblasso.so.*
%doc AUTHORS COPYING NEWS README

%files devel
%{_libdir}/liblasso.so
%{_libdir}/pkgconfig/lasso.pc
%{_includedir}/%{name}

%if %{with_perl}
%files -n perl-%{name} -f %{name}-perl-filelist
%endif

%if %{with_java}
%files -n java-%{name}
%{_libdir}/java/libjnilasso.so
%{_javadir}/lasso.jar
%endif

%if %{with_php}
%files -n php-%{name}
%attr(755,root,root) %{php_extdir}/lasso.so
%config(noreplace) %attr(644,root,root) %{php_inidir}/%{ini_name}
%attr(755,root,root) %dir %{_datadir}/php/%{name}
%attr(644,root,root) %{_datadir}/php/%{name}/lasso.php
%endif

%if %{with_python2}
%files -n python2-%{name}
%{python2_sitearch}/lasso.py*
%{python2_sitearch}/_lasso.so
%endif

%if %{with_python3}
%files -n python3-%{name}
%{python3_sitearch}/lasso.py*
%{python3_sitearch}/_lasso.so
%{python3_sitearch}/__pycache__/*
%endif

%changelog
* Wed May 4 2022 Tomas Halman <thalman@redhat.com> - 2.6.0-13
- Publishing the python3-lasso binding
- Resolves: rhbz#1888195 - Release python lasso package

* Fri Jul 30 2021 Jakub Hrozek <jhrozek@redhat.com> - 2.6.0-12
- Fix a dead code issue in the signature wrapping patch
- Resolves: rhbz#1951653 - CVE-2021-28091 lasso: XML signature wrapping
                           vulnerability when parsing SAML responses [rhel-8]

* Mon Jun 21 2021 Jakub Hrozek <jhrozek@redhat.com> - 2.6.0-11
- Bump release to force the package through OSCI as the previous
  build reached CI just in time for an outage
- Related: rhbz#1888195 - [RFE] release (built) python3-lasso pkg (comingfrom lasso)

* Fri Jun  4 2021 Jakub Hrozek <jhrozek@redhat.com> - 2.6.0-10
- Resolves: rhbz#1951653 - CVE-2021-28091 lasso: XML signature wrapping
                           vulnerability when parsing SAML responses [rhel-8]

* Thu May  6 2021 Jakub Hrozek <jhrozek@redhat.com> - 2.6.0-9
- Resolves: rhbz#1888195 - [RFE] release (built) python3-lasso pkg (coming
                           from lasso)

* Fri Oct 18 2019 Jakub Hrozek <jhrozek@redhat.com> - 2.6.0-8
- Resolves: rhbz#1730018 - lasso includes "Destination" attribute in SAML
                           AuthnRequest populated with SP
                           AssertionConsumerServiceURL when ECP workflow
                           is used which leads to IdP-side errors

* Fri Jun 14 2019 Jakub Hrozek <jhrozek@redhat.com> - 2.6.0-7
- Resolves: rhbz#1634268 - ECP signature check fails with
                           LASSO_DS_ERROR_SIGNATURE_NOT_FOUND when
                           assertion signed instead of response

* Thu Jun 13 2019 Jakub Hrozek <jhrozek@redhat.com> - 2.6.0-6
- Resolves: rhbz#1719020 - Expired certificate prevents tests from running

* Tue Sep 25 2018 Tomas Orsava <torsava@redhat.com> - 2.6.0-5
- Require the Python interpreter directly instead of using the package name
- Resolves: rhbz#1633617

* Tue Jul 17 2018  <jdennis@redhat.com> - 2.6.0-4
- more fixes for py2/py3 build dependencies

* Mon Jul  9 2018  <jdennis@redhat.com> - 2.6.0-3
- Modify configure to search for versioned python
- Resolves: rhbz#1598047
- Related: rhbz#1589856

* Wed Jun 27 2018  <jdennis@redhat.com> - 2.6.0-2
- fix language bindings package names to comply with guidelines,
  instead of %{name}-lang use lang-%{name}
- fix conditional logic used to build on rhel
- Resolves: rhbz#1589856 Drop python2 subpackage from RHEL8

* Tue Jun 26 2018  <jdennis@redhat.com> - 2.6.0-1
- Upgrade to latest upstream
- Build using Python3, add python3 subpackage
- Resolves: rhbz#1592416 Enable perl subpackage

* Wed May  2 2018 John Dennis <jdennis@redhat.com> - 2.5.1-13
- add xmlsec1 version dependency

* Tue May  1 2018 John Dennis <jdennis@redhat.com> - 2.5.1-12
- Resolves: rhbz#1542126, rhbz#1556016
- xmlsec removed SOAP support, reimplement missing xmlSecSoap* in Lasso

* Wed Feb 07 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Fri Jan 05 2018 Iryna Shcherbina <ishcherb@redhat.com> - 2.5.1-10
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Sun Aug 20 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.5.1-9
- Add Provides for the old name without %%_isa

* Sat Aug 19 2017 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 2.5.1-8
- Python 2 binary package renamed to python2-lasso
  See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3

* Thu Aug 03 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Binutils_Mass_Rebuild

* Wed Jul 26 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Fri Feb 10 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.5.1-4
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Jun 30 2016 John Dennis <jdennis@redhat.com> - 2.5.1-3
- disbable PHP binding because PHP-7 is now the default and lasso
  only knows how to build with PHP-5

* Wed Jun 15 2016 John Dennis <jdennis@redhat.com> - 2.5.1-2
- fix CFLAGS override in configure

* Mon Feb 22 2016 John Dennis <jdennis@redhat.com> - 2.5.1-1
- Upgrade to upstream 2.5.1 release
  See Changelog for details, mostly bugs fixes,
  most signficant is proper support of SHA-2
  Resolves: #1295472
  Resolves: #1303573
- Add java_binding_lasso_log.patch to fix "make check" failure during rpmbuild
  upstream commit d8e3ae8

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.5.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Mon Sep 14 2015 John Dennis <jdennis@redhat.com> - 2.5.0-1
- Upgrade to new upstream 2.5.0 release
  Includes ECP support

* Wed Jun 17 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Mon Mar 23 2015 Rob Crittenden <rcritten@redhat.com> - 2.4.1-3
- Add BuildRequires on libtool
- Add -fPIC to LDFLAGS
- Disable perl bindings, it fails to build on x86.

* Fri Jan 23 2015 Simo Sorce <simo@redhat.com> - 2.4.1-2
- Enable perl bindings
- Also add support for building with automake 1.15
- Fix build issues on rawhide due to missing build dep on perl(Error)

* Thu Aug 28 2014 Simo Sorce <simo@redhat.com> - 2.4.1-1
- New upstream relase 2.4.1
- Drop patches as they have all been integrated upstream

* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Fri Jun 20 2014 Remi Collet <rcollet@redhat.com> - 2.4.0-4
- rebuild for https://fedoraproject.org/wiki/Changes/Php56
- add numerical prefix to extension configuration file
- drop unneeded dependency on pecl
- add provides php-lasso

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.4.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Fri Apr 25 2014 Simo Sorce <simo@redhat.com> - 2.4.0-2
- Fixes for arches where pointers and integers do not have the same size
  (ppc64, s390, etc..)

* Mon Apr 14 2014 Stanislav Ochotnicky <sochotnicky@redhat.com> - 2.4.0-1
- Use OpenJDK instead of GCJ for java bindings

* Sat Jan 11 2014 Simo Sorce <simo@redhat.com> 2.4.0-0
- Update to final 2.4.0 version
- Drop all patches, they are now included in 2.4.0
- Change Source URI

* Mon Dec  9 2013 Simo Sorce <simo@redhat.com> 2.3.6-0.20131125.5
- Add patches to fix rpmlint license issues
- Add upstream patches to fix some build issues

* Thu Dec  5 2013 Simo Sorce <simo@redhat.com> 2.3.6-0.20131125.4
- Add patch to support automake-1.14 for rawhide

* Mon Nov 25 2013 Simo Sorce <simo@redhat.com> 2.3.6-0.20131125.3
- Initial packaging
- Based on the spec file by Jean-Marc Liger <jmliger@siris.sorbonne.fr>
- Code is updated to latest master via a jumbo patch while waiting for
  official upstream release.
- Jumbo patch includes also additional patches sent to upstream list)
  to build on Fedora 20
- Perl bindings are disabled as they fail to build
- Disable doc building as it doesn't ork correctly for now
