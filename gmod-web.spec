%define Sce_version S228C
%define Hsa_version 17

Summary: A gmod-web demo application based on Turnkey. It requires the chado RPM to be installed.
Name: gmod-web
Version: 1.3
Epoch: 1
Release: 1.30.%{distro}
Source0: Turnkey-%{version}.tar.gz
License: GPL
Group: Development/Web
Packager: Sean Collins <contact@seanmcollins.com>
URL: http://turnkey.sf.net
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch: noarch
Requires: postgresql-devel, postgresql-libs, postgresql-server, postgresql >= 7.3
Requires: perl-Apache-ParseFormData, perl-Apache-Session, perl-Class-Base, perl-Class-DBI, perl-Class-DBI-ConceptSearch, perl-Class-DBI-Pager, perl-Class-DBI-Pg = 0.08, perl-Class-DBI-Plugin-Type, perl-DBD-Pg, perl-DBI, perl-Log-Log4perl, perl-SQL-Translator, perl-Template-Toolkit, perl-XML-LibXML, perl-Plucene, perl-Apache2-SOAP, perl-Cache-Cache
Requires: httpd, mod_perl >= 2.0.1
Requires: gbrowse, textpresso, AmiGO, chado, turnkey
BuildRequires: perl, biopackages, turnkey, chado-schema,perl-SQL-Translator
Provides: perl(TurnkeyGmodWeb::Atom::AutoAtom), perl(TurnkeyGmodWeb::Model::AutoDBI)

%description
GMOD Web demos for various databases.

%package Sce
Summary: A gmod-web demo application based on Turnkey. It requires the chado-Sce RPM to be installed.
Group: Development/Web
Requires: postgresql-devel, postgresql-libs, postgresql-server, postgresql >= 7.3
Requires: perl-Apache-ParseFormData, perl-Apache-Session, perl-Class-Base, perl-Class-DBI, perl-Class-DBI-ConceptSearch, perl-Class-DBI-Pager, perl-Class-DBI-Pg = 0.08, perl-Class-DBI-Plugin-Type, perl-DBD-Pg, perl-DBI, perl-Log-Log4perl, perl-SQL-Translator, perl-Template-Toolkit, perl-XML-LibXML, perl-Lucene, perl-Apache2-SOAP, perl-Cache-Cache
Requires: httpd, mod_perl >= 2.0.1
Requires: chado-Sce, gbrowse, textpresso, AmiGO, genome-Sce-nib, genome-Sce, blastGraphic-Sce, genome-Sce-blast, turnkey
BuildRequires: turnkey, perl, biopackages, chado-schema
Provides: perl(TurnkeySceS228C::Atom::AutoAtom), perl(TurnkeySceS228C::Model::AutoDBI)

%description Sce
The Wiki web application demo for turnkey.

%package Hsa
Summary: A gmod-web demo application based on Turnkey. It requires the chado-Hsa RPM to be installed.
Group: Development/Web
Requires: postgresql-devel, postgresql-libs, postgresql-server, postgresql >= 7.3
Requires: perl-Apache-ParseFormData, perl-Apache-Session, perl-Class-Base, perl-Class-DBI, perl-Class-DBI-ConceptSearch, perl-Class-DBI-Pager, perl-Class-DBI-Pg = 0.08, perl-Class-DBI-Plugin-Type, perl-DBD-Pg, perl-DBI, perl-Log-Log4perl, perl-SQL-Translator, perl-Template-Toolkit, perl-XML-LibXML, perl-Lucene, perl-Apache2-SOAP, perl-Cache-Cache
Requires: httpd, mod_perl >= 2.0.1
Requires: chado-Hsa, gbrowse, textpresso, AmiGO, genome-Hsa-nib, genome-Hsa, blastGraphic-Hsa, genome-Hsa-blast, turnkey 
BuildRequires: turnkey, perl, biopackages, chado-schema
Provides: perl(TurnkeyHsa17::Atom::AutoAtom), perl(TurnkeyHsa17::Model::AutoDBI)


%description Hsa
The Wiki web application demo for turnkey.

