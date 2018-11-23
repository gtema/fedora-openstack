%global pypi_name bandit

Name:           python-%{pypi_name}
Version:        1.5.1
Release:        1%{?dist}
Summary:        Security oriented static analyser for python code

License:        None
URL:            https://bandit.readthedocs.io/en/latest/
Source0:        https://files.pythonhosted.org/packages/source/b/%{pypi_name}/%{pypi_name}-%{version}.tar.gz
BuildArch:      noarch

BuildRequires:  python2-devel
BuildConflicts: python2dist(coverage) = 4.4
BuildRequires:  python2dist(beautifulsoup4) >= 4.6.0
BuildRequires:  python2dist(coverage) >= 4.0
BuildRequires:  python2dist(fixtures) >= 3.0.0
BuildRequires:  python2dist(gitpython) >= 1.0.1
BuildRequires:  python2dist(hacking) >= 1.0.0
BuildRequires:  python2dist(mock) >= 2.0.0
BuildRequires:  python2dist(oslotest) >= 3.2.0
BuildRequires:  python2dist(pbr) >= 2.0.0
BuildRequires:  python2dist(pylint) = 1.4.5
BuildRequires:  python2dist(pyyaml) >= 3.12
BuildRequires:  python2dist(setuptools)
BuildRequires:  python2dist(six) >= 1.10.0
BuildRequires:  python2dist(stestr) >= 1.0.0
BuildRequires:  python2dist(stevedore) >= 1.20.0
BuildRequires:  python2dist(testscenarios) >= 0.4
BuildRequires:  python2dist(testtools) >= 2.2.0

BuildRequires:  python3-devel
BuildConflicts: python3dist(coverage) = 4.4
BuildRequires:  python3dist(beautifulsoup4) >= 4.6.0
BuildRequires:  python3dist(coverage) >= 4.0
BuildRequires:  python3dist(fixtures) >= 3.0.0
BuildRequires:  python3dist(gitpython) >= 1.0.1
BuildRequires:  python3dist(hacking) >= 1.0.0
BuildRequires:  python3dist(mock) >= 2.0.0
BuildRequires:  python3dist(oslotest) >= 3.2.0
BuildRequires:  python3dist(pbr) >= 2.0.0
BuildRequires:  python3dist(pylint) = 1.4.5
BuildRequires:  python3dist(pyyaml) >= 3.12
BuildRequires:  python3dist(setuptools)
BuildRequires:  python3dist(six) >= 1.10.0
BuildRequires:  python3dist(stestr) >= 1.0.0
BuildRequires:  python3dist(stevedore) >= 1.20.0
BuildRequires:  python3dist(testscenarios) >= 0.4
BuildRequires:  python3dist(testtools) >= 2.2.0
BuildRequires:  python3dist(sphinx)

%description
 .. image::

%package -n     python2-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python2-%{pypi_name}}

Requires:       python2dist(gitpython) >= 1.0.1
Requires:       python2dist(pyyaml) >= 3.12
Requires:       python2dist(setuptools)
Requires:       python2dist(six) >= 1.10.0
Requires:       python2dist(stevedore) >= 1.20.0
%description -n python2-%{pypi_name}
 .. image::

%package -n     python3-%{pypi_name}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypi_name}}

Requires:       python3dist(gitpython) >= 1.0.1
Requires:       python3dist(pyyaml) >= 3.12
Requires:       python3dist(setuptools)
Requires:       python3dist(six) >= 1.10.0
Requires:       python3dist(stevedore) >= 1.20.0
%description -n python3-%{pypi_name}
 .. image::

%package -n python-%{pypi_name}-doc
Summary:        bandit documentation
%description -n python-%{pypi_name}-doc
Documentation for bandit

%prep
%autosetup -n %{pypi_name}-%{version}
# Remove bundled egg-info
rm -rf %{pypi_name}.egg-info

%build
%py2_build
%py3_build
# generate html docs
PYTHONPATH=${PWD} sphinx-build-3 doc/source html
# remove the sphinx-build leftovers
rm -rf html/.{doctrees,buildinfo}

%install
# Must do the default python version install last because
# the scripts in /usr/bin are overwritten with every setup.py install.
%py2_install
rm -rf %{buildroot}%{_bindir}/*
%py3_install

%check
%{__python2} setup.py test
%{__python3} setup.py test

%files -n python2-%{pypi_name}
%license LICENSE
%doc README.rst
%{python2_sitelib}/%{pypi_name}
%{python2_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%files -n python3-%{pypi_name}
%license LICENSE
%doc README.rst
%{_bindir}/bandit
%{_bindir}/bandit-baseline
%{_bindir}/bandit-config-generator
%{python3_sitelib}/%{pypi_name}
%{python3_sitelib}/%{pypi_name}-%{version}-py?.?.egg-info

%files -n python-%{pypi_name}-doc
%doc html
%license LICENSE

%changelog
* Fri Nov 23 2018 Artem Goncharov <artem.goncharov@gmail.com> - 1.5.1-1
- Initial package.
