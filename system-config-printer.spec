Summary:	A graphical interface for configuring printers
Summary(pl.UTF-8):	Graficzny interfejs do zarządzania drukarkami
Name:		system-config-printer
Version:	1.2.95
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	http://cyberelk.net/tim/data/system-config-printer/1.3/%{name}-%{version}.tar.bz2
# Source0-md5:	2fa97e9814b4c555fa8604091d714a79
URL:		http://cyberelk.net/tim/software/system-config-printer/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	intltool
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	xmlto
%pyrequires_eq	python-libs
Requires:	python-PyXML
Requires:	python-pycups >= 1.9.28
Requires:	python-pygtk-glade
Requires:	python-pynotify
Requires:	python-smbc
Obsoletes:	eggcups
Obsoletes:	gnome-cups-manager < 0.34
# sr@Latn vs. sr@latin
Conflicts:	glibc-misc < 6:2.7
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The purpose of the tool is to configure a CUPS server (often the local
machine) using the CUPS API. The tool is written in Python, using
pygtk for the graphical parts and with some Python bindings (pycups)
for the CUPS API.

%description -l pl.UTF-8
To narzędzie służy do konfigurowania serwera CUPS (zwykle na maszynie
lokalnej) przy użyciu API CUPS-a. Narzędzie jest napisane w Pythonie z
użyciem pygtk do części graficznych i dowiązań Pythona (pycups) do API
CUPS-a.

%prep
%setup -q

%build
%{__intltoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure
%{__make} -j 1

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%py_comp $RPM_BUILD_ROOT%{_datadir}/system-config-printer
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/system-config-printer
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}/cupshelpers
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}/cupshelpers
%py_postclean

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
%attr(755,root,root) %{_bindir}/system-config-printer
%attr(755,root,root) %{_bindir}/system-config-printer-applet
%{_sysconfdir}/xdg/autostart/*.desktop
/etc/dbus-1/system.d/com.redhat.NewPrinterNotification.conf
/etc/dbus-1/system.d/com.redhat.PrinterDriversInstaller.conf
%dir %{_datadir}/system-config-printer
%dir %{_datadir}/system-config-printer/ui
%{_datadir}/system-config-printer/ui/*.glade
%attr(755,root,root) %{_datadir}/system-config-printer/*.py*
%dir %{_datadir}/system-config-printer/troubleshoot
%attr(755,root,root) %{_datadir}/system-config-printer/troubleshoot/*.py*
%dir %{_datadir}/system-config-printer/icons
%{_datadir}/system-config-printer/icons/i-network-printer.png
%{_mandir}/man*/*
%{_desktopdir}/*.desktop
%{py_sitescriptdir}/cupshelpers-1.0-py*.egg-info
%dir %{py_sitescriptdir}/cupshelpers
%{py_sitescriptdir}/cupshelpers/*.py[co]
