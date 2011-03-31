# TODO:
# fix jemboss and enable it

%define emhome %{_datadir}/EMBOSS
%define _javadir /usr/java/default

Name:           EMBOSS
Version:        6.1.0
Release:        6%{?dist}
Summary:        The European Molecular Biology Open Software Suite

Group:          Applications/Engineering
License:        GPLv2+
URL:            http://emboss.sf.net/
Source0:        ftp://emboss.open-bio.org/pub/EMBOSS/%{name}-%{version}.tar.gz
Source1:        README.fixes
Source2:        jemboss.desktop
#Use system-wide pcre. Sent upstream.
Patch1:         %{name}-system-pcre.patch
#Remove extra destdir. Sent upstream.
Patch3:         %{name}-6.1.0-destdir.patch
#Patch ensuring jemboss rebuild backported from CVS
Patch4:         %{name}-6.1.0-rebuild.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

#BuildRequires:  ant
#BuildRequires:  desktop-file-utils
#BuildRequires:  gd-devel
#BuildRequires:  java-devel >= 1:1.6.0
#BuildRequires:  jpackage-utils
#BuildRequires:  pam-devel
#BuildRequires:  pcre-devel
#BuildRequires:  axis jaf javamail jakarta-commons-discovery jakarta-commons-logging
#BuildRequires:  log4j regexp servlet xerces-j2 wsdl4j

%description
EMBOSS is a new, free Open Source software analysis package specially
developed for the needs of the molecular biology (e.g. EMBnet) user community.
The software automatically copes with data in a variety of formats and even
allows transparent retrieval of sequence data from the web. Also, as extensive
libraries are provided with the package, it is a platform to allow other
scientists to develop and release software in true open source spirit.
EMBOSS also integrates a range of currently available packages and tools for
sequence analysis into a seamless whole.

Reference for EMBOSS: Rice,P. Longden,I. and Bleasby,A.
"EMBOSS: The European Molecular Biology Open Software Suite"
Trends in Genetics June 2000, vol 16, No 6. pp.276-277


%package devel
Summary:        Development tools for programs which will use the %{name} library
Group:          Development/Libraries
Requires:       %{name}-libs = %{version}-%{release}

%description devel
The %{name}-devel package includes the header files and static libraries
necessary for developing programs which will use the %{name} library.


%package libs
Summary:        Shared libraries for %{name}
Group:          System Environment/Libraries

%description libs
The %{name}-libs package includes the dynamic libraries
necessary for %{name}.


#%package -n jemboss
#Summary:        Java interface to %{name}
#Group:          Applications/Engineering
#Requires:       %{name} = %{version}-%{release}
#Requires:       java >= 1:1.6.0
#Requires:       jpackage-utils    
#Requires:       axis jaf javamail jakarta-commons-discovery jakarta-commons-logging
#Requires:       log4j regexp servlet xerces-j2 wsdl4j

#%description -n jemboss
#Jemboss is a Java interface to EMBOSS, developed at
#the HGMP-RC and in close collaboration with the EMBOSS
#development team. It is distributed as part of the EMBOSS
#software.

#Documentation on Jemboss can be found at:
#http://www.hgmp.mrc.ac.uk/Software/EMBOSS/Jemboss/


%prep
%setup -q
%patch1 -p1 -b .pcre
%patch3 -p0 -b .destdir

#install the patch readme
install -pm 644 %{SOURCE1} README.fixes

#these files were executable for some reason
chmod 644 emboss/prettyplot.c emboss/polydot.c emboss/supermatcher.c

#use newer log4j version
#sed -i "s@log4j-1.2.8@log4j-1.2.14@" \
#    jemboss/lib/axis/Makefile.am \
#    jemboss/lib/axis/Makefile.in \
#    jemboss/utils/makeFileManagerJNLP.sh \
#    jemboss/utils/makeJNLP.sh

