Summary: EMBOSS:MYEMBOSS Applications
Name: MYEMBOSS
Version: 6.1.0
Release: 1.%{distro}
license: GPL
Group: Applications/Bioinformatics
Source: ftp://emboss.open-bio.org/pub/EMBOSS/%{name}-%{version}.tar.gz
BuildPrereq: EMBOSS-devel = 6.1.0
BuildRoot: %{_tmppath}/%{name}-buildroot
Prereq: EMBOSS = 6.1.0

%description
The MYEMBOSS package is an almost empty EMBASSY package where users can safely build their own EMBOSS applications.

The only applications we nitend to put into the MYEMBOSS package are examples of how to write programs. For now, these programs are installed - but we may decide to only build them locally in future. 

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
%{_datadir}/EMBOSS/doc/html/embassy/myseq/*
%{_datadir}/EMBOSS/doc/programs/text/myseq.txt

%changelog
* Mon Jan 4 2010 Sean Collins <contact@seanmcollins.com> 6.1.0-1
- Rebuilt for EMBOSS 6.1.0

* Mon Jul 23 2007 Ryan Golhar <golharam@umdnj.edu> 3.0.0-6
- Rebuitl for EMBOSS 5.0.0

* Wed Mar  7 2007 Ryan Golhar <golharam@umdnj.edu> 3.0.0-5
- Rebuilt for EMBOSS 4.1.0

* Thu Nov  2 2006 Ryan Golhar <golharam@umdnj.edu> 3.0.0-4
- Changed the application to Applications/Bioinformatics

* Thu Aug 17 2006 Ryan Golhar <golharam@umdnj.edu>
- Rebuilt for EMBOSS 4.0.0

* Wed Dec  7 2005 Ryan Golhar <golharam@umdnj.edu>
- Change binary directory from /usr/local/bin to /usr/bin

* Wed Jul 20 2005 Ryan Golhar <golharam@umdnj.edu> 
- Initial construction

