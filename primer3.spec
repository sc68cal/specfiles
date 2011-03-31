Vendor: biopackages.net
Group: Applications/Scientific
Packager: Sean Collins <contact@seanmcollins.com>
Version: 1.1.4
Release: 1.12.%{distro}
Name:     primer3
Summary:  Primer3 picks primers for PCR reactions
License:  Copyright Whitehead Institute for Biomedical Research
URL:      http://fokker.wi.mit.edu/primer3/
#Source:   http://fokker.wi.mit.edu/primer3/primer3_%{version}.tar.gz
Source:   %{name}-%{version}.tar.gz
BuildRequires: gcc
BuildRoot: %{_tmppath}/%{name}-root

%description
Primer3 is a complete rewrite of the original PRIMER program
(Primer 0.5), written by Steve Lincoln, Mark Daly, and Eric
Lander.

Primer3 picks primers for PCR reactions, considering as criteria:
- oligonucleotide melting temperature, size, GC content,
  and primer-dimer possibilities
- PCR product size
- positional constraints within the source sequence
- miscellaneous other constraints
All of these criteria are user-specifiable as constraints, and
some are specifiable as terms in an objective function that
characterizes an optimal primer pair.

Reference for Primer3:

We also request that use of this software be cited in publications as 

   Rozen, S., Skaletsky, H.  "Primer3 on the WWW for general 
   users and for biologist programmers."  In S. Krawetz and
   S. Misener, eds. Bioinformatics Methods and Protocols in
   the series Methods in Molecular Biology.  Humana Press, 
   Totowa, NJ, 2000, pages 365-386. Code available at
   http://fokker.wi.mit.edu/primer3/
   
%prep
rm -rf %{name}-%{version}
mkdir %{name}-%{version}
cd %{name}-%{version}
tar -xvzf %{SOURCE0}
#%setup -q -n %{name}-%{version}
perl -pi -e 's[/usr/local/bin][/usr/bin]g' test/dpal_gen.pl
perl -pi -e 's[/usr/local/bin][/usr/bin]g' test/long_seq_tm_test.pl
perl -pi -e 's[/usr/bin/perl5][%{__perl}]g' test/dpal_gen.pl
perl -pi -e 's[/usr/bin/perl5][%{__perl}]g' test/long_seq_tm_test.pl
perl -pi -e 's[/usr/bin/perl][%{__perl}]g' test/dpal_gen.pl
perl -pi -e 's[/usr/bin/perl][%{__perl}]g' test/long_seq_tm_test.pl

%build
export CC=%{__cc}
export CFLAGS="$RPM_OPT_FLAGS"
export LDLIBS="-lm"
cd %{name}-%{version}/src
make primer3_core
make ntdpal
#cd ../test
#perl -w primer_test.pl
#perl -w dpal_test.pl

%install
rm -rf %{buildroot}

install -m 755 -d %{buildroot}%{_bindir}
install -m 755 -d %{buildroot}%{_datadir}/%{name}-%{version}
install -m 755 %{name}-%{version}/src/primer3_core %{buildroot}%{_bindir}
ln -s %{_bindir}/primer3_core %{buildroot}%{_bindir}/primer3
install -m 755 %{name}-%{version}/src/ntdpal %{buildroot}%{_bindir}
#cp -pR %{name}-%{version}/test %{buildroot}%{_datadir}/%{name}-%{version}

%clean
rm -rf %{buildroot}

# ----------------------------------------------------------------------------

%files
%defattr(-,root,root)
%{_bindir}/*
%{_datadir}/%{name}-%{version}
%doc %{name}-%{version}/COPYING.txt %{name}-%{version}/README.txt %{name}-%{version}/example
%doc %{name}-%{version}/src/release_notes.txt

# ----------------------------------------------------------------------------

%changelog

* Mon Jan 4  2010 Sean Collins <contact@seanmcollins.com> 1.1.4-1.12
- Updated Deps
* Sun Mar 22 2009 allenday allenday 1.1.4-1.11
- version increment
* Sun Mar 22 2009 allenday allenday 1.1.4-1.10
- version increment
* Sun Mar 22 2009 allenday allenday 1.1.4-1.9
- version increment
* Sun Mar 22 2009 allenday allenday 1.1.4-1.8
- version increment
* Sun Mar 22 2009 allenday allenday 1.1.4-1.7
- version increment
* Sun Mar 22 2009 allenday allenday 1.1.4-1.6
- version increment
* Sun Mar 22 2009 allenday allenday 1.1.4-1.5
- version increment
* Sun Mar 22 2009 allenday allenday 1.1.4-1.4
- version increment
* Wed Aug 30 2006 allenday allenday 1.1.4-1.3
- symlink to "primer3"
* Sat Jul 15 2006 boconnor boconnor 1.1.4-1.2
- I updated the hardcoded /usr directory in all the spec files.  This
  was to support MacOS which installs all RPMs into /usr/local.  It
  uses a RPM macro now to make it platform neutral.  I've also updated
  some other SPEC files to support MacOS, I've done my best to ensure
  any changes don't affect other platforms negatively
* Mon Jul 10 2006 boconnor boconnor 1.1.4-1.1
- Import of spec.in from the testing repo
