#$Id: gbrowse.spec.in,v 1.9 2009/03/25 20:26:40 allenday Exp $
Summary: The Generic Genome Browser
Name: gbrowse
Version: 1.69
Release: 1.9.%{distro}
Packager: allenday@ucla.edu
License: GPL or Artistic
Group: Development/Libraries
URL: http://www.gmod.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root

BuildRequires: gd >= 2.0.33
BuildRequires: perl-Bio-Graphics
BuildRequires: perl-CGI-Session
BuildRequires: perl-ExtUtils-CBuilder
BuildRequires: perl-FCGI
BuildRequires: perl-GD
BuildRequires: perl-JSON
BuildRequires: perl-bioperl >= 1.6.0

Requires: gd >= 2.0.33
Requires: perl-Bio-Das
Requires: perl-Bio-Graphics
Requires: perl-Bio-PrimerDesigner
Requires: perl-CGI-Session
#Requires: perl-DB_File-Lock
Requires: perl-ExtUtils-CBuilder
Requires: perl-FCGI
Requires: perl-GD
Requires: perl-JSON
Requires: perl-Math-FFT
Requires: perl-Math-Round
#Requires: perl-Safe-World
Requires: perl-bioperl >= 1.6.0
Requires: perl-bioperl-db

Source0: Generic-Genome-Browser-%{version}.tar.gz
#Source1: Generic-Genome-Browser-%{version}-Makefile.PL
Patch0: Generic-Genome-Browser-%{version}-Ace.patch
#Patch1: Generic-Genome-Browser-%{version}-MOBY.patch
Patch2: Generic-Genome-Browser-%{version}-Chado.patch

%description
Built from the Generic-Genome-Browser-1.69.tar.gz release

%prep
rm -rf $RPM_BUILD_ROOT
%setup -q -n Generic-Genome-Browser-%{version}
#%patch0 -p1
#%patch1 -p1
#%patch2 -p1

%build
CFLAGS="$RPM_OPT_FLAGS" perl Makefile.PL --SELINUX=1 \
  PREFIX=$RPM_BUILD_ROOT \
  LIB=$RPM_BUILD_ROOT%{perl_sitelib} \
  INSTALLSITEMAN3DIR=$RPM_BUILD_ROOT%{_datadir} \
  INSTALLSITEMAN1DIR=$RPM_BUILD_ROOT%{_datadir} \
  INSTALLBIN=$RPM_BUILD_ROOT%{_bindir} \
  BIN=$RPM_BUILD_ROOT%{_bindir} \
  CONF=$RPM_BUILD_ROOT/etc/bioinformatics \
  HTDOCS=$RPM_BUILD_ROOT/var/www/html \
  CGIBIN=$RPM_BUILD_ROOT/var/www/cgi-bin/gbrowse < /dev/null
make OPTIMIZE="$RPM_OPT_FLAGS"
#CFLAGS="$RPM_OPT_FLAGS" perl Makefile.PL PREFIX=$RPM_BUILD_ROOT%{_prefix}  < /dev/null
#make OPTIMIZE="$RPM_OPT_FLAGS"

%install
rm -rf $RPM_BUILD_ROOT

eval `perl '-V:installarchlib'`
mkdir -p $RPM_BUILD_ROOT$installarchlib
%makeinstall

find $RPM_BUILD_ROOT -type f -exec perl -p -i -e "s!$RPM_BUILD_ROOT!!g" {} \;

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

%post
mkdir /var/www/html/gbrowse/tmp
chmod a+rwx /var/www/html/gbrowse/tmp
chown -R apache.apache /var/www/html/gbrowse
chown -R apache.apache /var/www/cgi-bin/gbrowse

%clean
rm -rf $RPM_BUILD_ROOT

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root,-)

%changelog
* Wed Mar 25 2009 allenday allenday 1.69-1.9
- permissions
* Wed Mar 25 2009 allenday allenday 1.69-1.8
- path tweak
* Sun Mar 22 2009 allenday allenday 1.69-1.7
- depcheck
* Sat Mar 21 2009 allenday allenday 1.69-1.6
- update to 1.69 release
* Tue Mar 17 2009 allenday allenday 1.69-1.5
- bringing up to head
* Tue Mar 17 2009 allenday allenday 1.69-1.4
- bringing up to head
* Fri Jan 05 2007 bpbuild bpbuild 1.69-1.3
- SELinux
* Sat Jul 15 2006 boconnor boconnor 1.69-1.2
- I updated the hardcoded /usr directory in all the spec files.  This
  was to support MacOS which installs all RPMs into /usr/local.  It
  uses a RPM macro now to make it platform neutral.  I've also updated
  some other SPEC files to support MacOS, I've done my best to ensure
  any changes don't affect other platforms negatively
* Mon Jul 10 2006 boconnor boconnor 1.69-1.1
- Added spec.in files for several packages that were previously built
  on the testing branch and not yet imported into the biopackages
  system
