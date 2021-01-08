Summary:	A graphical interface for configuring printers
Summary(pl.UTF-8):	Graficzny interfejs do zarządzania drukarkami
Name:		system-config-printer
Version:	1.5.14
Release:	1
License:	GPL v2+
Group:		X11/Applications
Source0:	https://github.com/OpenPrinting/system-config-printer/releases/download/v%{version}/%{name}-%{version}.tar.xz
# Source0-md5:	eb59fc79921e4378cf35650ad91c7476
Patch0:		%{name}-exec.patch
URL:		https://github.com/OpenPrinting/system-config-printer
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	cups-devel
BuildRequires:	desktop-file-utils
BuildRequires:	docbook-dtd412-xml
BuildRequires:	gettext-tools
BuildRequires:	glib2-devel
BuildRequires:	intltool
BuildRequires:	libusb-devel
BuildRequires:	pkgconfig
BuildRequires:	python3-devel
BuildRequires:	python3-modules
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 1.21
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-devel >= 172
BuildRequires:	xmlto
BuildRequires:	xz >= 1:4.999.7
Requires:	%{name}-libs = %{version}-%{release}
Requires:	glib2
Requires:	gtk+3
Requires:	libnotify
Requires:	pango
Requires:	python3-dbus
Requires:	python3-modules
Requires:	python3-pycups >= 1.9.60
Requires:	python3-pycurl
Requires:	python3-pygobject3
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
Requires:	python3-pycups >= 1.9.60
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

%py3_comp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py3_ocomp $RPM_BUILD_ROOT%{_datadir}/%{name}
%py3_comp $RPM_BUILD_ROOT%{py_sitedir}/cupshelpers
%py3_ocomp $RPM_BUILD_ROOT%{py_sitedir}/cupshelpers

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
%doc AUTHORS ChangeLog NEWS
/etc/xdg/autostart/print-applet.desktop
%attr(755,root,root) %{_bindir}/install-printerdriver
%attr(755,root,root) %{_bindir}/system-config-printer
%attr(755,root,root) %{_bindir}/system-config-printer-applet
%{_datadir}/metainfo/system-config-printer.appdata.xml
%dir %{_datadir}/%{name}/ui
%{_datadir}/%{name}/ui/*.ui
%dir %{_datadir}/%{name}/troubleshoot
%{_datadir}/%{name}/troubleshoot/__pycache__
%{_datadir}/%{name}/troubleshoot/*.py
%dir %{_datadir}/%{name}/xml
%{_datadir}/%{name}/xml/__pycache__
%{_datadir}/%{name}/xml/*.rng
%{_datadir}/%{name}/xml/validate.py
%{_datadir}/%{name}/check-device-ids.py
%{_datadir}/%{name}/HIG.py
%{_datadir}/%{name}/killtimer.py
%{_datadir}/%{name}/OpenPrintingRequest.py
%{_datadir}/%{name}/SearchCriterion.py
%{_datadir}/%{name}/serversettings.py
%{_datadir}/%{name}/system-config-printer.py
%{_datadir}/%{name}/ToolbarSearchEntry.py
%{_datadir}/%{name}/userdefault.py
%{_datadir}/%{name}/applet.py
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
%{_datadir}/%{name}/__pycache__
%{_datadir}/%{name}/asyncconn.py
%{_datadir}/%{name}/asyncipp.py
%{_datadir}/%{name}/asyncpk1.py
%{_datadir}/%{name}/authconn.py
%{_datadir}/%{name}/config.py
%{_datadir}/%{name}/cupspk.py
%{_datadir}/%{name}/debug.py
%{_datadir}/%{name}/dnssdresolve.py
%{_datadir}/%{name}/errordialogs.py
%{_datadir}/%{name}/firewallsettings.py
%{_datadir}/%{name}/gtkinklevel.py
%{_datadir}/%{name}/gui.py
%{_datadir}/%{name}/installpackage.py
%{_datadir}/%{name}/install-printerdriver.py
%{_datadir}/%{name}/jobviewer.py
%{_datadir}/%{name}/monitor.py
%{_datadir}/%{name}/newprinter.py
%{_datadir}/%{name}/options.py
%{_datadir}/%{name}/optionwidgets.py
%{_datadir}/%{name}/PhysicalDevice.py
%{_datadir}/%{name}/ppdcache.py
%{_datadir}/%{name}/ppdippstr.py
%{_datadir}/%{name}/ppdsloader.py
%{_datadir}/%{name}/printerproperties.py
%{_datadir}/%{name}/probe_printer.py
%{_datadir}/%{name}/pysmb.py
%{_datadir}/%{name}/scp-dbus-service.py
%{_datadir}/%{name}/smburi.py
%{_datadir}/%{name}/statereason.py
%{_datadir}/%{name}/timedops.py

%dir %{py3_sitedir}/cupshelpers
%{py3_sitedir}/cupshelpers/__pycache__
%{py3_sitedir}/cupshelpers/__init__.py
%{py3_sitedir}/cupshelpers/config.py
%{py3_sitedir}/cupshelpers/cupshelpers.py
%{py3_sitedir}/cupshelpers/installdriver.py
%{py3_sitedir}/cupshelpers/openprinting.py
%{py3_sitedir}/cupshelpers/ppds.py
%{py3_sitedir}/cupshelpers/xmldriverprefs.py
%{py3_sitedir}/*.egg-info

%files udev
%defattr(644,root,root,755)
/lib/udev/rules.d/*-printers.rules
%attr(755,root,root) /lib/udev/udev-add-printer
%attr(755,root,root) /lib/udev/udev-configure-printer
%{systemdunitdir}/configure-printer@.service
