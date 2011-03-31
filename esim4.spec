Summary: EMBOSS:ESIM4 Applications
Name: ESIM4
Version: 1.0.0
Release: 7.%{distro}
license: GPL
Group: Applications/Bioinformatics
Source: ftp://emboss.open-bio.org/pub/EMBOSS/%{name}-%{version}.tar.gz
BuildPrereq: EMBOSS-devel = 6.1.0
BuildRoot: %{_tmppath}/%{name}-buildroot
Prereq: EMBOSS = 6.1.0

%description
The ESIM4 package is an EMBOSS conversion of the SIM4 package from Liliana 
Florea.

The ESIM4 versions of these programs all have the prefix "e" to distinguish them from the original programs. Although we take care to check that the EMBOSS versions will give the same results as the original programs, we recommend that if the results are used for publication you should check that you get the same results with both for your specific inputs. 

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
%{_datadir}/EMBOSS/doc/html/embassy/esim4/*
%{_datadir}/EMBOSS/doc/programs/text/*

%changelog
* Mon Jan 11 2010 Sean Collins <contact@seanmcollins.com> 1.0.0-7
- Rebuilt for EMBOSS 6.1.0

* Mon Jul 23 2007 Ryan Golhar <golharam@umdnj.edu> 1.0.0-6
- Rebuilt for EMBOSS 5.0.0

* Wed Mar  7 2007 Ryan Golhar <golharam@umdnj.edu> 1.0.0-5
- Rebuilt for EMBOSS 4.1.0

* Thu Nov  2 2006 Ryan Golhar <golharam@umdnj.edu> 1.0.0-4
- Changed the application to Applications/Bioinformatics

* Fri Aug 11 2006 Ryan Golhar <golharam@umdnj.edu> 1.0.0-3
- Rebuilt for EMBOSS 4.0.0

* Wed Dec  7 2005 Ryan Golhar <golharam@umdnj.edu> 1.0.0-2
- Changed binary directory from /usr/local/bin to /usr/bin

* Wed Jul 20 2005 Ryan Golhar <golharam@umdnj.edu> 1.0.0-1
- Initial construction