%package Hsa-normal-tissue
Summary: A gmod-web demo application based on Turnkey. It requires the chado-Hsa RPM to be installed.
Group: Development/Web
Requires: postgresql-devel, postgresql-libs, postgresql-server, postgresql >= 7.3
Requires: perl-Apache-ParseFormData, perl-Apache-Session, perl-Class-Base, perl-Class-DBI, perl-Class-DBI-ConceptSearch, perl-Class-DBI-Pager, perl-Class-DBI-Pg = 0.08, perl-Class-DBI-Plugin-Type, perl-DBD-Pg, perl-DBI, perl-Log-Log4perl, perl-SQL-Translator, perl-Template-Toolkit, perl-XML-LibXML, perl-Lucene, perl-Apache2-SOAP, perl-Cache-Cache
Requires: httpd, mod_perl >= 2.0.1
Requires: chado-Hsa, gbrowse, textpresso, AmiGO, turnkey
#gmod-web-Hsa-normal-tissue-probeset-barcharts
BuildRequires: turnkey, perl, biopackages, chado-schema
Provides: perl(TurnkeyHsa17NormalTissue::Atom::AutoAtom), perl(TurnkeyHsa17NormalTissue::Model::AutoDBI)

%description Hsa-normal-tissue
The Wiki web application demo for turnkey.

%prep
%setup -n Turnkey-%{version}

%build

%install
%{_bindir}/turnkey_generate --use_web_caching=0 --search_engine=lucene --output_type=web_mod_perl --dbuser=postgres --dbpass= --dbhost=localhost --wwwemail=admin@host --sqlfile_path=/var/lib/gmod/src/chado/modules/default_nofuncs.sql --skip_tables=affymetrixprobeset,affymetrixprobe,affymetrixcel,affymetrixsnp,affymetrixmas5,affymetrixdchip,affymetrixvsn,affymetrixsea,affymetrixplier,affymetrixdabg,affymetrixrma,affymetrixgcrma,affymetrixprobesetstat --dbname=chado --output_path=%{buildroot}/var/www/gmod-web-demo --install_path=/var/www/gmod-web-demo --dbport=5432 --concat=GmodWeb --uri_prefix=GmodWeb --virtual=N --wwwport=80 --wwwhost=$HOSTNAME --usedemo=1 --demo=gmod-web 2>&1 >/dev/null;
%{_bindir}/turnkey_generate --use_web_caching=0 --search_engine=lucene --output_type=web_mod_perl --dbuser=postgres --dbpass= --dbhost=localhost --wwwemail=admin@host --sqlfile_path=/var/lib/gmod/src/chado/modules/default_nofuncs.sql --skip_tables=affymetrixprobeset,affymetrixprobe,affymetrixcel,affymetrixsnp,affymetrixmas5,affymetrixdchip,affymetrixvsn,affymetrixsea,affymetrixplier,affymetrixdabg,affymetrixrma,affymetrixgcrma,affymetrixprobesetstat --dbname=chado-Sce-%{Sce_version} --output_path=%{buildroot}/var/www/Sce/%{Sce_version} --install_path=/var/www/Sce/%{Sce_version} --dbport=5432 --concat=Sce%{Sce_version} --uri_prefix=Sce/%{Sce_version} --virtual=N --wwwport=80 --wwwhost=$HOSTNAME --usedemo=1 --demo=gmod-web-Sce 2>&1 >/dev/null;
%{_bindir}/turnkey_generate --use_web_caching=0 --search_engine=lucene --output_type=web_mod_perl --dbuser=postgres --dbpass= --dbhost=localhost --wwwemail=admin@host --sqlfile_path=/var/lib/gmod/src/chado/modules/default_nofuncs.sql --skip_tables=affymetrixprobeset,affymetrixprobe,affymetrixcel,affymetrixsnp,affymetrixmas5,affymetrixdchip,affymetrixvsn,affymetrixsea,affymetrixplier,affymetrixdabg,affymetrixrma,affymetrixgcrma,affymetrixprobesetstat --dbname=chado-Hsa-%{Hsa_version} --output_path=%{buildroot}/var/www/Hsa/%{Hsa_version} --install_path=/var/www/Hsa/%{Hsa_version} --dbport=5432 --concat=Hsa%{Hsa_version} --uri_prefix=Hsa/%{Hsa_version} --virtual=N --wwwport=80 --wwwhost=$HOSTNAME --usedemo=1 --demo=gmod-web-Hsa 2>&1 >/dev/null;
%{_bindir}/turnkey_generate --use_web_caching=0 --search_engine=lucene --output_type=web_mod_perl --dbuser=postgres --dbpass= --dbhost=localhost --wwwemail=admin@host --sqlfile_path=/var/lib/gmod/src/chado/modules/default_nofuncs.sql --skip_tables=affymetrixprobeset,affymetrixprobe,affymetrixcel,affymetrixsnp,affymetrixmas5,affymetrixdchip,affymetrixvsn,affymetrixsea,affymetrixplier,affymetrixdabg,affymetrixrma,affymetrixgcrma,affymetrixprobesetstat --dbname=chado-Hsa-%{Hsa_version} --output_path=%{buildroot}/var/www/Hsa-Normal-Tissue/%{Hsa_version} --install_path=/var/www/Hsa-Normal-Tissue/%{Hsa_version} --dbport=5432 --concat=Hsa%{Hsa_version}NormalTissue --uri_prefix=HsaNormalTissue/%{Hsa_version} --virtual=N --wwwport=80 --wwwhost=$HOSTNAME --usedemo=1 --demo=normal-tissue 2>&1 >/dev/null;

