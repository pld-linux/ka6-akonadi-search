#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	24.05.0
%define		kframever	5.94.0
%define		qtver		5.15.2
%define		kaname		akonadi-search
Summary:	Akonadi Search
Name:		ka6-%{kaname}
Version:	24.05.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	ce25ae7c890d690293938425a03ee35f
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Test-devel >= 5.9.0
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	ka6-akonadi-devel >= %{kdeappsver}
BuildRequires:	ka6-akonadi-mime-devel >= %{kdeappsver}
BuildRequires:	ka6-kmime-devel >= %{kdeappsver}
BuildRequires:	kf6-extra-cmake-modules >= %{kframever}
BuildRequires:	kf6-kcalendarcore-devel >= %{kframever}
BuildRequires:	kf6-kcmutils-devel >= %{kframever}
BuildRequires:	kf6-kconfig-devel >= %{kframever}
BuildRequires:	kf6-kcontacts-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kio-devel >= %{kframever}
BuildRequires:	kf6-krunner-devel >= %{kframever}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xapian-core-devel
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libraries and daemons to implement searching in Akonadi.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kaname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kaname}.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON
%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif


%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/akonadi_html_to_text
%attr(755,root,root) %{_bindir}/akonadi_indexing_agent
%attr(755,root,root) %{_libdir}/libKPim6AkonadiSearchCore.so.*.*
%ghost %{_libdir}/libKPim6AkonadiSearchCore.so.6
%attr(755,root,root) %{_libdir}/libKPim6AkonadiSearchDebug.so.*.*
%ghost %{_libdir}/libKPim6AkonadiSearchDebug.so.6
%attr(755,root,root) %{_libdir}/libKPim6AkonadiSearchPIM.so.*.*
%ghost %{_libdir}/libKPim6AkonadiSearchPIM.so.6
%attr(755,root,root) %{_libdir}/libKPim6AkonadiSearchXapian.so.*.*
%ghost %{_libdir}/libKPim6AkonadiSearchXapian.so.6
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/krunner/kcms/kcm_krunner_pimcontacts.so
%attr(755,root,root) %{_libdir}/qt6/plugins/kf6/krunner/krunner_pimcontacts.so
%attr(755,root,root) %{_libdir}/qt6/plugins/pim6/akonadi/akonadi_search_plugin.so
%attr(755,root,root) %{_libdir}/qt6/plugins/pim6/akonadi/calendarsearchstore.so
%attr(755,root,root) %{_libdir}/qt6/plugins/pim6/akonadi/contactsearchstore.so
%attr(755,root,root) %{_libdir}/qt6/plugins/pim6/akonadi/emailsearchstore.so
%attr(755,root,root) %{_libdir}/qt6/plugins/pim6/akonadi/notesearchstore.so
%{_datadir}/akonadi/agents/akonadiindexingagent.desktop
%{_datadir}/qlogging-categories6/akonadi-search.categories
%{_datadir}/qlogging-categories6/akonadi-search.renamecategories

%files devel
%defattr(644,root,root,755)
%{_includedir}/KPim6/AkonadiSearch
%{_libdir}/cmake/KPim6AkonadiSearch
%{_libdir}/libKPim6AkonadiSearchCore.so
%{_libdir}/libKPim6AkonadiSearchDebug.so
%{_libdir}/libKPim6AkonadiSearchPIM.so
%{_libdir}/libKPim6AkonadiSearchXapian.so
