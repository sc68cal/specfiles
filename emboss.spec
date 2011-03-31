# ----------------------------------------------------------------------------
#
#   EMBOSS
#
# ----------------------------------------------------------------------------
%define _version 6.1.0

Name:      EMBOSS
Version:   %{_version}
Release:   1.%{distro}
Summary:   The European Molecular Biology Open Software Suite

Group:     Applications/Bioinformatics
License:   GPL/LGPL
URL:       http://emboss.sourceforge.net

Source0:   ftp://emboss.open-bio.org/pub/EMBOSS/EMBOSS-%{_version}.tar.gz

Source1:   ftp://ftp.genome.ad.jp/pub/db/genomenet/aaindex/aaindex1
Source2:   ftp://ftp.neb.com/pub/rebase/withrefm.609
Source3:   ftp://ftp.neb.com/pub/rebase/proto.609
Source4:   ftp://ftp.ebi.ac.uk/pub/databases/prints/prints38_0.dat.gz
Source5:   ftp://ftp.ebi.ac.uk/pub/databases/prosite/release_with_updates/prosite.dat
Source6:   ftp://ftp.ebi.ac.uk/pub/databases/prosite/release_with_updates/prosite.doc

Source7:   emboss.default

Source8:   runJemboss.standalone
Source9:   jemboss.properties

Requires:  /sbin/ldconfig
BuildRoot: %{_tmppath}/%{name}-buildroot
BuildPrereq: gd >= 1.8.4

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
Summary:   Header files and static libraries for EMBOSS
Group:     Development/Libraries
Requires:  EMBOSS = %{_version}

%description devel
Header files and static libraries for EMBOSS

%package data
Summary:   Extra data for EMBOSS
Group:     Applications/Bioinformatics
Requires:  EMBOSS = %{_version}

%description data
Extra data for EMBOSS:
 * AAINDEX
 * REBASE
 * PRINTS
 * PROSITE

%package Jemboss
Summary:   Java based GUI for EMBOSS
Group:     Applications/Bioinformatics
Requires:  EMBOSS = %{_version}

%description Jemboss
Jemboss is a java based interface to EMBOSS. It provides the advantage of 
being able to provide sensible EMBOSS defaults on-the-fly for a given sequence
or for a given input parameter. 
Jemboss can run the EMBOSS applications interactively or as a batch process.

# ----------------------------------------------------------------------------

%prep
%setup -q

%build
#Check for JAVADIR
if [ -z "$JAVADIR" || ! -d "$JAVADIR" ]; then
	# Not found or not set correctly.
	# Go hunting
	JAVADIR=""
	for D in /usr/java/j2sdk* /usr/local/j2sdk* /opt/java/j2sdk* /opt/local/j2sdk* /usr/java/jdk*; do
		if [ -x $D/bin/java ]; then
			JAVADIR=$D
			break
		fi
	done

	if [ -z "$JAVADIR" ]; then
		echo "JAVADIR not defined, and I couldn't find a replacement"
		exit 1
	fi
fi

export JAVADIR
export PATH=$PATH:$JAVADIR/bin

./configure CFLAGS="$RPM_OPT_FLAGS" --prefix=/usr \
    --bindir=%{_bindir} \
    --libdir=%{_libdir} \
    --with-java=$JAVADIR/include --with-javaos=$JAVADIR/include/linux \
    --with-thread=linux 
nice make -j2

%install
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

#Check for JAVADIR (again)
if [ -z "$JAVADIR" || ! -d "$JAVADIR" ]; then
	# Not found or not set correctly.
	# Go hunting
	JAVADIR=""
	for D in /usr/java/j2sdk* /usr/local/j2sdk* /opt/java/j2sdk* /opt/local/j2sdk* /usr/java/jdk*; do
		if [ -x $D/bin/java ]; then
			JAVADIR=$D
			break
		fi
	done

	if [ -z "$JAVADIR" ]; then
		echo "JAVADIR not defined, and I couldn't find a replacement"
	exit 1
	fi
fi

export JAVADIR
export PATH=$PATH:$JAVADIR/bin

make DESTDIR=$RPM_BUILD_ROOT install
install -m 644 $RPM_SOURCE_DIR/emboss.default $RPM_BUILD_ROOT%{_datadir}/EMBOSS