%post
cp /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf.rpmsave
echo 'Include /var/www/gmod-web-demo/conf/httpd.conf' >> /etc/httpd/conf/httpd.conf
# the cache dir needs to be owned by apache
chown apache:apache /var/www/gmod-web-demo/cache_root
# this ensures the DB has been initialized
/etc/init.d/postgresql restart
# the changes below are to allow GMODWeb to connect to the local database over TCP/IP
# for postgres on FC2 & CentOS4
perl -p -i -e 's!#tcpip_socket = false!tcpip_socket = true!' /var/lib/pgsql/data/postgresql.conf
perl -p -i -e 's!#host    all         all         127.0.0.1         255.255.255.255   trust!host    all         all         127.0.0.1         255.255.255.255   trust!' /var/lib/pgsql/data/pg_hba.conf
# for postgres on FC5
perl -p -i -e 's!host    all         all         127.0.0.1/32          ident sameuser!host    all         all         127.0.0.1/32          trust!' /var/lib/pgsql/data/pg_hba.conf
# this ensures the access restriction changes have been lifted
/etc/init.d/postgresql restart
# index sample articles
/usr/bin/textpresso_inject_pdf /var/www/gmod-web-demo/html/articles/GO_nature_genetics_2000.pdf
# index cvterms
mkdir -p /var/www/gmod-web-demo/lucene
%{_bindir}/gmodweb_indexer_by_db "/GmodWeb/db/Cvterm" /var/www/gmod-web-demo/lucene NA cvterm localhost 5432 chado 1
/etc/init.d/httpd restart

