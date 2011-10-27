%{!?python_sitelib: %define python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%{!?pyver: %define pyver %(%{__python} -c "import sys ; print sys.version[:3]")}

%define module carbon

Summary:    Backend data caching and persistence daemon for Graphite
Name:       python-%{module}
Version:    0.9.7
Release:    0%{?dist}
Source:     %{module}-%{version}.tar.gz
Patch0:     %{module}-0.9.7-fhs-compliance.patch
License:    Apache Software License 2.0
Group:      Development/Libraries
Prefix:     %{_prefix}
BuildArch:  noarch
URL:        https://launchpad.net/graphite
Requires:   python-twisted
Requires:   python-txamqp

%description
UNKNOWN

%prep
%setup -n %{module}-%{version}
%patch0 -p1

%build
%{__python} setup.py build

%install
%{__python} setup.py install --root=$RPM_BUILD_ROOT

install -d -m 0755 $RPM_BUILD_ROOT%{_sysconfdir}
mv $RPM_BUILD_ROOT%{_prefix}/conf $RPM_BUILD_ROOT%{_sysconfdir}/graphite

install -d -m 0755 $RPM_BUILD_ROOT%{_localstatedir}/log/graphite/carbon-cache

find $RPM_BUILD_ROOT -type f -name \*~\* -exec rm {} +

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)
%dir %attr(0755,graphite,graphite) %{_sysconfdir}/graphite
%{_sysconfdir}/graphite/*.example
%{_prefix}/bin/carbon-cache.py
%{_prefix}/bin/carbon-relay.py
%{python_sitelib}/%{module}-%{version}-py%{pyver}.egg-info
%{python_sitelib}/%{module}/*.py
%{python_sitelib}/%{module}/*.pyc
%{python_sitelib}/%{module}/*.pyo
%{python_sitelib}/%{module}/amqp0-8.xml
%attr(0755,graphite,graphite) %{_localstatedir}/log/graphite
%attr(0755,graphite,graphite) %{_localstatedir}/log/graphite/carbon-cache

%changelog
* Wed Oct 26 2011 Jeffrey Goldschrafe <jeff@holyhandgrenade.org> - 0.9.7-1
- Initial package for Fedora
