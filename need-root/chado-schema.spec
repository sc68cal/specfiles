#$Id: chado-schema.spec.in,v 1.7 2009/03/26 00:32:18 allenday Exp $
%define gmod_root /var/lib/gmod/src/chado

Summary: Chado, a modular relational schema at the core of the Generic Model Organism Database (GMOD) project.
Name: chado-schema
Version: 1.0
Epoch: 0
Release: 1.8.%{distro}
License: GPL
Group: Databases/Bioinformatics
Packager: Sean Collins <contact@seanmcollins.com>
URL: http://www.gmod.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch
AutoReq: no

Requires: perl-go-perl

Source0: gmod-%{version}.tar.gz

%description
Chado, a modular relational schema at the core of the Generic Model Organism Database (GMOD) project. 
This package only contains the schema.

%prep
%setup -n gmod-%{version}

%build

%install
mkdir -p %{buildroot}%{gmod_root}
mv modules $RPM_BUILD_ROOT%{gmod_root}
find $RPM_BUILD_ROOT%{gmod_root} -type f | sed "s@^$RPM_BUILD_ROOT@@g" >> %{name}-%{version}-%{release}-filelist

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && [ -d ${RPM_BUILD_ROOT} ] && rm -rf ${RPM_BUILD_ROOT};


%changelog
* Tue Jan 12 2010 Sean Collins <contact@seanmcollins.com> 1.0-1.8
- Updated deps
* Thu Mar 26 2009 allenday allenday 1.0-1.7
- depcheck
* Thu Mar 26 2009 allenday allenday 1.0-1.6
- version increment
* Fri Jun 27 2008 bpbuild bpbuild 1.0-1.5
- Modified the schema a bit in gmod-schema-0.003.tar.gz to add in
  primary keys.  Added a couple godb tables to the skip table arg in
  the gmod-web spec file.  This is because SQLTranslator 0.09 is more
  strict.
* Fri Jun 27 2008 bpbuild bpbuild 1.0-1.4
- Set the schema version to 0.003.
* Fri Aug 24 2007 boconnor boconnor 1.0-1.3
- Updating for the 0.5 schema
* Thu Jan 04 2007 bpbuild bpbuild 1.0-1.2
- Updates to the chado RPMs, the schema is now separated into it's own
  RPM to make it easier to build GMODWeb sites without first having to
  build/install the chado RPM
* Thu Jan 04 2007 bpbuild bpbuild 1.0-1.1
- Added new chado-schema spec file
