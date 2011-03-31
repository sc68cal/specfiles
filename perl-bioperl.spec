#$Id: perl-bioperl.spec.in,v 1.11 2009/03/17 08:16:51 allenday Exp $
Name:           perl-bioperl
Version:        1.6.0
Release:        1.14.%{distro}
Summary:        Perl tools for computational molecular biology

Group:          Development/Libraries
License:        GPL+ or Artistic
URL:            http://www.bioperl.org/
Source0:        http://bioperl.org/DIST/bioperl-%{version}.tar.bz2
Source1:        ftp://ftp.perl.org/pub/CPAN/authors/id/M/MI/MINGYILIU/Bio-ASN1-EntrezGene-1.091.tgz
Patch0:         %{name}-%{version}-paths.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  perl-AcePerl
#BuildRequires:  perl-Algorithm-Munkres
BuildRequires:  perl-Array-Compare
BuildRequires:  perl-Cache-Cache
BuildRequires:  perl-Class-AutoClass >= 1
BuildRequires:  perl-Clone
BuildRequires:  perl-Convert-Binary-C
BuildRequires:  perl-Data-Stag
BuildRequires:  perl-DBD-mysql
BuildRequires:  perl-DBD-Pg
BuildRequires:  perl-Error
BuildRequires:  perl-GD >= 1.3
BuildRequires:  perl-GD-SVG
BuildRequires:  perl-Graph
BuildRequires:  perl-GraphViz
BuildRequires:  perl-HTML-Parser
BuildRequires:  perl-IO-stringy
BuildRequires:  perl-IO-String
BuildRequires:  perl-libwww-perl
BuildRequires:  perl-Math-Random
BuildRequires:  perl-Module-Build
BuildRequires:  perl-PostScript
BuildRequires:  perl-Set-Scalar
BuildRequires:  perl-SOAP-Lite
BuildRequires:  perl-Spreadsheet-ParseExcel
BuildRequires:  perl-SVG >= 2.26
BuildRequires:  perl-SVG-Graph >= 0.01
BuildRequires:  perl-Test-Exception
BuildRequires:  perl-Test-Warn
BuildRequires:  perl-Text-Shellwords
BuildRequires:  perl-URI
BuildRequires:  perl-WWW-Mechanize
BuildRequires:  perl-XML-DOM-XPath >= 0.13
BuildRequires:  perl-XML-LibXML
BuildRequires:  perl-XML-Parser
BuildRequires:  perl-XML-SAX >= 0.14
BuildRequires:  perl-XML-SAX-Writer
BuildRequires:  perl-XML-Simple
BuildRequires:  perl-XML-Twig
BuildRequires:  perl-XML-Writer > 0.4

Requires:  perl-AcePerl
#Requires:  perl-Algorithm-Munkres
Requires:  perl-Array-Compare
Requires:  perl-Cache-Cache
Requires:  perl-Class-AutoClass >= 1
Requires:  perl-Clone
Requires:  perl-Convert-Binary-C
Requires:  perl-Data-Stag
Requires:  perl-DBD-mysql
Requires:  perl-DBD-Pg
Requires:  perl-Error
Requires:  perl-GD >= 1.3
Requires:  perl-GD-SVG
Requires:  perl-Graph
Requires:  perl-GraphViz
Requires:  perl-HTML-Parser
Requires:  perl-IO-stringy
Requires:  perl-IO-String
Requires:  perl-libwww-perl
Requires:  perl-Math-Random
Requires:  perl-Module-Build
Requires:  perl-PostScript
Requires:  perl-Set-Scalar
Requires:  perl-SOAP-Lite
Requires:  perl-Spreadsheet-ParseExcel
Requires:  perl-SVG >= 2.26
Requires:  perl-SVG-Graph >= 0.01
Requires:  perl-Test-Exception
Requires:  perl-Test-Warn
Requires:  perl-Text-Shellwords
Requires:  perl-URI
Requires:  perl-WWW-Mechanize
Requires:  perl-XML-DOM-XPath >= 0.13
Requires:  perl-XML-LibXML
Requires:  perl-XML-Parser
Requires:  perl-XML-SAX >= 0.14
Requires:  perl-XML-SAX-Writer
Requires:  perl-XML-Simple
Requires:  perl-XML-Twig
Requires:  perl-XML-Writer > 0.4
#Requires:  perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))

%description
BioPerl is a toolkit of Perl modules useful in building bioinformatics
solutions in Perl. It is built in an object-oriented manner so that
many modules depend on each other to achieve a task.

%prep
%setup -q -n BioPerl-%{version}
%patch0 -p1 
#begin hack to fold Bio-ASN1-EntrezGene into the bioperl distribution.  eliminates cyclic dependency
mkdir rpmtmp
pushd rpmtmp
tar -xvzf %{SOURCE1}
popd
mv rpmtmp/Bio-ASN1-EntrezGene-1.09/lib/Bio/ASN1 Bio/
rm -rf rpmtmp
#end hack


