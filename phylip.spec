Summary: EMBOSS:PHYLIP Applications
Name: PHYLIP
Version: 3.68
Release: 7.%{distro}
license: GPL
Group: Applications/Bioinformatics
Source: ftp://emboss.open-bio.org/pub/EMBOSS/PHYLIP-%{version}.tar.gz
BuildPrereq: EMBOSS-devel = 6.1.0
BuildRoot: %{_tmppath}/%{name}-buildroot
Prereq: EMBOSS = 6.1.0
Obsoletes: PHYLIPNEW

%description
The PHYLIP programs in this EMBASSY package are ported from release 3.572.
PHYLIP 3.6 is being converted as PHYLIPNEW and will be released soon. The developers version can be downloaded from CVS. 

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
%{_datadir}/EMBOSS/doc/html/embassy/phylipnew/*
%{_datadir}/EMBOSS/doc/programs/text/*
%{_datadir}/PHYLIP

%changelog
* Mon Jan 11 2010 Sean Collins <contact@seanmcollins.com> 3.68-7
- Rebuilt for EMBOSS 6.1.0

* Mon Jul 23 2007 Ryan Golhar <golharam@umdnj.edu> 3.6b-6
- Rebuilt for EMBOSS 5.0.0

* Wed Mar  7 2007 Ryan Golhar <golharam@umdnj.edu> 3.6b-5
- Rebuilt for EMBOSS 4.1.0

* Thu Nov  2 2006 Ryan Golhar <golharam@umdnj.edu> 3.6b-4
- Changed the application to Applications/Bioinformatics

* Thu Aug 17 2006 Ryan Golhar <golharam@umdnj.edu> 3.6b-3
- Rebuilt for PHYLIPNEW and EMBOSS 4.0.0

* Wed Dec  7 2005 Ryan Golhar <golharam@umdnj.edu> 3.6b-2
- Changed binary directory from /usr/local/bin to /usr/bin

* Wed Jul 20 2005 Ryan Golhar <golharam@umdnj.edu> 3.6b-1
- Initial construction

