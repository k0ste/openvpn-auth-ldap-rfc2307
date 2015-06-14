Summary: OpenVPN plugin for LDAP authentication
Name: openvpn-auth-ldap
Version: 2.0.3
Release: 16%{?dist}
License: BSD
Group: Applications/Internet
URL: http://code.google.com/p/openvpn-auth-ldap/
Source0: http://openvpn-auth-ldap.googlecode.com/files/auth-ldap-%{version}.tar.gz
Source1: openvpn-plugin.h
Patch0: auth-ldap-2.0.3-top_builddir.patch
Patch1: auth-ldap-2.0.3-README.patch
Patch2: auth-ldap-2.0.3-tools-CFLAGS.patch
Patch3: auth-ldap-gnustep.patch
Patch4: auth-ldap-2.0.3-remoteAddress.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
# This is a plugin not linked against a lib, so hardcode the requirement
# since we require the parent configuration and plugin directories
Requires: openvpn >= 2.0
BuildRequires: re2c
Buildrequires: doxygen
Buildrequires: openldap-devel
BuildRequires: check-devel
BuildRequires: gcc-objc
BuildRequires: gnustep-base-devel
BuildRequires: autoconf

%description
The OpenVPN Auth-LDAP Plugin implements username/password authentication via
LDAP for OpenVPN 2.x.


%prep
%setup -q -n auth-ldap-%{version}
%patch1 -p1 -b .README
%patch2 -p1 -b .tools-CFLAGS
%patch3 -p0 -b .gnustep
%patch4 -p1 -b .remoteAddress
# Fix plugin from the instructions in the included README
sed -i 's|^plugin .*| plugin %{_libdir}/openvpn/plugin/lib/openvpn-auth-ldap.so "/etc/openvpn/auth/ldap.conf"|g' README
# Install the one required OpenVPN plugin header
install -p -m 0644 %{SOURCE1} .
autoconf
autoheader


%build
# Fix undefined objc_msgSend reference (nope, the with-objc-runtime is enough)
#export OBJCFLAGS=-fobjc-abi-version=2
%configure \
%if 0%{?fedora} || 0%{?rhel} >= 7
    --with-objc-runtime=modern \
%endif
    --libdir=%{_libdir}/openvpn/plugin/lib \
    --with-openvpn="`pwd`"
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
# Main plugin
mkdir -p %{buildroot}%{_libdir}/openvpn/plugin/lib
make install DESTDIR=%{buildroot}
# Example config file
install -D -p -m 0600 auth-ldap.conf \
    %{buildroot}%{_sysconfdir}/openvpn/auth/ldap.conf


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE README auth-ldap.conf
%dir %{_sysconfdir}/openvpn/auth/
%config(noreplace) %{_sysconfdir}/openvpn/auth/ldap.conf
%{_libdir}/openvpn/plugin/lib/openvpn-auth-ldap.so


%changelog
* Sun Aug 17 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-16
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_22_Mass_Rebuild

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-15
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Mar 11 2014 Matthias Saou <matthias@saou.eu> 2.0.3-13
- Include remoteAddress patch from upstream issue n°4, to fix tap bridging.
- Only enable the modern objc on Fedora and EL7+ (not available on EL6).

* Sat Aug 03 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-13
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Wed May 29 2013 Orion Poplawski <orion@cora.nwra.com> - 2.0.3-12
- Use gnustep runtime (bug #870988)

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-11
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-10
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Wed Feb  8 2012 Matthias Saou <matthias@saou.eu> 2.0.3-10
- Include patch to fix check for no longer existing objc/objc-api.h file.

* Fri Jan 13 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Aug 13 2011 Matthias Saou <matthias@saou.eu> 2.0.3-8
- Minor spec file cleanups.
- Fix build on F-15+.
- Make sure tools/ content gets our CFLAGS.

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sat Jul 25 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.0.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Matthias Saou <matthias@saou.eu> 2.0.3-5
- Update URL and Source locations.

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org>
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sun Feb  3 2008 Matthias Saou <matthias@saou.eu> 2.0.3-3
- No longer use the full openvpn sources for the build, as only the
  openvpn-plugin.h file is required, so just include it alone.
- Fix check to check-devel build requirement (it needs the header).

* Thu Jun 21 2007 Matthias Saou <matthias@saou.eu> 2.0.3-2
- Patch and change README to remove build instructions and have the proper
  line to be added to openvpn's configuration.
- Move config file to a sub-dir since it gets picked up by openvpn otherwise.

* Wed Jun 20 2007 Matthias Saou <matthias@saou.eu> 2.0.3-1
- Initial RPM release.