# Temporary hack for bootstrapping
# Filter unwanted Requires:
# cat << \EOF > %{_builddir}/bioperl-%{version}/%{name}-req
# #!/bin/sh
# %{__perl_requires} $* |\
#   sed -e '/perl(Bio::Tools::Run::Alignment::Clustalw)/d; /perl(Bio::Tools::Run::GenericParameters)/d; /perl(Bio::Tools::Run::Phylo::Molphy::ProtML)/d; /perl(Bio::Tools::Run::Phylo::Phylip::Neighbor)/d; /perl(Bio::Tools::Run::Phylo::Phylip::ProtDist)/d; /perl(Bio::Tools::Run::Phylo::Phylip::ProtPars)/d; /perl(Bio::Tools::Run::RemoteBlast)/d'
# EOF
# 
# %%define __perl_requires %{_builddir}/bioperl-%{version}/%{name}-req
# chmod +x %{__perl_requires}

# remove all execute bits from the doc stuff
find examples -type f -exec chmod -x {} 2>/dev/null ';'

%build
%{__perl} Build.PL --installdirs vendor << EOF
n
a
n
EOF

./Build

# make sure the man page is UTF-8...
cd blib/libdoc
for i in Bio::Tools::GuessSeqFormat.3pm Bio::Tools::Geneid.3pm; do
    iconv --from=ISO-8859-1 --to=UTF-8 $i > new
    mv new $i
done


%install
rm -rf $RPM_BUILD_ROOT
#make pure_install PERL_INSTALL_ROOT=$RPM_BUILD_ROOT
perl Build pure_install --destdir=$RPM_BUILD_ROOT
find $RPM_BUILD_ROOT -type f -a \( -name .packlist \
  -o \( -name '*.bs' -a -empty \) \) -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
# remove errant execute bit from the .pm's
find $RPM_BUILD_ROOT -type f -name '*.pm' -exec chmod -x {} 2>/dev/null ';'
# correct all binaries in /usr/bin to be 0755
find $RPM_BUILD_ROOT/%{_bindir} -type f -name '*.pl' -exec chmod 0755 {} 2>/dev/null ';'

%check
%{?_with_check:./Build test || :}

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
## don't distribute "doc" subdirectory,  doesn't contain docs
%doc examples models 
%doc AUTHORS BUGS Changes DEPRECATED  INSTALL LICENSE PLATFORMS README
%{_bindir}/*
%{perl_vendorlib}/*
%{_mandir}/man1/*.1*
%{_mandir}/man3/*.3*    

%changelog
* Mon Jan 11 2010 Sean Collins <contact@seanmcollins.com> 1.6.0-1.14
- Updated deps

* Thu Sep 25 2008 Alex Lancaster <alexlan[AT]fedoraproject org> - 1.5.2_102-13
- Fix patch fuzz

* Wed Mar  5 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.2_102-12
- bootstrapping done, building normally

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.2_102-11.2
- missed one

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.2_102-11.1
- actually disable bioperl-run requires for bootstrapping

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.2_102-11
- disable bioperl-run requires for bootstrapping

* Tue Mar  4 2008 Tom "spot" Callaway <tcallawa@redhat.com> 1.5.2_102-10
- rebuild for new perl

* Mon Oct 15 2007 Alex Lancaster <alexl@users.sourceforge.net> 1.5.2_102-9
- Add missing BR: perl(Test::More)
- Clarified license terms: GPL+ or Artistic

* Thu May 07 2007 Alex Lancaster <alexl@users.sourceforge.net> 1.5.2_102-8
- Spec file cleanups.
- Improve description.

* Thu Apr 19 2007 Alex Lancaster <alexl@users.sourceforge.net> 1.5.2_102-7
- Fix 'perl Build' command so that it does not attempt CPAN downloads.

* Thu Apr 19 2007 Alex Lancaster <alexl@users.sourceforge.net> 1.5.2_102-6
- Enable scripts, now that bioperl-run is in the repository.

* Tue Apr 03 2007 Alex Lancaster <alexl@users.sourceforge.net> 1.5.2_102-5
- Fix changelog

* Tue Apr 03 2007 Alex Lancaster <alexl@users.sourceforge.net> 1.5.2_102-4
- Disable tests because many of them require network access, add
  _with_check macro so they can be enabled during testing.

* Mon Apr 02 2007 Alex Lancaster <alexl@users.sourceforge.net> 1.5.2_102-3
- Remove BuildRequires: perl(Bio::ASN1::EntrezGene), creates a
  circular dependency, the dependency is still found at install-time.

* Thu Mar 29 2007 Alex Lancaster <alexl@users.sourceforge.net> 1.5.2_102-2
- Add all BRs listed as 'recommends' in Build.PL so that it never
  needs to get packages from CPAN.
- Remove unnecessary filtering of Requires

* Wed Mar 23 2007 Alex Lancaster <alexl@users.sourceforge.net> 1.5.2_102-1
- Update to 1.5.2_102
- Review suggestions from Steven Pritchard
- BR: perl(IO::String)
- Disable scripts for now as they require bioperl-run (not yet packaged)
- Don't mark non-documentation files as documentation.

* Wed Apr 06 2005 Hunter Matthews <thm@duke.edu> 1.5.0-3
- Review suggestions from José Pedro Oliveira

* Mon Apr 01 2005 Hunter Matthews <thm@duke.edu> 1.5.0-2
- Added buildrequires and improved documention entries from FE mailing list.

* Mon Mar 21 2005 Hunter Matthews <thm@duke.edu> 1.5.0-1
- Initial build. I started with the biolinux.org rpm, but broke out 
  most of the deps and built them seperately.
%changelog
