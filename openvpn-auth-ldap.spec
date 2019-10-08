Summary: OpenVPN plugin for LDAP authentication
Name: openvpn-auth-ldap
Version: 2.0.4
Release: 2%{?dist}
License: BSD
Group: Applications/Internet
URL: https://github.com/threerings/openvpn-auth-ldap 
Source0: https://github.com/threerings/openvpn-auth-ldap/archive/auth-ldap-%{version}.tar.gz
Patch0: 77.patch
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
# This is a plugin not linked against a lib, so hardcode the requirement
# since we require the parent configuration and plugin directories
Requires: openvpn >= 2.0
BuildRequires: re2c
BuildRequires: doxygen
BuildRequires: openldap-devel
BuildRequires: openssl-devel
BuildRequires: openvpn-devel
BuildRequires: check-devel
BuildRequires: gcc-objc
BuildRequires: autoconf

%description
The OpenVPN Auth-LDAP Plugin implements username/password authentication via
LDAP for OpenVPN 2.x.

%prep
%setup -q -n openvpn-auth-ldap-auth-ldap-%{version}
%patch0 -p1
autoreconf -fvi
autoheader

%build
CFLAGS="-fPIC" OBJCFLAGS="-std=gnu11"
%configure \
    --libdir=%{_libdir}/openvpn/plugins \
    --with-openvpn="/usr/include/openvpn"
make %{?_smp_mflags}

%install
rm -rf %{buildroot}
# Main plugin
mkdir -p %{buildroot}%{_libdir}/openvpn/plugins
make install DESTDIR=%{buildroot}
# Example config file
install -D -p -m 0600 auth-ldap.conf \
    %{buildroot}%{_sysconfdir}/openvpn/server/auth/ldap.conf

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root,-)
%doc LICENSE auth-ldap.conf
%dir %{_sysconfdir}/openvpn/server/auth/
%config(noreplace) %{_sysconfdir}/openvpn/server/auth/ldap.conf
%{_libdir}/openvpn/plugins/openvpn-auth-ldap.so


%changelog
* Tue Oct 8 2019 Konstantin Shalygin <k0ste@k0ste.ru> 2.0.4-2
- Update dependencies list.
- Add TLSRequireCert option patch.

* Mon Oct 7 2019 Konstantin Shalygin <k0ste@k0ste.ru> 2.0.4-1
- Fixed plugin path's.
- Use openvpn-devel headers.
- Bump version to 2.0.4.

* Thu Sep 05 2019 Sean Callaway <seancallaway@gmail.com> 2.0.3-17
- Applied patch to prevent crash when LDAP server unavailable.

* Wed Jan 23 2019 Sean Callaway <seancallaway@gmail.com> 2.0.3-16
- Added unapplied patch.

* Wed Sep 13 2017 Sean Callaway <seancallaway@gmail.com> 2.0.3-15
- Include patch to fix binding before STARTTLS has completed.
- Updated URLs.

* Mon Apr 11 2016 Sean Callaway <seancallaway@gmail.com> 2.0.3-14.1
- Rebuilt for OpenVPN 2.3.10 headers.

* Fri Jun 12 2015 Konstantin Shalygin <k0ste@k0ste.ru> 2.0.3-14
- Added RFC2307 patch.

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

