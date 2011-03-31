Summary: EMBOSS:DOMSEARCH Applications
Name: DOMSEARCH
Version: 0.1.0
Release: 7.%{distro}
license: GPL
Group: Applications/Bioinformatics
Source: ftp://emboss.open-bio.org/pub/EMBOSS/%{name}-%{version}.tar.gz
BuildPrereq: EMBOSS-devel = 6.1.0
BuildRoot: %{_tmppath}/%{name}-buildroot
Prereq: EMBOSS = 6.1.0

%description
The DOMSEARCH programs were developed by Jon Ison and colleagues at HGMP for 
their protein domain research. They are included as an EMBASSY package as a 
work in progress.

%prep
%setup -q 

%build
./configure CFLAGS="$RPM_OPT_FLAGS" --prefix=/usr \
    --bindir=%{_bindir} \
    --with-thread=linux 
make -j2

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -fr $RPM_BUILD_ROOT

make DESTDIR=$RPM_BUILD_ROOT install


%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -fr $RPM_BUILD_ROOT

%files
%defattr(755,root,root)
%doc AUTHORS ChangeLog COPYING INSTALL 
%{_bindir}/*
%{_datadir}/EMBOSS/acd/*
%{_datadir}/EMBOSS/doc/html/embassy/domsearch/*
%{_datadir}/EMBOSS/doc/programs/text/*

%changelog
* Mon Jan 11 2010 Sean Collins <contact@seanmcollins.com> 0.1.0-7
- Rebuilt for EMBOSS 6.1.0

* Mon Jul 23 2007 Ryan Golhar <golharam@umdnj.edu> 0.1.0-6
- Rebuilt for EMBOSS 5.0.0

* Wed Mar  7 2007 Ryan Golhar <golharam@umdnj.edu> 0.1.0-5
- Rebuilt for EMBOSS 4.1.0

* Thu Nov  2 2006 Ryan Golhar <golharam@umdnj.edu> 0.1.0-4
- Changed the application to Applications/Bioinformatics

* Fri Aug 11 2006 Ryan Golhar <golharam@umdnj.edu> 0.1.0-3
- Rebuilt for EMBOSS 4.0.0

* Wed Dec  7 2005 Ryan Golhar <golharam@umdnj.edu> 0.1.0-2
- Changed binary directory from /usr/local/bin to /usr/bin

* Wed Jul 20 2005 Ryan Golhar <golharam@umdnj.edu> 0.1.0-1
- Initial construction

