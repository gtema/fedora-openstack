%if 0%{?rhel}
%global rdo 1
%endif
Name:           openstack-macros
Version:        2018.2.1
Release:        0
Summary:        OpenStack Packaging - RPM Macros
License:        ASL 2.0
Group:          Development/Libraries/Python
URL:            https://wiki.openstack.org/wiki/Rpm-packaging
Source1:        macros.openstack-common
Source2:        macros.openstack-suse
Source3:        macros.openstack-rdo
Source4:        macros.openstack-fedora
# the singlespec macros are a copy of https://github.com/openSUSE/python-rpm-macros
Source5:        macros.openstack-singlespec
BuildArch:      noarch
%if 0%{?rdo}
Obsoletes:     rdo-rpm-macros <= 1-3
# Fake NVR to avoid dealing with epochs
# just bump release field
Provides:      rdo-rpm-macros = 1-4
%endif

%description
This package provides OpenStack RPM macros. You need it to build OpenStack
packages.

%prep

%build

%install
install -D -m644 %{SOURCE1} %{buildroot}%{_sysconfdir}/rpm/macros.openstack-common
install -D -m644 %{SOURCE5} %{buildroot}%{_sysconfdir}/rpm/macros.openstack-singlespec
%if 0%{?suse_version}
install -D -m644 %{SOURCE2} %{buildroot}%{_sysconfdir}/rpm/macros.openstack-suse
%endif
%if 0%{?rdo}
install -D -m644 %{SOURCE3} %{buildroot}%{_sysconfdir}/rpm/macros.openstack-rdo
%endif
%if 0%{?fedora}
install -D -m644 %{SOURCE4} %{buildroot}%{_sysconfdir}/rpm/macros.openstack-fedora
%endif

%files
%{_sysconfdir}/rpm/macros.openstack-common
%{_sysconfdir}/rpm/macros.openstack-singlespec
%if 0%{?suse_version}
%{_sysconfdir}/rpm/macros.openstack-suse
%endif
%if 0%{?rdo}
%{_sysconfdir}/rpm/macros.openstack-rdo
%endif
%if 0%{?fedora}
%{_sysconfdir}/rpm/macros.openstack-fedora
%endif

%changelog