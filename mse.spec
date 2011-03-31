Summary: EMBOSS:MSE Applications
Name: MSE
Version: 1.0.0
Release: 7.%{distro}
license: GPL
Group: Applications/Bioinformatics
Source: ftp://emboss.open-bio.org/pub/EMBOSS/%{name}-%{version}.tar.gz
BuildPrereq: EMBOSS-devel = 6.1.0
BuildRoot: %{_tmppath}/%{name}-buildroot
Prereq: EMBOSS = 6.1.0


%description
The MSE package is a multiple sequence editor.

The program was contributed to the EMBOSS package by the author, Will Gilbert, as one of the first EMBASSY programs.

Users of the GCG package may find this program familiar - GCG converted an earlier (fortran) version of the same program to be their multiple sequence editor.

%prep
%setup -q 

%build
./configure CFLAGS="$RPM_OPT_FLAGS" --prefix=/usr \
    --bindir=%{_bindir} \
    --with-thread=linux \
    --libdir=%{_libdir}
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
%{_datadir}/EMBOSS/doc/html/embassy/mse/*
%{_datadir}/EMBOSS/doc/programs/text/*
%{_libdir}/libckit.*


%changelog
* Mon Jan 11 2010 Sean Collins <contact@seanmcollins.com> 1.0.0-7
- Rebuilt for EMBOSS 6.1.0

* Mon Jul 23 2007 Ryan Golhar <golharam@umdnj.edu> 1.0.0-6
- Rebuilt for EMBOSS 5.0.0

* Wed Feb  7 2007 Ryan Golhar <golharam@umdnj.edu> 1.0.0-5
- Rebuilt for EMBOSS 4.1.0

* Thu Nov  2 2006 Ryan Golhar <golharam@umdnj.edu> 1.0.0-4
- Changed the application to Applications/Bioinformatics

* Thu Aug 17 2006 Ryan Golhar <golharam@umdnj.edu>
- Rebuilt for EMBOSS 4.0.0

* Wed Dec  7 2005 Ryan Golhar <golharam@umdnj.edu>
- Changed binary directory from /usr/local/bin to /usr/bin

* Wed Jul 20 2005 Ryan Golhar <golharam@umdnj.edu> 
- Initial construction

