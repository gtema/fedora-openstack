# Tests requiring Internet connections are disabled by default
# pass --with internet to run them (e.g. when doing a local rebuild
# for sanity checks before committing)
%bcond_with internet


%global pypiname tox
Name:           python-%{pypiname}
Version:        3.5.3
Release:        1%{?dist}
Summary:        Virtualenv-based automation of test activities

# file toxbootstrap.py is licensed under MIT License
License:        GPLv2+ and MIT
URL:            http://tox.testrun.org/
Source0:        https://files.pythonhosted.org/packages/source/t/%{pypiname}/%{pypiname}-%{version}.tar.gz
BuildArch:      noarch

%description
Tox as is a generic virtualenv management and test command line tool you
can use for:

 - checking your package installs correctly with different Python versions
   and interpreters
 - running your tests in each of the environments, configuring your test tool
   of choice
 - acting as a frontend to Continuous Integration servers, greatly reducing
   boilerplate and merging CI and shell-based testing.


%package -n python3-%{pypiname}
Summary:        %{summary}
%{?python_provide:%python_provide python3-%{pypiname}}
Provides:       %{pypiname} = %{version}-%{release}
BuildRequires:  python3-devel
BuildRequires:  python3-setuptools
BuildRequires:  python3-setuptools_scm

# Recommend "all the Pythons"
# Why? Tox exists to enable developers to test libraries against various Python
# versions, with just "dnf install tox" and a config file.
# See: https://developer.fedoraproject.org/tech/languages/python/python-installation.html#using-virtualenv
# Tox itself runs on the system python3 (i.e. %%{python3_version},
# however it launches other Python versions as subprocesses.
# It recommends all Python versions it supports. (This is an exception to
# the rule that Fedora packages may not require the alternative interpreters.)
Recommends:     python27
Recommends:     python34
Recommends:     python35
Recommends:     python36
Recommends:     python37
Recommends:     pypy-devel
Recommends:     pypy3-devel
Recommends:     python2-devel
Recommends:     python3-devel

# Replace the python2 version
Obsoletes:      python2-tox < 2.9.1-4

%if %{with internet}
# for tests
BuildRequires:  python3-py
BuildRequires:  python3-pytest
BuildRequires:  python3-virtualenv
%endif

%?python_enable_dependency_generator

%description -n python3-%{pypiname}
Tox as is a generic virtualenv management and test command line tool you
can use for:

 - checking your package installs correctly with different Python versions
   and interpreters
 - running your tests in each of the environments, configuring your test tool
   of choice
 - acting as a frontend to Continuous Integration servers, greatly reducing
   boilerplate and merging CI and shell-based testing.

%prep
%setup -q -n %{pypiname}-%{version}

# remove bundled egg-info
rm -rf %{pypiname}.egg-info

%build
%py3_build


%install
%py3_install

# if internet connection available, run tests
%if %{with internet}
%check
TOXENV=py%{python3_version_nodots} %{__python3} setup.py test
%endif

%files -n python3-%{pypiname}
%{_bindir}/%{pypiname}
%{_bindir}/%{pypiname}-quickstart
%{python3_sitelib}/%{pypiname}
%{python3_sitelib}/%{pypiname}-%{version}-py%{python3_version}.egg-info

%changelog
* Thu Nov 22 2018 Artem Goncharov <artem.goncharov@gmail.com> - 3.5.3-1
- upgrade to 3.5.3 version