#use system java libraries
#rm jemboss/lib/{activation,client,jakarta-regexp-1.2,mail,xerces}.jar
#build-jar-repository -s -p jemboss/lib activation regexp javamail xerces-j2
#mv jemboss/lib/regexp.jar jemboss/lib/jakarta-regexp-1.2.jar
#mv jemboss/lib/javamail.jar jemboss/lib/mail.jar
#mv jemboss/lib/xerces-j2.jar jemboss/lib/xerces.jar
#rm jemboss/lib/axis/*.jar
#build-jar-repository -s -p jemboss/lib/axis axis/axis-ant axis/axis axis/jaxrpc axis/saaj commons-discovery commons-logging log4j-1.2.14 servlet wsdl4j
#for i in axis axis-ant jaxrpc saaj;
#do
#mv jemboss/lib/axis/axis_$i.jar jemboss/lib/axis/$i.jar;
#done


%build
export PATH=$PATH:%{_javadir}/bin/
%configure \
  --disable-static \
  --with-x \
  --with-auth \
  --with-thread \
  --includedir=%{_includedir}/EMBOSS \
%ifarch ppc64 sparc64 x86_64
  --enable-64 \
%endif
   --with-java=%{_javadir}/include \
   --with-javaos=%{_javadir}/include/linux \

%{__make} %{?_smp_mflags}


%install
rm -rf $RPM_BUILD_ROOT
export PATH=$PATH:%{_javadir}/bin/

%{__make} install DESTDIR=$RPM_BUILD_ROOT

install -m 755 -d $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d
cat << __EOF__ >> $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/emboss.sh
export PLPLOT_LIB=%{emhome}
export EMBOSS_ACDROOT=%{emhome}/acd
export EMBOSS_DOCROOT=%{emhome}/doc
export EMBOSS_DATABASE_DIR=%{emhome}/data
export EMBOSS_DATA=%{emhome}/data
__EOF__

cat << __EOF__ >> $RPM_BUILD_ROOT/%{_sysconfdir}/profile.d/emboss.csh
setenv PLPLOT_LIB %{emhome}
setenv EMBOSS_ACDROOT %{emhome}/acd
setenv EMBOSS_DOCROOT %{emhome}/doc
setenv EMBOSS_DATABASE_DIR %{emhome}/data
setenv EMBOSS_DATA %{emhome}/data
__EOF__

