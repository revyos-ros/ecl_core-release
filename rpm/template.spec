%bcond_without tests
%bcond_without weak_deps

%global __os_install_post %(echo '%{__os_install_post}' | sed -e 's!/usr/lib[^[:space:]]*/brp-python-bytecompile[[:space:]].*$!!g')
%global __provides_exclude_from ^/opt/ros/jazzy/.*$
%global __requires_exclude_from ^/opt/ros/jazzy/.*$

Name:           ros-jazzy-ecl-core
Version:        1.2.1
Release:        6%{?dist}%{?release_suffix}
Summary:        ROS ecl_core package

License:        BSD
URL:            http://www.ros.org/wiki/ecl_core
Source0:        %{name}-%{version}.tar.gz

Requires:       ros-jazzy-ecl-command-line
Requires:       ros-jazzy-ecl-concepts
Requires:       ros-jazzy-ecl-containers
Requires:       ros-jazzy-ecl-converters
Requires:       ros-jazzy-ecl-core-apps
Requires:       ros-jazzy-ecl-devices
Requires:       ros-jazzy-ecl-eigen
Requires:       ros-jazzy-ecl-exceptions
Requires:       ros-jazzy-ecl-formatters
Requires:       ros-jazzy-ecl-geometry
Requires:       ros-jazzy-ecl-ipc
Requires:       ros-jazzy-ecl-linear-algebra
Requires:       ros-jazzy-ecl-math
Requires:       ros-jazzy-ecl-mpl
Requires:       ros-jazzy-ecl-sigslots
Requires:       ros-jazzy-ecl-statistics
Requires:       ros-jazzy-ecl-streams
Requires:       ros-jazzy-ecl-threads
Requires:       ros-jazzy-ecl-time
Requires:       ros-jazzy-ecl-type-traits
Requires:       ros-jazzy-ecl-utilities
Requires:       ros-jazzy-ros-workspace
BuildRequires:  ros-jazzy-ament-cmake-ros
BuildRequires:  ros-jazzy-ros-workspace
Provides:       %{name}-devel = %{version}-%{release}
Provides:       %{name}-doc = %{version}-%{release}
Provides:       %{name}-runtime = %{version}-%{release}

%description
A set of tools and interfaces extending the capabilities of c++ to provide a
lightweight, consistent interface with a focus for control programming.

%prep
%autosetup -p1

%build
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/jazzy/setup.sh" ]; then . "/opt/ros/jazzy/setup.sh"; fi
mkdir -p .obj-%{_target_platform} && cd .obj-%{_target_platform}
%cmake3 \
    -UINCLUDE_INSTALL_DIR \
    -ULIB_INSTALL_DIR \
    -USYSCONF_INSTALL_DIR \
    -USHARE_INSTALL_PREFIX \
    -ULIB_SUFFIX \
    -DCMAKE_INSTALL_PREFIX="/opt/ros/jazzy" \
    -DAMENT_PREFIX_PATH="/opt/ros/jazzy" \
    -DCMAKE_PREFIX_PATH="/opt/ros/jazzy" \
    -DSETUPTOOLS_DEB_LAYOUT=OFF \
%if !0%{?with_tests}
    -DBUILD_TESTING=OFF \
%endif
    ..

%make_build

%install
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/jazzy/setup.sh" ]; then . "/opt/ros/jazzy/setup.sh"; fi
%make_install -C .obj-%{_target_platform}

%if 0%{?with_tests}
%check
# Look for a Makefile target with a name indicating that it runs tests
TEST_TARGET=$(%__make -qp -C .obj-%{_target_platform} | sed "s/^\(test\|check\):.*/\\1/;t f;d;:f;q0")
if [ -n "$TEST_TARGET" ]; then
# In case we're installing to a non-standard location, look for a setup.sh
# in the install tree and source it.  It will set things like
# CMAKE_PREFIX_PATH, PKG_CONFIG_PATH, and PYTHONPATH.
if [ -f "/opt/ros/jazzy/setup.sh" ]; then . "/opt/ros/jazzy/setup.sh"; fi
CTEST_OUTPUT_ON_FAILURE=1 \
    %make_build -C .obj-%{_target_platform} $TEST_TARGET || echo "RPM TESTS FAILED"
else echo "RPM TESTS SKIPPED"; fi
%endif

%files
/opt/ros/jazzy

%changelog
* Thu Sep 26 2024 Daniel Stonier <d.stonier@gmail.com> - 1.2.1-6
- Autogenerated by Bloom

