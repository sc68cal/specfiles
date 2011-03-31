Distribution: Custom
Vendor: Custom
Summary: manipulate structured data definitions (SQL and more)
Name: perl-SQL-Translator
Version: 0.07
Release: 1.5.%{distro}
Packager: Sean Collins <contact@seanmcollins.com>
License: GPL or Artistic
Group: Development/Libraries
URL: http://search.cpan.org/dist/SQL-Translator
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildRequires: perl >= 2:5.8.0
BuildRequires: perl, biopackages
BuildRequires: perl-Module-Build, perl-Test-Exception, perl-Test-Differences
Requires: perl-Class-Base, perl-Parse-RecDescent, perl-Test-Exception, perl-Test-Differences, perl-Template-Toolkit
Requires: perl-Spreadsheet-ParseExcel, perl-Text-RecordParser, perl-GraphViz
Requires: perl-IO-stringy, perl-Class-MakeMethods, perl-YAML
Requires: perl-GD

#WTF?
Provides: perl(:)

Source0: SQL-Translator-%{version}.tar.gz

%description
This documentation covers the API for SQL::Translator. For a more general discussion of how to use the modules and scripts, please see SQL::Translator::Manual.

SQL::Translator is a group of Perl modules that converts vendor-specific SQL table definitions into other formats, such as other vendor-specific SQL, ER diagrams, documentation (POD and HTML), XML, and Class::DBI classes. The main focus of SQL::Translator is SQL, but parsers exist for other structured data formats, including Excel spreadsheets and arbitrarily delimited text files. Through the separation of the code into parsers and producers with an object model in between, it's possible to combine any parser with any producer, to plug in custom parsers or producers, or to manipulate the parsed data via the built-in object model. Presently only the definition parts of SQL are handled (CREATE, ALTER), not the manipulation of data (INSERT, UPDATE, DELETE).

%prep
%setup -q -n SQL-Translator-%{version}

%build
CFLAGS="$RPM_OPT_FLAGS" perl Makefile.PL destdir=%{buildroot} < /dev/null
make OPTIMIZE="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

eval `perl '-V:installarchlib'`
mkdir -p $RPM_BUILD_ROOT$installarchlib
%makeinstall

find $RPM_BUILD_ROOT -type f -a \( -name perllocal.pod -o -name .packlist \
  -o \( -name '*.bs' -a -empty \) \) -exec rm -f {} ';'
find $RPM_BUILD_ROOT -type d -depth -exec rmdir {} 2>/dev/null ';'
chmod -R u+w $RPM_BUILD_ROOT/*

[ -x /usr/lib/rpm/brp-compress ] && /usr/lib/rpm/brp-compress

find $RPM_BUILD_ROOT -type f \
| sed "s@^$RPM_BUILD_ROOT@@g" \
> %{name}-%{version}-%{release}-filelist

eval `perl -V:archname -V:installsitelib -V:installvendorlib -V:installprivlib`
for d in $installsitelib $installvendorlib $installprivlib; do
  [ -z "$d" -o "$d" = "UNKNOWN" -o ! -d "$RPM_BUILD_ROOT$d" ] && continue
  find $RPM_BUILD_ROOT$d/* -type d \
  | grep -v "/$archname\(/auto\)\?$" \
  | sed "s@^$RPM_BUILD_ROOT@%dir @g" \
  >> %{name}-%{version}-%{release}-filelist
done

if [ "$(cat %{name}-%{version}-%{release}-filelist)X" = "X" ] ; then
    echo "ERROR: EMPTY FILE LIST"
    exit 1
fi

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root,-)

%changelog
* Mon Jan 11 2010 Sean Collins <contact@seanmcollins.com> 0.07-1.5
- Fixed dep

* Wed Jan 10 2007 bpbuild bpbuild 0.07-1.4
- Added dep
* Thu Nov 30 2006 bpbuild bpbuild 0.07-1.3
- Added dep
* Thu Sep 07 2006 boconnor boconnor 0.07-1.2
- Updates to deps
* Thu Sep 07 2006 boconnor boconnor 0.07-1.1
- Import to stable branch