%post Sce
cp /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf.rpmsave
echo 'Include /var/www/Sce/%{Sce_version}/conf/httpd.conf' >> /etc/httpd/conf/httpd.conf
# the cache dir needs to be owned by apache
chown apache:apache /var/www/Sce/%{Sce_version}/cache_root
# this ensures the DB has been initialized
/etc/init.d/postgresql restart
# the changes below are to allow GMODWeb to connect to the local database over TCP/IP
# for postgres on FC2 & CentOS4
perl -p -i -e 's!#tcpip_socket = false!tcpip_socket = true!' /var/lib/pgsql/data/postgresql.conf
perl -p -i -e 's!#host    all         all         127.0.0.1         255.255.255.255   trust!host    all         all         127.0.0.1         255.255.255.255   trust!' /var/lib/pgsql/data/pg_hba.conf
# for postgres on FC5
perl -p -i -e 's!host    all         all         127.0.0.1/32          ident sameuser!host    all         all         127.0.0.1/32          trust!' /var/lib/pgsql/data/pg_hba.conf
# this ensures the access restriction changes have been lifted
/etc/init.d/postgresql restart
# index sample articles
/usr/bin/textpresso_inject_pdf /var/www/Sce/%{Sce_version}/html/articles/GO_nature_genetics_2000.pdf
/usr/bin/textpresso_inject_pdf /var/www/Sce/%{Sce_version}/html/articles/genetic_and_physical_maps_of_Saccharomyces_cerevisiae.pdf
cp /usr/share/doc/turnkey-%{version}/conf/chado-Sce-S228C.conf /etc/bioinformatics/gbrowse.conf/chado-Sce-S228C.conf
ln -s /usr/share/genome/Sce/%{Sce_version}/* /var/www/Sce/%{Sce_version}/html/files/
# index features & cvterms
mkdir -p /var/www/Sce/%{Sce_version}/lucene
%{_bindir}/gmodweb_indexer_by_db "/Sce/%{Sce_version}/db/Feature" /var/www/Sce/%{Sce_version}/lucene 10159,9689,9813 feature localhost 5432 chado-Sce-%{Sce_version} 1
%{_bindir}/gmodweb_indexer_by_db "/Sce/%{Sce_version}/db/Cvterm" /var/www/Sce/%{Sce_version}/lucene NA cvterm localhost 5432 chado-Sce-%{Sce_version} 0
/etc/init.d/httpd restart

%post Hsa
cp /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf.rpmsave
echo 'Include /var/www/Hsa/%{Hsa_version}/conf/httpd.conf' >> /etc/httpd/conf/httpd.conf
# the cache dir needs to be owned by apache
chown apache:apache /var/www/Hsa/%{Hsa_version}/cache_root
# this ensures the DB has been initialized
/etc/init.d/postgresql restart
# the changes below are to allow GMODWeb to connect to the local database over TCP/IP
# for postgres on FC2 & CentOS4
perl -p -i -e 's!#tcpip_socket = false!tcpip_socket = true!' /var/lib/pgsql/data/postgresql.conf
perl -p -i -e 's!#host    all         all         127.0.0.1         255.255.255.255   trust!host    all         all         127.0.0.1         255.255.255.255   trust!' /var/lib/pgsql/data/pg_hba.conf
# for postgres on FC5
perl -p -i -e 's!host    all         all         127.0.0.1/32          ident sameuser!host    all         all         127.0.0.1/32          trust!' /var/lib/pgsql/data/pg_hba.conf
# this ensures the access restriction changes have been lifted
/etc/init.d/postgresql restart
# index sample articles
/usr/bin/textpresso_inject_pdf /var/www/Hsa/%{Hsa_version}/html/articles/GO_nature_genetics_2000.pdf
/usr/bin/textpresso_inject_pdf /var/www/Hsa/%{Hsa_version}/html/articles/a_physical_map_of_the_human_genome.pdf
/usr/bin/textpresso_inject_pdf /var/www/Hsa/%{Hsa_version}/html/articles/the_sequence_of_the_human_genome.pdf
cp /usr/share/doc/turnkey-%{version}/conf/chado-Hsa-17.conf /etc/bioinformatics/gbrowse.conf/chado-Hsa-17.conf
ln -s /usr/share/genome/Hsa/%{Hsa_version}/* /var/www/Hsa/%{Hsa_version}/html/files/
# index features & cvterms
mkdir -p /var/www/Hsa/%{Hsa_version}/lucene
%{_bindir}/gmodweb_indexer_by_db "/Hsa/%{Hsa_version}/db/Feature" /var/www/Hsa/%{Hsa_version}/lucene 10159,9689,9813 feature localhost 5432 chado-Hsa-%{Hsa_version} 1
%{_bindir}/gmodweb_indexer_by_db "/Hsa/%{Hsa_version}/db/Cvterm" /var/www/Hsa/%{Hsa_version}/lucene NA cvterm localhost 5432 chado-Hsa-%{Hsa_version} 0
/etc/init.d/httpd restart

%post Hsa-normal-tissue
cp /etc/httpd/conf/httpd.conf /etc/httpd/conf/httpd.conf.rpmsave
echo 'Include /var/www/Hsa-Normal-Tissue/%{Hsa_version}/conf/httpd.conf' >> /etc/httpd/conf/httpd.conf
# the cache dir needs to be owned by apache
chown apache:apache /var/www/Hsa-Normal-Tissue/%{Hsa_version}/cache_root
# this ensures the DB has been initialized
/etc/init.d/postgresql restart
# the changes below are to allow GMODWeb to connect to the local database over TCP/IP
# for postgres on FC2 & CentOS4
perl -p -i -e 's!#tcpip_socket = false!tcpip_socket = true!' /var/lib/pgsql/data/postgresql.conf
perl -p -i -e 's!#host    all         all         127.0.0.1         255.255.255.255   trust!host    all         all         127.0.0.1         255.255.255.255   trust!' /var/lib/pgsql/data/pg_hba.conf
# for postgres on FC5
perl -p -i -e 's!host    all         all         127.0.0.1/32          ident sameuser!host    all         all         127.0.0.1/32          trust!' /var/lib/pgsql/data/pg_hba.conf
# this ensures the access restriction changes have been lifted
/etc/init.d/postgresql restart
# index sample articles
/usr/bin/textpresso_inject_pdf /var/www/Hsa-Normal-Tissue/%{Hsa_version}/html/articles/GO_nature_genetics_2000.pdf
/usr/bin/textpresso_inject_pdf /var/www/Hsa-Normal-Tissue/%{Hsa_version}/html/articles/a_physical_map_of_the_human_genome.pdf
/usr/bin/textpresso_inject_pdf /var/www/Hsa-Normal-Tissue/%{Hsa_version}/html/articles/the_sequence_of_the_human_genome.pdf
cp /usr/share/doc/turnkey-%{version}/conf/chado-Hsa-17.conf /etc/bioinformatics/gbrowse.conf/chado-Hsa-17.conf
ln -s /usr/share/genome/Hsa/%{Hsa_version}/* /var/www/Hsa-Normal-Tissue/%{Hsa_version}/html/files/
# index features & cvterms
mkdir -p /var/www/Hsa-Normal-Tissue/%{Hsa_version}/lucene
%{_bindir}/gmodweb_indexer_by_db "/HsaNormalTissue/%{Hsa_version}/db/Feature" /var/www/Hsa-Normal-Tissue/%{Hsa_version}/lucene 10159,9689,9813 feature localhost 5432 chado-Hsa-%{Hsa_version} 1
%{_bindir}/gmodweb_indexer_by_db "/HsaNormalTissue/%{Hsa_version}/db/Cvterm" /var/www/Hsa-Normal-Tissue/%{Hsa_version}/lucene NA cvterm localhost 5432 chado-Hsa-%{Hsa_version} 0
/etc/init.d/httpd restart

%postun
/etc/init.d/httpd stop
perl -p -i -e 's!Include /var/www/gmod-web-demo/conf/httpd.conf!!' /etc/httpd/conf/httpd.conf
rm -rf /var/www/gmod-web-demo
/etc/init.d/httpd start

%postun Sce
/etc/init.d/httpd stop
perl -p -i -e 's!Include /var/www/Sce/%{Sce_version}/conf/httpd.conf!!' /etc/httpd/conf/httpd.conf
rm -rf /var/www/Sce/%{Sce_version}
/etc/init.d/httpd start

%postun Hsa
/etc/init.d/httpd stop
perl -p -i -e 's!Include /var/www/Hsa/%{Hsa_version}/conf/httpd.conf!!' /etc/httpd/conf/httpd.conf
rm -rf /var/www/Hsa/%{Hsa_version}
/etc/init.d/httpd start

%postun Hsa-normal-tissue
/etc/init.d/httpd stop
perl -p -i -e 's!Include /var/www/Hsa-Normal-Tissue/%{Hsa_version}/conf/httpd.conf!!' /etc/httpd/conf/httpd.conf
rm -rf /var/www/Hsa-Normal-Tissue/%{Hsa_version}
/etc/init.d/httpd start

%clean
[ "%{buildroot}" != "/" ] && [ -d %{buildroot} ] && rm -rf %{buildroot};

%files
%doc README INSTALL LICENSE
/var/www/gmod-web-demo/*

%files Sce
%doc README INSTALL LICENSE
/var/www/Sce/%{Sce_version}/*

%files Hsa
%doc README INSTALL LICENSE
/var/www/Hsa/%{Hsa_version}/*

%files Hsa-normal-tissue
%doc README INSTALL LICENSE
/var/www/Hsa-Normal-Tissue/%{Hsa_version}/*

%changelog
* Mon Jan 11 2010 Sean Collins <contact@seanmcollins.com> 1.3-1.30
- Updated deps

* Mon Feb 05 2007 bpbuild bpbuild 1.3-1.29
- Updated version number of gmod-web, turnkey
* Fri Jan 26 2007 bpbuild bpbuild 1.3-1.28
- Updated deps
* Thu Jan 25 2007 bpbuild bpbuild 1.3-1.27
- Added version requirement so our patched version of class-dbi-pg will
  be used.
* Mon Jan 15 2007 bpbuild bpbuild 1.3-1.26
- Incremented the version number for Turnkey, 1.2 release includes bug
  fixes with the gmodweb demos.
* Mon Jan 15 2007 bpbuild bpbuild 1.3-1.25
- This fixes a problem where, on a clean install box, the hostname is
  localhost so search results have localhost hardcoded into their URLs.
* Sun Jan 14 2007 bpbuild bpbuild 1.3-1.24
- Updated for next release, gmodweb sites include some sample artilces
  for textpresso
* Sun Jan 14 2007 bpbuild bpbuild 1.3-1.23
- Updated spec for 1.1 release
* Sat Jan 13 2007 bpbuild bpbuild 1.3-1.22
- I added script to update the postgres settings on a new install so
  that the GMODWeb application can connect to the underlying database.
* Tue Jan 09 2007 bpbuild bpbuild 1.3-1.21
- Update deps
* Mon Jan 08 2007 bpbuild bpbuild 1.3-1.20
- updates
* Mon Jan 08 2007 bpbuild bpbuild 1.3-1.19
- Updates
* Thu Jan 04 2007 bpbuild bpbuild 1.3-1.18
- foo
* Wed Jan 03 2007 bpbuild bpbuild 1.3-1.17
- Updated the Amigo spec.in file to include an embeddable theme
* Wed Sep 13 2006 boconnor boconnor 1.3-1.16
- Now that I've consolidated RPM versions for the deps it seems as
  though this patch is required for FC2.
* Wed Sep 13 2006 boconnor boconnor 1.3-1.15
- Added blast graphic deps
* Wed Sep 13 2006 boconnor boconnor 1.3-1.14
- Nib and fasta files for Hsa and Sce.
* Wed Sep 13 2006 boconnor boconnor 1.3-1.13
- Nib and fasta files for Hsa and Sce.
* Wed Sep 13 2006 boconnor boconnor 1.3-1.12
- The demo for Hsa and Sce GMODWeb sites was not specified correctly.
* Tue Sep 12 2006 boconnor boconnor 1.3-1.11
- Incremented version since turnkey changed
* Tue Sep 12 2006 boconnor boconnor 1.3-1.10
- trigger new version
* Wed Jun 28 2006 boconnor boconnor 1.3-1.9
- Updated spec files
* Tue Jun 27 2006 boconnor boconnor 1.3-1.8
- Updates to gmod-web spec file for turnkey 1.0 release
* Tue Jun 27 2006 boconnor boconnor 1.3-1.7
- 1.0 release of Turnkey
* Tue Mar 21 2006 boconnor boconnor 1.3-1.6
- Updated the Turnkey these rpms are built with
* Tue Mar 21 2006 boconnor boconnor 1.3-1.5
- Got rid of the probeset_svg requirement for
  gmod-web-Hsa-Normal-Tissue. I will add it back in when this RPM is
  finished.
* Mon Mar 20 2006 boconnor boconnor 1.3-1.4
- Added spec file for probeset SVGs for normal tissue website.	I don't
  know if the shell used in the RRM build process is going to barf with
  this many files.
* Mon Mar 20 2006 boconnor boconnor 1.3-1.3
- Updated the turnkey source
* Sat Mar 11 2006 boconnor boconnor 1.3-1.2
- Updates to the gmod-web spec
* Fri Mar 10 2006 boconnor boconnor 1.3-1.1
- Added spec.in files for Turnkey and GMOD-Web RPMs. I will add spec.in
  files for all the dependencies before the next release.
