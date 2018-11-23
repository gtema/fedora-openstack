
Name:           python-os-service-types
Version:        1.3.0
Release:        1%{?dist}
Summary:        Python library for consuming OpenStack sevice-types-authority data
License:        ASL 2.0
Group:          Development/Languages/Python
URL:            https://docs.openstack.org/developer/os-service-types
Source0:        https://files.pythonhosted.org/packages/source/o/os-service-types/os-service-types-%{version}.tar.gz
# https://review.openstack.org/599979
Patch0:         0001-Use-keystoneauth-only-in-applicable-test.patch
BuildRequires:  openstack-macros
BuildRequires:  python-oslotest python3-oslotest
BuildRequires:  python-pbr python3-pbr
BuildRequires:  python-subunit python3-subunit
BuildRequires:  python-requests-mock python3-requests-mock
BuildRequires:  python-stestr python3-stestr
BuildRequires:  python-testscenarios python3-testscenarios
Requires:       python-pbr
BuildArch:      noarch
%python_subpackages

%description
The OpenStack Service Types Authority contains information about official
OpenStack services and their historical service-type aliases.
The data is in JSON and the latest data should always be used. This simple
library exists to allow for easy consumption of the data, along with a built-in
version of the data to use in case network access is for some reason not
possible and local caching of the fetched data.

%package -n os-service-types-doc
Summary:        Documentation for OpenStack os-service-types library
BuildRequires:  python-sphinx
BuildRequires:  python-openstackdocstheme

%description -n os-service-types-doc
The OpenStack Service Types Authority contains information about official
OpenStack services and their historical service-type aliases.
The data is in JSON and the latest data should always be used. This simple
library exists to allow for easy consumption of the data, along with a built-in
version of the data to use in case network access is for some reason not
possible and local caching of the fetched data.
This package contains the documentation.

%prep
%autosetup -p1 -n os-service-types-1.3.0
%py_req_cleanup
sed -i 's/^warning-is-error.*/warning-is-error = 0/g' setup.cfg
# The TestRemote test cases must be excluded because they introduce a circular
# dependency on python-keystoneauth1.
# Using --black-regex with stestr is not enough because the problem occurs when
# keystoneauth is imported, not when the test is run.
rm os_service_types/tests/test_remote.py

%build
%{python_build}

# generate html docs
%{__python2} setup.py build_sphinx
# remove the sphinx-build leftovers
rm -rf doc/build/html/.{doctrees,buildinfo}

%install
%{python_install}

%check
export OS_TEST_PATH=os_service_types/tests
%python_exec -m stestr.cli run

%files %{python_files}
%license LICENSE
%doc README.rst ChangeLog
%{python_sitelib}/os_service_types
%{python_sitelib}/*.egg-info

%files -n os-service-types-doc
%license LICENSE
%doc doc/build/html

%changelog
