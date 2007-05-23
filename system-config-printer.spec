Summary:	A graphical interface for modifying system date and time
Summary(pl.UTF-8):	Graficzny interfejs do zmiany daty i czasu systemowego
Name:		system-config-printer
Version:	0.7.65
Release:	0.1
License:	GPL v2
Group:		X11/Application
Source0:	http://cyberelk.net/tim/data/system-config-printer/%{name}-%{version}.tar.bz2
# Source0-md5:	c076dee6f8ecc0819a9d397b8f204e74
URL:		http://cyberelk.net/tim/software/system-config-printer/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	gettext-devel
BuildRequires:	intltool
BuildRequires:	python-devel
%pyrequires_eq	python-libs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
system-config-date is a graphical interface for changing the system
date and time, configuring the system time zone, and setting up the
NTP daemon to synchronize the time of the system with a NTP time
server.

%description -l pl.UTF-8
system-config-date to graficzny interfejs do zmiany daty i czasu
systemowego, konfiguracji strefy czasowej i ustawiania demona NTP do
synchronizacji czasu systemowego z serwerem czasu NTP.

%prep
%setup -q

%build
%{__aclocal}
%{__autoconf}
%{__automake}
%{configure}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

rm -rf $RPM_BUILD_ROOT%{_datadir}/locale/no

%find_lang %{name}

%py_postclean %{_datadir}/system-config-printer

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/system-config-printer-applet
%attr(755,root,root) %{_sbindir}/system-config-printer
%{_sysconfdir}/xdg/autostart/*.desktop
%{_datadir}/system-config-printer
%{_mandir}/man*/*
%{_desktopdir}/*.desktop
