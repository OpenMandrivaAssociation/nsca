Summary:	NSCA daemon for Nagios
Name:		nsca
Version:	2.7.2
Release:	%mkrel 6
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
