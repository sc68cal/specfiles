#$Id: turnkey.spec.in,v 1.22 2007/02/05 03:48:55 bpbuild Exp $

Distribution: Custom
Vendor: biopackages.net
Summary: Turnkey generates a mod_perl website from a database schema file.
Name: turnkey
Version: 1.4
Epoch: 2
Release: 1.%{distro}
Packager: contact@seanmcollins.com
License: GPL or Artistic
Group: Development/Web
URL: http://turnkey.sf.net
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
BuildRequires: perl, biopackages
Requires: httpd, mod_perl >= 2.0.1
Requires: perl-Apache-ParseFormData, perl-Apache-Session
Requires: perl-Class-Base, perl-Class-DBI, perl-Class-DBI-ConceptSearch, perl-Class-DBI-Pager, perl-Class-DBI-Pg, perl-Class-DBI-Plugin-Type, perl-DBD-Pg, perl-DBI, perl-Log-Log4perl, perl-SQL-Translator, perl-Template-Toolkit, perl-XML-LibXML, perl-Apache2-SOAP, perl-Cache-Cache, perl-Plucene, perl-Class-Data-Inheritable
Provides: perl(Turnkey::Atom::AutoAtom), perl(Turnkey::Model::AutoDBI) 
# need to remove all this mod_perl 1 stuff from the codebase
Provides: perl(Apache::Const), perl(Apache::RequestIO), perl(Apache::RequestRec), perl(Apache::RequestUtil)

# perl(Lucene) has been changed to perl(Plucene), and the install process screws up
AutoReq: no


Source0: Turnkey-%{version}.tar.gz
#Patch0: Turnkey-%{version}-disconnect.patch

%description
The Turnkey project makes it easy to quickly convert a database schema file into a mod_perl database.

%prep
%setup -q -n Turnkey-%{version}
# only apply this patch on centos where calling disconnect on model object db
# handles causes problems because db handles appear to be recycled when they
# aren't on FC2
#distro_str=%{distro}
#if [ ${distro_str:0:9} == "bp.centos" ]; then
#echo "Detected CentOS, patching and removing disconnect call in model objects"
#%patch -p1
#else
#echo "Not applying Centos patch"
#fi


#substitute in "hard coded" $TURNKEY_ROOT path for rpm
perl -p -i -e 's!(\$ENV{TURNKEY_ROOT})!$1 or my \$working_dir = "%{_datadir}/doc/%{name}-%{version}/"!' scripts/turnkey_generate;

%build
CFLAGS="$RPM_OPT_FLAGS" perl Makefile.PL PREFIX=$RPM_BUILD_ROOT%{_prefix}  < /dev/null
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

[ -x %{_usr}/lib/rpm/brp-compress ] && %{_usr}/lib/rpm/brp-compress

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
%doc README INSTALL LICENSE meta conf schema demo tt2 html turnkeylib plugin

%changelog
* Tue Jan 05 2010 Sean Collins <contact@seanmcollins.com> 1.4-1
- Updated to turnkey 1.4 

* Mon Feb 05 2007 bpbuild bpbuild 1.3-1.22
- Updated version number of gmod-web, turnkey
* Mon Jan 15 2007 bpbuild bpbuild 1.3-1.21
- Incremented the version number for Turnkey, 1.2 release includes bug
  fixes with the gmodweb demos.
* Sun Jan 14 2007 bpbuild bpbuild 1.3-1.20
- Updates to supress uneeded errors for dep resolution in yum
* Sun Jan 14 2007 bpbuild bpbuild 1.3-1.19
- Updated turnkey, these are changes to the source file that include
  bug fixes for 1.2 release. Some new files all for gmod web demos
* Mon Jan 08 2007 bpbuild bpbuild 1.3-1.18
- Updated deps
* Mon Jan 08 2007 bpbuild bpbuild 1.3-1.17
- First attempt at updating the Turnkey RPM to 1.1 release.
* Wed Jan 03 2007 bpbuild bpbuild 1.3-1.16
- Updated the Amigo spec.in file to include an embeddable theme
* Tue Jan 02 2007 bpbuild bpbuild 1.3-1.15
- Changes to spec file
* Wed Sep 13 2006 boconnor boconnor 1.3-1.14
- Now that I've consolidated RPM versions for the deps it seems as
  though this patch is required for FC2.
* Tue Sep 12 2006 boconnor boconnor 1.3-1.13
- Updates to distro check
* Tue Sep 12 2006 boconnor boconnor 1.3-1.12
- Updates to distro check
* Tue Sep 12 2006 boconnor boconnor 1.3-1.11
- Updates to distro check
* Tue Sep 12 2006 boconnor boconnor 1.3-1.10
- Added conditional patch to remove disconnect calls on CentOS where
  some odd cacheing problem is causing the server to barf
* Tue Sep 12 2006 boconnor boconnor 1.3-1.9
- trigger new version
* Sat Jul 15 2006 boconnor boconnor 1.3-1.8
- I updated the hardcoded /usr directory in all the spec files.  This
  was to support MacOS which installs all RPMs into /usr/local.  It
  uses a RPM macro now to make it platform neutral.  I've also updated
  some other SPEC files to support MacOS, I've done my best to ensure
  any changes don't affect other platforms negatively
* Tue Jun 27 2006 boconnor boconnor 1.3-1.7
- 1.0 release of Turnkey
* Wed Mar 22 2006 boconnor boconnor 1.3-1.6
- Tried upping the epoc on turnkey
* Tue Mar 21 2006 boconnor boconnor 1.3-1.5
- Updated the gzip
* Tue Mar 21 2006 boconnor boconnor 1.3-1.4
- Updated source gzip
* Mon Mar 20 2006 boconnor boconnor 1.3-1.3
- Updated the source gzip.
* Sat Mar 11 2006 boconnor boconnor 1.3-1.2
- Updates to the gmod-web spec
* Fri Mar 10 2006 boconnor boconnor 1.3-1.1
- Added spec.in files for Turnkey and GMOD-Web RPMs. I will add spec.in
  files for all the dependencies before the next release.
