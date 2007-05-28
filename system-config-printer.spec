Summary:	A graphical interface for configuring printers
Summary(pl.UTF-8):	Graficzny interfejs do zarządzania drukarkami
Name:		system-config-printer
Version:	0.7.65
Release:	1
License:	GPL v2
Group:		X11/Application
Source0:	http://cyberelk.net/tim/data/system-config-printer/%{name}-%{version}.tar.bz2
# Source0-md5:	c076dee6f8ecc0819a9d397b8f204e74
Patch0:		%{name}-desktop.patch
URL:		http://cyberelk.net/tim/software/system-config-printer/
BuildRequires:	autoconf
BuildRequires:	automake
BuildRequires:	desktop-file-utils
BuildRequires:	gettext-devel
BuildRequires:	intltool
BuildRequires:	python-devel
BuildRequires:	xmlto
Requires:	eggcups
Requires:	gksu
Requires:	python-PyXML
Requires:	python-pycups >= 1.9.22
Requires:	python-pynotify
Requires:	python-rhpl
%pyrequires_eq	python-libs
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The purpose of the tool is to configure a CUPS server (often the
local machine) using the CUPS API. The tool is written in Python,
using pygtk for the graphical parts and with some Python bindings
(pycups) for the CUPS API.

%description -l pl.UTF-8
To narzędzie służy do konfigurowania serwera CUPS (zwykle na
maszynie lokalnej) przy użyciu API CUPS-a. Narzędzie jest napisane w
Pythonie z użyciem pygtk do części graficznych i dowiązań Pythona
(pycups) do API CUPS-a.

%prep
%setup -q
%patch0 -p1

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

%py_comp $RPM_BUILD_ROOT%{_datadir}/system-config-printer
%py_ocomp $RPM_BUILD_ROOT%{_datadir}/system-config-printer

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}.lang
%defattr(644,root,root,755)
%doc AUTHORS ChangeLog NEWS README TODO
%attr(755,root,root) %{_bindir}/system-config-printer-applet
%attr(755,root,root) %{_sbindir}/system-config-printer
%{_sysconfdir}/xdg/autostart/*.desktop
%dir %{_datadir}/system-config-printer
%{_datadir}/system-config-printer/*.glade
%{_datadir}/system-config-printer/*.png
%attr(755,root,root) %{_datadir}/system-config-printer/*.py*
%{_mandir}/man*/*
%{_desktopdir}/*.desktop
