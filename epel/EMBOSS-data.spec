# ----------------------------------------------------------------------------
#
#   EMBOSS
#
# ----------------------------------------------------------------------------
%define _version 6.2.0

Name:      EMBOSS-data
Version:   %{_version}
Release:   1.%{distro}
License:   GPL/LGPL
URL:       http://emboss.sourceforge.net

Source0:   ftp://emboss.open-bio.org/pub/EMBOSS/EMBOSS-%{_version}.tar.gz

Source1:   ftp://ftp.genome.ad.jp/pub/db/genomenet/aaindex/aaindex1
Source2:   ftp://ftp.neb.com/pub/rebase/withrefm.609
Source3:   ftp://ftp.neb.com/pub/rebase/proto.609
Source4:   ftp://ftp.ebi.ac.uk/pub/databases/prints/prints38_0.dat.gz
Source5:   ftp://ftp.ebi.ac.uk/pub/databases/prosite/release_with_updates/prosite.dat
Source6:   ftp://ftp.ebi.ac.uk/pub/databases/prosite/release_with_updates/prosite.doc
BuildRoot: %{_tmppath}/%{name}-buildroot
Summary:   Extra data for EMBOSS
Group:     Applications/Bioinformatics
Requires:  EMBOSS = %{_version}

%description 
Extra data for EMBOSS:
 * AAINDEX
 * REBASE
 * PRINTS
 * PROSITE


%prep
%setup -q -n EMBOSS-%{_version}

%build
%install
## data stuff
export EMBOSS_DATA=$RPM_BUILD_ROOT/usr/share/EMBOSS/data

mkdir $EMBOSS_DATA/AAINDEX
mkdir $EMBOSS_DATA/REBASE


# aaindex
aaindexextract \
   -infile $RPM_SOURCE_DIR/aaindex1
# rebase
rebaseextract \
   -infile $RPM_SOURCE_DIR/withrefm.609 \
   -protofile $RPM_SOURCE_DIR/proto.609
# prints
printsextract \
   -infile $RPM_SOURCE_DIR/prints38_0.dat.gz
# prosite
prosextract \
   -prositedir $RPM_SOURCE_DIR
#   -infdat $RPM_SOURCE_DIR

%clean
[ "$RPM_BUILD_ROOT" != "/" ] && rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig

%postun
/sbin/ldconfig:wq

# ----------------------------------------------------------------------------

%files 
%defattr(-,root,root)
%{_datadir}/EMBOSS/data/AAINDEX/*[0-9]*
%{_datadir}/EMBOSS/data/PRINTS/[Pp]*
%{_datadir}/EMBOSS/data/PROSITE/[Pp]*
%{_datadir}/EMBOSS/data/REBASE/embossre.*


# ----------------------------------------------------------------------------

%changelog
* Fri Jan 22 2010 Sean Collins <contact@seanmcollins.com> 6.2.0-1
- Rebuilt for EMBOSS v6.2.0

* Mon Jan 4 2010 Sean Collins <contact@seanmcollins.com> 6.1.0-1
- Rebuilt for EMBOSS v6.1.0
- Changed SPEC file to work with CentOS 5.4 and Sun JRE 1.6.0_17-b04

