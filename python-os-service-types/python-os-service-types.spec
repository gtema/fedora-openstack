%global pypi_name os-service-types
%global module_name os_service_types

%if 0%{?fedora}
%global with_python3 1
%endif

%global common_desc \
OsServiceTypes is a Python library for consuming OpenStack \
sevice-types-authority data. \
The OpenStack Service Types Authority contains information about official \
OpenStack services and their historical service-type aliases. \
The data is in JSON and the latest data should always be used. This simple \
library exists to allow for easy consumption of the data, along with a built-in \
version of the data to use in case network access is for some reason not \
possible and local caching of the fetched data.

Name:           python-%{pypi_name}
Version:        1.3.0
Release:        1%{?dist}
Summary:        Python library for consuming OpenStack sevice-types-authority data

License:        ASL 2.0
URL:            http://www.openstack.org/
Source0:        https://tarballs.openstack.org/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch
# https://review.openstack.org/599979
Patch0:         0001-Use-keystoneauth-only-in-applicable-test.patch

BuildRequires:  git

%description
%{common_desc}

%if 0%{?with_python2}
%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}

BuildRequires:  python2-devel
BuildRequires:  python2-setuptools
BuildRequires:  python2-keystoneauth1 >= 3.4.0
BuildRequires:  python2-oslotest >= 3.2.0
#BuildRequires:  python2-openstackdocstheme >= 1.18.1
BuildRequires:  python2-pbr >= 2.0.0
BuildRequires:  python2-reno >= 2.5.0
BuildRequires:  python2-requests-mock >= 1.2.0
BuildRequires:  python2-six >= 1.10.0
BuildRequires:  python2-stestr >= 2.0.0
BuildRequires:  python2-subunit >= 1.0.0
BuildRequires:  python2-testscenarios >= 0.4

Requires:       python2-pbr >= 2.0.0
%description -n python2-%{pypi_name}
%{common_desc}
%endif

%if 0%{?with_python3}
%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-keystoneauth1 >= 3.4.0
#BuildRequires:  python3-openstackdocstheme >= 1.18.1
BuildRequires:  python3-oslotest >= 3.2.0
BuildRequires:  python3-pbr >= 2.0.0
BuildRequires:  python3-reno >= 2.5.0
BuildRequires:  python3-requests-mock >= 1.2.0
BuildRequires:  python3-six >= 1.10.0
BuildRequires:  python3-stestr >= 2.0.0
BuildRequires:  python3-subunit >= 1.0.0
BuildRequires:  python3-testscenarios >= 0.4

Requires:       python3-pbr >= 2.0.0
%description -n python3-%{pypi_name}
%{common_desc}
%endif

%package -n python-%{pypi_name}-doc
Summary:        %{pypi_name} documentation

%if 0%{?with_python3}
BuildRequires:  python3-openstackdocstheme >= 1.18.1
BuildRequires:  python3-sphinx
%else
BuildRequires:  python2-openstackdocstheme >= 1.18.1
BuildRequires:  python2-sphinx
%endif

%description -n python-%{pypi_name}-doc
%{common_desc}


Documentation for %{pypi_name}

%prep
%autosetup -n %{pypi_name}-%{version} -S git
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info
sed -i 's/^warning-is-error.*/warning-is-error = 0/g' setup.cfg
# The TestRemote test cases must be excluded because they introduce a circular
# dependency on python-keystoneauth1.
# Using --black-regex with stestr is not enough because the problem occurs when
# keystoneauth is imported, not when the test is run.
rm os_service_types/tests/test_remote.py
rm -rf *requirements.txt

%build
%if 0%{?with_python3}
%py3_build
%endif
%if 0%{?with_python2}
%py2_build
%endif
# generate html docs
%if 0%{?with_python3}
%{__python3} setup.py build_sphinx -b html
%else
%{__python2} setup.py build_sphinx -b html
%endif
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%if 0%{?with_python3}
%py3_install
%endif

%if 0%{?with_python2}
%py2_install
%endif

%check
%if 0%{?with_python3}
%{__python3} -m stestr.cli run
%endif

%if 0%{?with_python2}
%{__python2} -m stestr.cli run
%endif

%if 0%{?with_python2}
%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst doc/source/readme.rst
%{python2_sitelib}/%{module_name}
%{python2_sitelib}/%{module_name}-%{version}-py?.?.egg-info
%endif

%if 0%{?with_python3}
%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst doc/source/readme.rst
%{python3_sitelib}/%{module_name}
%{python3_sitelib}/%{module_name}-%{version}-py?.?.egg-info
%endif

%files -n python-%{pypi_name}-doc
%license LICENSE
%doc doc/build/html

%changelog
* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.1.0-6
- Rebuilt for Python 3.7

* Fri Feb 09 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.1.0-5
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Wed Oct 11 2017 ykarel <ykarel@redhat.com> - 1.1.0-3
- Fix rpmlint warnings and use python2-subunit
* Wed Oct 11 2017 ykarel <ykarel@redhat.com> - 1.1.0-2
- Incorporate some nits in spec from rdo-review
* Tue Oct 10 2017 ykarel <ykarel@redhat.com> - 1.1.0-1
- Initial package.
