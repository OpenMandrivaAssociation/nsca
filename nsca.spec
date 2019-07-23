Summary:	NSCA daemon for Nagios
Name:		nsca
Version:	2.9.2
Release:	1
License:	GPL
Group:		System/Servers
URL:		http://sourceforge.net/projects/nagios/
Source0:	http://prdownloads.sourceforge.net/nagios/%{name}-%{version}.tar.gz
Source1:	nsca.init
Patch0:		nsca-mdv_conf.diff
BuildRequires:	tcp_wrappers-devel
BuildRequires:	libmcrypt-devel
BuildRequires:	libtool-devel
Requires:	tcp_wrappers
Requires:	nagios
Requires(post): rpm-helper
Requires(preun): rpm-helper
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
The NSCA addon is designed to accept passive host and service check results
from clients that use the send_nsca utility (included in client subpackage) and
pass them along to the Nagios process by using the external command interface.

%package -n	send_nsca
Summary:	NSCA client
Group:		System/Servers

%description -n	send_nsca
NSCA client - is used to send service check information from a remote machine
to the NSCA daemon on the central machine that runs Nagios.

%prep

%setup -q
%patch0 -p0

cp %{SOURCE1} nsca.init

%build

%configure2_5x \
    --with-nsca-port=5667 \
    --with-nsca-user=nagios \
    --with-nsca-grp=nagios \
    --localstatedir=/var/spool/nagios \
    --sysconfdir=%{_sysconfdir}/nagios

%make

%install
rm -rf %{buildroot}

install -d %{buildroot}%{_sysconfdir}/nagios
install -d %{buildroot}%{_initrddir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}/var/spool/nagios
install -d %{buildroot}/var/run/%{name}

install -m0755 src/nsca %{buildroot}%{_sbindir}/
install -m0755 src/send_nsca %{buildroot}%{_sbindir}/
install -m0755 nsca.init %{buildroot}%{_initrddir}/nsca
install -m0644 sample-config/nsca.cfg %{buildroot}%{_sysconfdir}/nagios/nsca.cfg
install -m0644 sample-config/send_nsca.cfg %{buildroot}%{_sysconfdir}/nagios/send_nsca.cfg

%post
%_post_service %{name}

%preun
%_preun_service %{name}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc Changelog LEGAL README SECURITY
%config(noreplace) %{_sysconfdir}/nagios/nsca.cfg
%{_initrddir}/nsca
%{_sbindir}/nsca
%attr(-,nagios,nagios) /var/spool/nagios
%attr(-,nagios,nagios) %dir /var/run/%{name}

%files -n send_nsca
%defattr(-,root,root)
%doc Changelog LEGAL README SECURITY
%config(noreplace) %{_sysconfdir}/nagios/send_nsca.cfg
%{_sbindir}/send_nsca


%changelog
* Fri Sep 04 2009 Thierry Vignaud <tvignaud@mandriva.com> 2.7.2-6mdv2010.0
+ Revision: 430184
- rebuild

  + Guillaume Rousse <guillomovitch@mandriva.org>
    - %files section cleanup

* Thu Sep 11 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.7.2-5mdv2009.0
+ Revision: 283883
- client package doesn't require nagios

* Fri Aug 08 2008 Thierry Vignaud <tvignaud@mandriva.com> 2.7.2-4mdv2009.0
+ Revision: 268291
- rebuild early 2009.0 package (before pixel changes)

* Thu May 15 2008 Guillaume Rousse <guillomovitch@mandriva.org> 2.7.2-3mdv2009.0
+ Revision: 207545
- LSB headers in initscript

* Mon Feb 11 2008 Oden Eriksson <oeriksson@mandriva.com> 2.7.2-2mdv2008.1
+ Revision: 165298
- rebuild

  + Olivier Blin <oblin@mandriva.com>
    - restore BuildRoot

  + Thierry Vignaud <tvignaud@mandriva.com>
    - kill re-definition of %%buildroot on Pixel's request

* Fri Jul 13 2007 Oden Eriksson <oeriksson@mandriva.com> 2.7.2-1mdv2008.0
+ Revision: 51850
- 2.7.2

* Tue Apr 17 2007 Oden Eriksson <oeriksson@mandriva.com> 2.7.1-1mdv2008.0
+ Revision: 13785
- Import nsca



* Wed Apr 11 2007 Oden Eriksson <oeriksson@mandriva.com> 2.7.1-1mdv2007.1
- initial mandriva package