## environment stuff
DESTDIR=$RPM_BUILD_ROOT%{_sysconfdir}/profile.d
install -m 755 -d $DESTDIR
echo "export PLPLOT_LIB=%{_datadir}/EMBOSS" > $DESTDIR/emboss.sh
echo "setenv PLPLOT_LIB %{_datadir}/EMBOSS" > $DESTDIR/emboss.csh

## data stuff
export LD_LIBRARY_PATH=$RPM_BUILD_ROOT/%{_libdir}
export EMBOSS_DATA=$RPM_BUILD_ROOT%{_datadir}/EMBOSS/data
# aaindex
$RPM_BUILD_ROOT%{_bindir}/aaindexextract \
   -infile $RPM_SOURCE_DIR/aaindex1
# rebase
$RPM_BUILD_ROOT%{_bindir}/rebaseextract \
   -infile $RPM_SOURCE_DIR/withrefm.609 \
   -protofile $RPM_SOURCE_DIR/proto.609
# prints
$RPM_BUILD_ROOT%{_bindir}/printsextract \
   -infile $RPM_SOURCE_DIR/prints38_0.dat.gz
# prosite
$RPM_BUILD_ROOT%{_bindir}/prosextract \
   -prositedir $RPM_SOURCE_DIR
#   -infdat $RPM_SOURCE_DIR

## jemboss stuff
install -m 755 $RPM_SOURCE_DIR/runJemboss.standalone $RPM_BUILD_ROOT/%{_bindir}
install -m 644 $RPM_SOURCE_DIR/jemboss.properties $RPM_BUILD_ROOT/%{_datadir}/EMBOSS/jemboss/resources

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig

# ----------------------------------------------------------------------------

