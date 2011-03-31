Summary: mod_wsgi Apache module
License: Apache License 2.0
Name: mod_wsgi
Version: 3.2
Release: 1
Source: http://modwsgi.googlecode.com/files/%{name}-%{version}.tar.gz
Group: Devel
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

Requires: python httpd httpd-devel

%description
The aim of mod_wsgi is to implement a simple to use Apache module which can host any Python application which supports the Python WSGI interface. The module would be suitable for use in hosting high performance production web sites, as well as your average self managed personal sites running on web hosting services. 

%pre
%prep
%setup -q
%configure
make
%install
make DESTDIR=%buildroot install

%files
%{_libdir}/httpd/modules/mod_wsgi.so
