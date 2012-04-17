Summary:	A graphical interface for configuring printers
Summary(pl.UTF-8):	Graficzny interfejs do zarządzania drukarkami
Name:		system-config-printer
Version:	1.3.9
Release:	2
License:	GPL v2+
Group:		X11/Applications
Source0:	http://cyberelk.net/tim/data/system-config-printer/1.3/%{name}-%{version}.tar.xz
# Source0-md5:	df424f127eede63965608e5ec5e27519
Patch0:		pyc.patch
URL:		http://cyberelk.net/tim/software/system-config-printer/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-devel
BuildRequires:	intltool
BuildRequires:	pkgconfig
BuildRequires:	python-devel
BuildRequires:	python-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	tar >= 1:1.22
BuildRequires:	xmlto
BuildRequires:	xz >= 1:4.999.7
%pyrequires_eq	python-libs
Requires:	python-PyXML
Requires:	python-pycurl
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

%package libs
Summary:	Libraries and shared code for printer administration tool
Group:		Base
Requires:	python
Requires:	python-pycups >= 1.9.60
Conflicts:	%{name} < 1.3.9

%description libs
The common code used by both the graphical and non-graphical parts of
the configuration tool.

%package udev
Summary:	Rules for udev for automatic configuration of USB printers
Group:		Base
Requires(post,preun,postun):	systemd-units >= 38
Requires:	%{name}-libs = %{version}-%{release}
Requires:	systemd-units >= 0.38
Provides:	hal-cups-utils = 0.6.20
Obsoletes:	hal-cups-utils < 0.6.20

%description udev
The udev rules and helper programs for automatically configuring USB
printers.

%prep
%setup -q
%patch0 -p1

%build
%{__intltoolize}
%{__aclocal}
%{__autoconf}
%{__automake}
%configure \
	--with-udev-rules
%{__make} \
	udevhelperdir=/lib/udev

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
	udevhelperdir=/lib/udev \
	udevrulesdir=/lib/udev/rules.d \
	DESTDIR=$RPM_BUILD_ROOT

%find_lang %{name}

%py_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py_comp $RPM_BUILD_ROOT%{py_sitescriptdir}/cupshelpers
%py_ocomp $RPM_BUILD_ROOT%{py_sitescriptdir}/cupshelpers
%py_postclean %{_datadir}/%{name}

%clean
rm -rf $RPM_BUILD_ROOT

%post udev
%systemd_post udev-configure-printer.service

%preun udev
%systemd_preun udev-configure-printer.service

%postun udev
%systemd_reload

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README
/etc/xdg/autostart/print-applet.desktop
%attr(755,root,root) %{_bindir}/system-config-printer
%attr(755,root,root) %{_bindir}/system-config-printer-applet
%dir %{_datadir}/%{name}/ui
%{_datadir}/%{name}/ui/*.ui
%dir %{_datadir}/%{name}/troubleshoot
%{_datadir}/%{name}/troubleshoot/*.py[co]
%dir %{_datadir}/%{name}/xml
%{_datadir}/%{name}/xml/*.rng
%{_datadir}/%{name}/xml/validate.py[co]
%{_datadir}/%{name}/check-device-ids.py[co]
%{_datadir}/%{name}/HIG.py[co]
%{_datadir}/%{name}/SearchCriterion.py[co]
%{_datadir}/%{name}/serversettings.py[co]
%{_datadir}/%{name}/system-config-printer.py[co]
%{_datadir}/%{name}/ToolbarSearchEntry.py[co]
%{_datadir}/%{name}/userdefault.py[co]
%{_datadir}/%{name}/applet.py[co]
%dir %{_datadir}/%{name}/icons
%{_datadir}/%{name}/icons/i-network-printer.png
%{_mandir}/man1/system-config-printer-applet.1*
%{_mandir}/man1/system-config-printer.1*
%{_desktopdir}/*.desktop

%files libs
%defattr(644,root,root,755)
%dir %{_sysconfdir}/cupshelpers
%config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/cupshelpers/preferreddrivers.xml
/etc/dbus-1/system.d/com.redhat.NewPrinterNotification.conf
/etc/dbus-1/system.d/com.redhat.PrinterDriversInstaller.conf
%{_datadir}/dbus-1/interfaces/org.fedoraproject.Config.Printing.xml
%{_datadir}/dbus-1/services/org.fedoraproject.Config.Printing.service
%attr(755,root,root) %{_bindir}/scp-dbus-service
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/asyncconn.py[co]
%{_datadir}/%{name}/asyncipp.py[co]
%{_datadir}/%{name}/asyncpk1.py[co]
%{_datadir}/%{name}/authconn.py[co]
%{_datadir}/%{name}/config.py[co]
%{_datadir}/%{name}/cupspk.py[co]
%{_datadir}/%{name}/debug.py[co]
%{_datadir}/%{name}/dnssdresolve.py[co]
%{_datadir}/%{name}/errordialogs.py[co]
%{_datadir}/%{name}/firewall.py[co]
%{_datadir}/%{name}/gtkinklevel.py[co]
%{_datadir}/%{name}/gtk_label_autowrap.py[co]
%{_datadir}/%{name}/gtkspinner.py[co]
%{_datadir}/%{name}/gui.py[co]
%{_datadir}/%{name}/installpackage.py[co]
%{_datadir}/%{name}/jobviewer.py[co]
%{_datadir}/%{name}/monitor.py[co]
%{_datadir}/%{name}/newprinter.py[co]
%{_datadir}/%{name}/options.py[co]
%{_datadir}/%{name}/optionwidgets.py[co]
%{_datadir}/%{name}/PhysicalDevice.py[co]
%{_datadir}/%{name}/ppdcache.py[co]
%{_datadir}/%{name}/ppdippstr.py[co]
%{_datadir}/%{name}/ppdsloader.py[co]
%{_datadir}/%{name}/printerproperties.py[co]
%{_datadir}/%{name}/probe_printer.py[co]
%{_datadir}/%{name}/pysmb.py[co]
%{_datadir}/%{name}/scp-dbus-service.py[co]
%{_datadir}/%{name}/smburi.py[co]
%{_datadir}/%{name}/statereason.py[co]
%{_datadir}/%{name}/timedops.py[co]

%dir %{py_sitescriptdir}/cupshelpers
%{py_sitescriptdir}/cupshelpers/__init__.py[co]
%{py_sitescriptdir}/cupshelpers/config.py[co]
%{py_sitescriptdir}/cupshelpers/cupshelpers.py[co]
%{py_sitescriptdir}/cupshelpers/installdriver.py[co]
%{py_sitescriptdir}/cupshelpers/openprinting.py[co]
%{py_sitescriptdir}/cupshelpers/ppds.py[co]
%{py_sitescriptdir}/cupshelpers/xmldriverprefs.py[co]
%{py_sitescriptdir}/*.egg-info

%files udev
%defattr(644,root,root,755)
/lib/udev/rules.d/*-printers.rules
%attr(755,root,root) /lib/udev/udev-add-printer
%attr(755,root,root) /lib/udev/udev-configure-printer
%{systemdunitdir}/udev-configure-printer.service