* Thu Nov 01 2018 Matthias Runge <mrunge@redhat.com> - 3.0.0-6
- remove and revert the change to recommend python 2.7 (rhbz#1645025)

* Tue Aug 28 2018 Miro Hrončok <mhroncok@redhat.com> - 3.0.0-4
- Don't recommend Python 2.6, it doesn't work with tox 3

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 3.0.0-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Mon Jul 02 2018 Miro Hrončok <mhroncok@redhat.com> - 3.0.0-2
- Rebuilt for Python 3.7

* Mon Jul 02 2018 Matthias Runge <mrunge@redhat.com> - 3.0.0-1
- upgrade to 3.0.0

* Sun Jun 17 2018 Miro Hrončok <mhroncok@redhat.com> - 2.9.1-7
- Rebuilt for Python 3.7

* Tue May 15 2018 Miro Hrončok <mhroncok@redhat.com> - 2.9.1-6
- Remove the python2 version once again
- Stop recommending python33 (it's retired)

* Mon May 07 2018 Miro Hrončok <mhroncok@redhat.com> - 2.9.1-5
- Add python2 back, see #1575667

* Mon Apr 30 2018 Miro Hrončok <mhroncok@redhat.com> - 2.9.1-4
- Remove the python2 version

* Thu Mar 15 2018 Miro Hrončok <mhroncok@redhat.com> - 2.9.1-3
- Switch to automatic dependency generator (also fixes #1556164)
- Recommend python37

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2.9.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 29 2018 Matthias Runge <mrunge@redhat.com> - 2.9.1-1
- update to 2.9.1

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.7.0-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Tue Apr 25 2017 Matthias Runge <mrunge@redhat.com> - 2.7.0-1
- upgrade to 2.7.0

* Sun Apr 09 2017 Miro Hrončok <mhroncok@redhat.com> - 2.3.1-8
- Recommend the devel subpackages of Pythons (so tox works with extension modules)

* Tue Feb 14 2017 Miro Hrončok <mhroncok@redhat.com> - 2.3.1-7
- Recommend python36

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 2.3.1-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 2.3.1-5
- Rebuild for Python 3.6

* Mon Oct 10 2016 Miro Hrončok <mhroncok@redhat.com> - 2.3.1-4
- Recommend "all the Pythons"

* Thu Aug 11 2016 Miro Hrončok <mhroncok@redhat.com> - 2.3.1-3
- /usr/bin/tox is Python3
- Python 2 subpackage is python2-tox
- Run the tests also on Python 3
- Update Source URL and URL
- Use modern macros
- Get rid of Fedora 17 checks

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 2.3.1-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Mon Feb 29 2016 Matthias Runge <mrunge@redhat.com> - 2.3.1-1
- update to 2.3.1

* Thu Feb 04 2016 Fedora Release Engineering <releng@fedoraproject.org> - 2.1.1-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_24_Mass_Rebuild

* Thu Nov 12 2015 Kalev Lember <klember@redhat.com> - 2.1.1-3
- Rebuilt for https://fedoraproject.org/wiki/Changes/python3.5

* Tue Aug 25 2015 Matthias Runge <mrunge@redhat.com> - 2.1.1-2
- add requirement: python-pluggy

* Tue Aug 18 2015 Matthias Runge <mrunge@redhat.com> - 2.1.1-1
- update to 2.1.1

* Thu Jun 18 2015 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.8.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_23_Mass_Rebuild

* Tue Dec 16 2014 Matthias Runge <mrunge@redhat.com> - 1.8.1-1
- update to 1.8.1

* Wed Aug 13 2014 Matthias Runge <mrunge@redhat.com> - 1.7.1-3
- Fix ConfigError: ConfigError: substitution key 'posargs' not found
  (rhbz#1127961, rhbz#1128562)

* Wed Jul 30 2014 Matthias Runge <mrunge@redhat.com> - 1.7.1-2
- require virtualenv >= 1.11.2 (rhbz#1122603)

* Tue Jul 08 2014 Matthias Runge <mrunge@redhat.com> - 1.7.1-1
- update to 1.7.1 (rhbz#111797)

* Sat Jun 07 2014 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.6.1-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_21_Mass_Rebuild

* Tue Sep 24 2013 Matthias Runge <mrunge@redhat.com> - 1.6.1-1
- update to 1.6.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-9
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.4.2-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Wed Nov 14 2012 Matthias Runge <mrunge@redhat.com> - 1.4.2-7
- add requires python-py, python-virtualenv (rhbz#876246)

* Thu Oct 18 2012 Matthias Runge <mrunge@redhat.com> - 1.4.2-6
- change license to GPLv2+ and MIT

* Tue Oct 16 2012 Matthias Runge <mrunge@redhat.com> - 1.4.2-5
- totally disable python3 support for now

* Fri Oct 12 2012 Matthias Runge <mrunge@redhat.com> - 1.4.2-4
- conditionalize checks, as internet connection required, not available on koji

* Thu Oct 11 2012 Matthias Runge <mrunge@redhat.com> - 1.4.2-3
- buildrequirement: virtualenv
- disable python3-tests because of missing build-requirement python3-virtualenv

* Wed Oct 10 2012 Matthias Runge <mrunge@redhat.com> - 1.4.2-2
- include tests

* Tue Oct 09 2012 Matthias Runge <mrunge@redhat.com> - 1.4.2-1
- initial packaging
