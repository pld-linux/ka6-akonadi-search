# TODO: Corrosion (for safe parsing of html emails) https://github.com/corrosion-rs/corrosion
#
# Conditional build:
%bcond_with	tests		# test suite

%define		kdeappsver	25.12.2
# packages version, not cmake config version (which is 6.2.2)
%define		ka_ver		%{version}
%define		kf_ver		6.3.0
%define		qt_ver		6.6.0
%define		kaname		akonadi-search
Summary:	Akonadi Search
Summary(pl.UTF-8):	Komponent wyszukiwania dla Akonadi
Name:		ka6-%{kaname}
Version:	25.12.2
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	8415969b50c78f77bfc9c2c461672b17
URL:		https://kde.org/
BuildRequires:	Qt6Core-devel >= %{qt_ver}
BuildRequires:	Qt6Test-devel >= %{qt_ver}
BuildRequires:	cmake >= 3.20
BuildRequires:	gettext-devel
BuildRequires:	ka6-akonadi-devel >= %{ka_ver}
BuildRequires:	ka6-akonadi-mime-devel >= %{ka_ver}
BuildRequires:	ka6-kmime-devel >= %{ka_ver}
BuildRequires:	kf6-extra-cmake-modules >= %{kf_ver}
BuildRequires:	kf6-kcalendarcore-devel >= %{kf_ver}
BuildRequires:	kf6-kcmutils-devel >= %{kf_ver}
BuildRequires:	kf6-kconfig-devel >= %{kf_ver}
BuildRequires:	kf6-kcontacts-devel >= %{kf_ver}
BuildRequires:	kf6-kcoreaddons-devel >= %{kf_ver}
BuildRequires:	kf6-kcrash-devel >= %{kf_ver}
BuildRequires:	kf6-kdbusaddons-devel >= %{kf_ver}
BuildRequires:	kf6-ki18n-devel >= %{kf_ver}
BuildRequires:	kf6-kio-devel >= %{kf_ver}
BuildRequires:	kf6-krunner-devel >= %{kf_ver}
BuildRequires:	kf6-ktextaddons-devel >= 1.8.0
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qt_ver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	shared-mime-info
BuildRequires:	tar >= 1:1.22
BuildRequires:	xapian-core-devel
BuildRequires:	xz
Requires:	Qt6Core >= %{qt_ver}
Requires:	ka6-akonadi >= %{ka_ver}
Requires:	ka6-akonadi-mime >= %{ka_ver}
Requires:	ka6-kmime >= %{ka_ver}
Requires:	kf6-kcmutils >= %{kf_ver}
Requires:	kf6-kconfig >= %{kf_ver}
Requires:	kf6-kcontacts >= %{kf_ver}
Requires:	kf6-kcoreaddons >= %{kf_ver}
Requires:	kf6-ki18n >= %{kf_ver}
Requires:	kf6-krunner >= %{kf_ver}
Requires:	kf6-ktextaddons >= 1.8.0
%requires_eq_to Qt6Core Qt6Core-devel
Obsoletes:	ka5-akonadi-search < 24
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libraries and daemons to implement searching in Akonadi.

%description -l pl.UTF-8
Biblioteki i demony do implementowania wyszukiwania w Akonadi.

%package devel
Summary:	Header files for %{kaname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kaname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	Qt6Core-devel >= %{qt_ver}
Requires:	ka6-akonadi-devel >= %{ka_ver}
Requires:	ka6-akonadi-mime-devel >= %{ka_ver}
Requires:	ka6-kmime-devel >= %{ka_ver}
Requires:	kf6-kcalendarcore-devel >= %{kf_ver}
Requires:	kf6-kcontacts-devel >= %{kf_ver}
Requires:	kf6-kcoreaddons-devel >= %{kf_ver}
Obsoletes:	ka5-akonadi-search-devel < 24

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

%find_lang akonadi_search

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files -f akonadi_search.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/akonadi_html_to_text
%attr(755,root,root) %{_bindir}/akonadi_indexing_agent
%{_libdir}/libKPim6AkonadiSearchCore.so.*.*.*
%ghost %{_libdir}/libKPim6AkonadiSearchCore.so.6
%{_libdir}/libKPim6AkonadiSearchDebug.so.*.*.*
%ghost %{_libdir}/libKPim6AkonadiSearchDebug.so.6
%{_libdir}/libKPim6AkonadiSearchPIM.so.*.*.*
%ghost %{_libdir}/libKPim6AkonadiSearchPIM.so.6
%{_libdir}/libKPim6AkonadiSearchXapian.so.*.*.*
%ghost %{_libdir}/libKPim6AkonadiSearchXapian.so.6
%{_libdir}/qt6/plugins/kf6/krunner/kcms/kcm_krunner_pimcontacts.so
%{_libdir}/qt6/plugins/kf6/krunner/krunner_pimcontacts.so
%{_libdir}/qt6/plugins/pim6/akonadi/akonadi_search_plugin.so
%{_libdir}/qt6/plugins/pim6/akonadi/calendarsearchstore.so
%{_libdir}/qt6/plugins/pim6/akonadi/contactsearchstore.so
%{_libdir}/qt6/plugins/pim6/akonadi/emailsearchstore.so
%{_libdir}/qt6/plugins/pim6/akonadi/notesearchstore.so
%{_datadir}/akonadi/agents/akonadiindexingagent.desktop
%{_datadir}/qlogging-categories6/akonadi-search.categories
%{_datadir}/qlogging-categories6/akonadi-search.renamecategories

%files devel
%defattr(644,root,root,755)
%{_libdir}/libKPim6AkonadiSearchCore.so
%{_libdir}/libKPim6AkonadiSearchDebug.so
%{_libdir}/libKPim6AkonadiSearchPIM.so
%{_libdir}/libKPim6AkonadiSearchXapian.so
%{_includedir}/KPim6/AkonadiSearch
%{_libdir}/cmake/KPim6AkonadiSearch
