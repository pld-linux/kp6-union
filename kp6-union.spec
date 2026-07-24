#
# Conditional build:
%bcond_with	tests		# test suite

%define		kf_ver		6.26.0
%define		kp_ver		%{version}
%define		qt_ver		6.9.0
%define		kpname		union
Summary:	Plasma and Qt widget style and window decorations for Plasma 5 and 6
Summary(pl.UTF-8):	Styl Plasmy i widżetów Qt oraz dekoracje okien dla Plasmy 5 i 6
Name:		kp6-%{kpname}
Version:	6.7.3
Release:	2
License:	GPL v2+/LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{version}/%{kpname}-%{version}.tar.xz
# Source0-md5:	dca8900cde84143d706e07fa2ae1a632
URL:		https://kde.org/
BuildRequires:	Qt6Core-devel >= %{qt_ver}
BuildRequires:	Qt6DBus-devel >= %{qt_ver}
BuildRequires:	Qt6Qml-devel >= %{qt_ver}
BuildRequires:	Qt6Quick-devel >= %{qt_ver}
BuildRequires:	Qt6ShaderTools-devel >= %{qt_ver}
BuildRequires:	Qt6Widgets-devel >= %{qt_ver}
BuildRequires:	cmake >= 3.25
BuildRequires:	cxx-rust-cssparser-devel >= 1.0.0
BuildRequires:	kf6-extra-cmake-modules >= %{kf_ver}
BuildRequires:	kf6-kcolorscheme-devel >= %{kf_ver}
BuildRequires:	kf6-kcoreaddons-devel >= %{kf_ver}
BuildRequires:	kf6-kguiaddons-devel >= %{kf_ver}
BuildRequires:	kf6-kiconthemes-devel >= %{kf_ver}
BuildRequires:	kf6-kirigami-devel >= %{kf_ver}
BuildRequires:	ninja
BuildRequires:	qt6-build >= %{qt_ver}
BuildRequires:	rpmbuild(macros) >= 2.004
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
%requires_eq_to Qt6Core Qt6Core-devel
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Plasma and Qt widget style and window decorations for Plasma 5 and 6.

%description -l pl.UTF-8
Styl Plasmy i widżetów Qt oraz dekoracje okien dla Plasmy 5 i 6.

%package devel
Summary:	Header files for %{kpname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for %{kpname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kpname}.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DBUILD_QT5=OFF \
	-DBUILD_QT6=ON

%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/union-ruleinspector
%ghost %{_libdir}/libUnion.so.6
%{_libdir}/libUnion.so.*.*
%ghost %{_libdir}/libUnionQuickImpl.so.6
%{_libdir}/libUnionQuickImpl.so.*.*
%ghost %{_libdir}/libUnionQuickStyle.so.6
%{_libdir}/libUnionQuickStyle.so.*.*
%{_libdir}/qt6/plugins/kf6/kirigami/platform/org.kde.union.so
%{_libdir}/qt6/plugins/styles/UnionWidgetsStyle.so
%{_libdir}/qt6/plugins/union
%{_libdir}/qt6/qml/org/kde/kirigami/styles/org.kde.union
%{_libdir}/qt6/qml/org/kde/union
%{_datadir}/kstyle/themes/union.themerc
%{_datadir}/qlogging-categories6/union.categories
%{_datadir}/union

%files devel
%defattr(644,root,root,755)
%{_includedir}/union
%{_libdir}/cmake/Union
%{_libdir}/libUnion.so