%files
%defattr(-,root,root)
%{_libdir}/*.so*
%{_bindir}/aaindexextract
%{_bindir}/abiview
%{_bindir}/acdc
%{_bindir}/acdpretty
%{_bindir}/acdtable
%{_bindir}/acdtrace
%{_bindir}/acdvalid
%{_bindir}/antigenic
%{_bindir}/backtranambig
%{_bindir}/backtranseq
%{_bindir}/banana
%{_bindir}/biosed
%{_bindir}/btwisted
%{_bindir}/cai
%{_bindir}/chaos
%{_bindir}/charge
%{_bindir}/checktrans
%{_bindir}/chips
%{_bindir}/cirdna
%{_bindir}/codcmp
%{_bindir}/codcopy
%{_bindir}/coderet
%{_bindir}/compseq
%{_bindir}/cons
%{_bindir}/cpgplot
%{_bindir}/cpgreport
%{_bindir}/cusp
%{_bindir}/cutgextract
%{_bindir}/cutseq
%{_bindir}/dan
%{_bindir}/dbiblast
%{_bindir}/dbifasta
%{_bindir}/dbiflat
%{_bindir}/dbigcg
%{_bindir}/dbxfasta
%{_bindir}/dbxflat
%{_bindir}/dbxgcg
%{_bindir}/degapseq
%{_bindir}/descseq
%{_bindir}/diffseq
%{_bindir}/digest
%{_bindir}/distmat
%{_bindir}/dotmatcher
%{_bindir}/dotpath
%{_bindir}/dottup
%{_bindir}/dreg
%{_bindir}/einverted
%{_bindir}/edialign
%{_bindir}/embossdata
%{_bindir}/embossversion
%{_bindir}/emma
%{_bindir}/emowse
%{_bindir}/entret
%{_bindir}/epestfind
%{_bindir}/eprimer3
%{_bindir}/equicktandem
%{_bindir}/est2genome
%{_bindir}/etandem
%{_bindir}/extractalign
%{_bindir}/extractfeat
%{_bindir}/extractseq
%{_bindir}/findkm
%{_bindir}/freak
%{_bindir}/fuzznuc
%{_bindir}/fuzzpro
%{_bindir}/fuzztran
%{_bindir}/garnier
%{_bindir}/geecee
%{_bindir}/getorf
%{_bindir}/helixturnhelix
%{_bindir}/hmoment
%{_bindir}/iep
%{_bindir}/infoalign
%{_bindir}/infoseq
%{_bindir}/isochore
%{_bindir}/lindna
%{_bindir}/listor
%{_bindir}/makenucseq
%{_bindir}/makeprotseq
%{_bindir}/marscan
%{_bindir}/maskfeat
%{_bindir}/maskseq
%{_bindir}/matcher
%{_bindir}/megamerger
%{_bindir}/merger
%{_bindir}/msbar
%{_bindir}/mwcontam
%{_bindir}/mwfilter
%{_bindir}/needle
%{_bindir}/newcpgreport
%{_bindir}/newcpgseek
%{_bindir}/newseq
%{_bindir}/noreturn
%{_bindir}/notseq
%{_bindir}/nthseq
%{_bindir}/octanol
%{_bindir}/oddcomp
%{_bindir}/palindrome
%{_bindir}/pasteseq
%{_bindir}/patmatdb
%{_bindir}/patmatmotifs
%{_bindir}/pepcoil
%{_bindir}/pepinfo
%{_bindir}/pepnet
%{_bindir}/pepstats
%{_bindir}/pepwheel
%{_bindir}/pepwindow
%{_bindir}/pepwindowall
%{_bindir}/plotcon
%{_bindir}/plotorf
%{_bindir}/polydot
%{_bindir}/preg
%{_bindir}/prettyplot
%{_bindir}/prettyseq
%{_bindir}/primersearch
%{_bindir}/printsextract
%{_bindir}/profit
%{_bindir}/prophecy
%{_bindir}/prophet
%{_bindir}/prosextract
%{_bindir}/pscan
%{_bindir}/psiphi
%{_bindir}/rebaseextract
%{_bindir}/recoder
%{_bindir}/redata
%{_bindir}/remap
%{_bindir}/restover
%{_bindir}/restrict
%{_bindir}/revseq
%{_bindir}/seealso
%{_bindir}/seqmatchall
%{_bindir}/seqret
%{_bindir}/seqretsplit
%{_bindir}/showalign
%{_bindir}/showdb
%{_bindir}/showfeat
%{_bindir}/showorf
%{_bindir}/showseq
%{_bindir}/shuffleseq
%{_bindir}/sigcleave
%{_bindir}/silent
%{_bindir}/sirna
%{_bindir}/sixpack
%{_bindir}/skipseq
%{_bindir}/splitter
%{_bindir}/stretcher
%{_bindir}/stssearch
%{_bindir}/supermatcher
%{_bindir}/syco
%{_bindir}/tcode
%{_bindir}/textsearch
%{_bindir}/tfextract
%{_bindir}/tfm
%{_bindir}/tfscan
%{_bindir}/tmap
%{_bindir}/tranalign
%{_bindir}/transeq
%{_bindir}/trimest
%{_bindir}/trimseq
%{_bindir}/twofeat
%{_bindir}/union
%{_bindir}/vectorstrip
%{_bindir}/water
%{_bindir}/whichdb
%{_bindir}/wobble
%{_bindir}/wordcount
%{_bindir}/wordfinder
%{_bindir}/wordmatch
%{_bindir}/wossname
%{_bindir}/yank

%{_bindir}/aligncopy
%{_bindir}/aligncopypair
%{_bindir}/consambig
%{_bindir}/density
%{_bindir}/featcopy
%{_bindir}/featreport
%{_bindir}/infobase
%{_bindir}/inforesidue
%{_bindir}/jaspextract
%{_bindir}/jaspscan
%{_bindir}/maskambignuc
%{_bindir}/maskambigprot
%{_bindir}/nohtml
%{_bindir}/nospace
%{_bindir}/notab
%{_bindir}/nthseqset
%{_bindir}/seqretsetall
%{_bindir}/showpep
%{_bindir}/sizeseq
%{_bindir}/skipredundant
%{_bindir}/splitsource
%{_bindir}/trimspace
%{_datadir}/EMBOSS/data/JASPAR_CNE/dummyfile
%{_datadir}/EMBOSS/data/JASPAR_CORE/dummyfile
%{_datadir}/EMBOSS/data/JASPAR_FAM/dummyfile
%{_datadir}/EMBOSS/data/JASPAR_PHYLOFACTS/dummyfile
%{_datadir}/EMBOSS/data/JASPAR_POLII/dummyfile
%{_datadir}/EMBOSS/data/JASPAR_SPLICE/dummyfile
%{_datadir}/EMBOSS/data/SSSUB


%{_datadir}/EMBOSS/acd
%{_datadir}/EMBOSS/data/CODONS
%{_datadir}/EMBOSS/data/AAINDEX/dummyfile
%{_datadir}/EMBOSS/data/PRINTS/dummyfile
%{_datadir}/EMBOSS/data/PROSITE/dummyfile
%{_datadir}/EMBOSS/data/REBASE/dummyfile
%{_datadir}/EMBOSS/data/[Ee]*
%{_datadir}/EMBOSS/data/Matrices.*
%{_datadir}/EMBOSS/data/tp400_dna
%{_datadir}/EMBOSS/data/tp400_prot
%{_datadir}/EMBOSS/data/tp400_trans
%{_datadir}/EMBOSS/doc
%{_datadir}/EMBOSS/test
%{_datadir}/EMBOSS/emboss.default.template
%{_datadir}/EMBOSS/plstnd5.fnt
%{_datadir}/EMBOSS/plxtnd5.fnt
%config %{_sysconfdir}/profile.d/*
%config %{_datadir}/EMBOSS/emboss.default
%doc AUTHORS ChangeLog COPYING FAQ INSTALL LICENSE NEWS README THANKS

%files devel
%defattr(-,root,root)
/usr/include/*.h
/usr/include/eplplot
/usr/include/*.c
%{_libdir}/*.a
%{_libdir}/*.la

%files data
%defattr(-,root,root)
%{_datadir}/EMBOSS/data/AAINDEX/*[0-9]*
%{_datadir}/EMBOSS/data/PRINTS/[Pp]*
%{_datadir}/EMBOSS/data/PROSITE/[Pp]*
%{_datadir}/EMBOSS/data/REBASE/embossre.*

%files Jemboss
%defattr(-,root,root)
%{_bindir}/jembossctl
%{_bindir}/runJemboss.csh
%{_bindir}/runJemboss.standalone
%{_datadir}/EMBOSS/jemboss

# ----------------------------------------------------------------------------

%changelog
* Mon Jan 4 2010 Sean Collins <contact@seanmcollins.com> 6.1.0-1
- Rebuilt for EMBOSS v6.1.0
- Changed SPEC file to work with CentOS 5.4 and Sun JRE 1.6.0_17-b04

* Mon Jul 23 2007 Ryan Golhar <golharam@umdnj.edu> 5.0.0-1
- Rebuilt for EMBOSS v5.0.0

* Wed Mar  7 2007 Ryan Golhar <golharam@umdnj.edu> 4.1.0-1
- Rebuilt for EMBOSS v4.1.0
- Changed SPEC file to find Java installation (Jesse Becker)
- Changed SPEC file for 64-bit support (Jesse Becker) <beckerjes@nhgri.nih.gov>

* Wed Nov  8 2006 Ryan Golhar <golharam@umdnj.edu> 4.0.0-5
- Applied patches 1-19.
- Patch 19: This fixes a problem with the specification of mismatches in "the fuzzies" (i.e. fuzznuc etc).

* Thu Nov  2 2006 Ryan Golhar <golharam@umdnj.edu> 4.0.0-4
- Changed the application to Applications/Bioinformatics

* Wed Sep 20 2006 Ryan Golhar <golharam@umdnj.edu> 4.0.0-3
- Applied patches 1-18

* Sun Aug 27 2006 Ryan Golhar <golharam@umdnj.edu> 4.0.0-2
- Applied patches 1-15
- Updated aaindex1, rebase, prints, and prosite

* Fri Aug 11 2006 Ryan Golhar <golharam@umdnj.edu> 4.0.0-1
- Rebuilt for EMBOSS 4.0.0

* Mon Oct 31 2005 Ryan Golhar <golharam@umdnj.edu>
- Changed binary installs from /usr/local/bin to /usr/bin to be consistent

* Sun Oct 16 2005 Ryan Golhar <golharam@umdnj.edu>
- Build for EMBOSS 3.0.0-2
- Added prosite build back

* Thu Jul 20 2005 Ryan Golhar <golharam@umdnj.edu>
- Build for EMBOSS 3.0.0
- Removed prosite build - parameters changed and do not match docs
- Changed installation location for include files to /usr/include
- Added sanity check to cleaning

* Fri May 13 2005 Ryan Golhar <golharam@umdnj.edu>
- Build for EMBOSS 2.10.0

* Mon Jul 26 2004 Luc Ducazu <luc@biolinux.org>
- Build for EMBOSS 2.9.0
- subpackage EMBOSS-devel
- subpackage EMBOSS-data

* Fri May 07 2004 Luc Ducazu <luc@biolinux.org>
- Added AAINDEX, PROSITE, PRINTS and REBASE data files

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