rm $RPM_BUILD_ROOT%{_libdir}/*.la

#this file has zero length, so kill it
rm $RPM_BUILD_ROOT%{_datadir}/EMBOSS/test/data/dna.aln

#fix executable permissions
pushd $RPM_BUILD_ROOT%{_datadir}/EMBOSS/jemboss/utils
chmod +x install-jemboss-server.sh keys.sh makeFileManagerJNLP.sh makeJar.csh \
     makeJNLP.sh
popd
pushd $RPM_BUILD_ROOT%{_datadir}/EMBOSS/jemboss/api
chmod +x getClasses.pl makeDocs.csh
popd

#rename conflicting binaries
mv $RPM_BUILD_ROOT%{_bindir}/chaos $RPM_BUILD_ROOT%{_bindir}/em_chaos

%clean
rm -rf $RPM_BUILD_ROOT


%post libs -p /sbin/ldconfig


%postun libs -p /sbin/ldconfig


%files
%defattr(-,root,root,-)
%doc AUTHORS ChangeLog COPYING FAQ INSTALL LICENSE NEWS README README.fixes THANKS
%{_bindir}/*
%exclude %{_bindir}/runJemboss.csh
%exclude %{_bindir}/jembossctl
%{_datadir}/EMBOSS
%exclude %{_datadir}/EMBOSS/jemboss
%config %{_sysconfdir}/profile.d/*


%files devel
%defattr(-,root,root,-)
%{_libdir}/*.so
%{_includedir}/EMBOSS


%files libs
%defattr(-,root,root,-)
%{_libdir}/*.so.*


#%files -n jemboss
#%defattr(-,root,root,-)
#%doc jemboss/README jemboss/resources jemboss/api
#%{_bindir}/runJemboss.csh
#%{_bindir}/jembossctl
#%{_datadir}/applications/jemboss.desktop
#%{_datadir}/EMBOSS/jemboss


%changelog
* Sun Dec 13 2009 Julian Sikorski <belegdol@fedoraproject.org> - 6.1.0-6
- Added the upstream 1-3 patch
- Fixed bogus Patch3 description
- Jemboss is still disabled, but some improvements have been made
  - Backported patch enabling jemboss rebuild from CVS
  - Added ant and jpackage-utils to BuildRequires
  - Made java-devel dependency versioned
  - Switched to build-jar-repository to fill the dependencies
  - Replaced versioned log4j calls with latest version
  - Renamed EMBOSS-java to jemboss
  - Added a desktop entry for jemboss from Debian

* Sat Oct 17 2009 Julian Sikorski <belegdol@fedoraproject.org> - 6.1.0-5
- Added comments explaining the purpose of each patch

* Mon Oct 05 2009 Julian Sikorski <belegdol@fedoraproject.org> - 6.1.0-4
- Renamed conflicting binaries
- Disabled jemboss

* Tue Sep 29 2009 Julian Sikorski <belegdol@fedoraproject.org> - 6.1.0-3
- Re-enabled system pcre usage
- Initial attempt at using system-wide .jar files

* Tue Sep 22 2009 Julian Sikorski <belegdol@fedoraproject.org> - 6.1.0-2
- Added the upstream 1-2 patch

* Wed Jul 29 2009 Julian Sikorski <belegdol@fedoraproject.org> - 6.1.0-1
- Updated to 6.1.0
- Dropped pcre-devel from BuildRequires for the time being
- Ditto --with-java and --with-javaos
- Patched jemboss/Makefile.am not to include DESTDIR in runJemboss.sh
- Install the header files in EMBOSS subdir
- Added the missing executable bits

* Fri Jun 12 2009 Julian Sikorski <belegdol@fedoraproject.org> - 6.0.1-3
- Updated the upstream patch to 1-12
- Added the patch readme to %%doc

* Thu Apr 16 2009 Julian Sikorski <belegdol@fedoraproject.org> - 6.0.1-2
- Own %%{_datadir}/EMBOSS
- Don't use %%{name} macro in %%files
- Updated the upstream patch to 1-7
- Use dist instead of dist_tag
- Adjusted whitespaces
- Added pcre-devel to BuildRequires
- Fixed spurious executable permissions
- Removed the empty dna.aln file
- Patched jemboss.properties to include the paths this package uses
- Made the -java package require the main one

* Mon Sep 29 2008 Dominik Mierzejewski <rpm@greysector.net> 6.0.1-1
- updated to 6.0.1
- applied upstream patch 1-1
- patched to use system pcre

* Tue Jan 08 2008 Dominik Mierzejewski <rpm@greysector.net> 5.0.0-1
- Cleaned up BioRPMs' spec
- Updated to 5.0.0

* Thu Mar 17 2005 Bent Terp <Bent.Terp@biosci.ki.se>
- Upped to 2.10.0

* Fri Jul 16 2004 Bent Terp <Bent.Terp@biosci.ki.se>
- Had forgotten the emboss_database_dir env var

* Wed Feb 18 2004 Bent Terp <Bent.Terp@biosci.ki.se>
- Tried to make the building more dynamic. Added Requires and BuildRequires

* Thu Dec 04 2003 Luc Ducazu <luc@biolinux.org>
- Build for EMBOSS 2.8.0
- subpackage jemboss

* Wed Jun 11 2003 Luc Ducazu <luc@biolinux.org>
- Build for EMBOSS 2.7.1

* Tue Jan 28 2003 Luc Ducazu <luc@biolinux.org>
- Build for EMBOSS 2.6.0
- Programs moved to /usr/local/bin
- Adopted many ideas from Guillaume Rousse <g.rousse@linux-mandrake.com>

* Wed Nov 27 2002 Luc Ducazu <luc@biolinux.org>
- Initial build for EMBOSS 2.5.1
