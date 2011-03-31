#$Id: chado.spec.in,v 1.33 2009/04/07 08:10:32 allenday Exp $
%define gmod_root /var/lib/gmod

Summary: Chado, a modular relational schema at the core of the Generic Model Organism Database (GMOD) project
Name: chado
Version: 1.0
Epoch: 0
Release: 1.33.%{distro}
License: GPL
Group: Databases/Bioinformatics
Packager: Allen Day <allenday@ucla.edu>
URL: http://www.gmod.org
BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

BuildRequires: obo-core >= 1.0.1, perl-go-perl >= 0.09
#Dropped 2009/03/25 -day
#BuildRequires: obo-extra

BuildRequires: perl-Class-DBI
BuildRequires: perl-Class-DBI-Pager
BuildRequires: perl-Class-DBI-Pg
BuildRequires: perl-Log-Log4perl
BuildRequires: perl-Template-Toolkit
BuildRequires: perl-Term-ProgressBar
BuildRequires: perl-DBIx-DBStag
BuildRequires: chado-schema = 1.0
BuildRequires: postgresql >= 7.3
BuildRequires: postgresql-AffxSeq = 1.00-3.20050411

Requires: chado-schema = 1.0
Requires: perl-Bio-GMOD
Requires: perl-Class-Accessor
Requires: perl-Class-Accessor-Chained
Requires: perl-Class-DBI
Requires: perl-Class-DBI-ConceptSearch
Requires: perl-Class-DBI-Pager
Requires: perl-Class-DBI-Pg
Requires: perl-DBD-Pg
Requires: perl-DBI
Requires: perl-File-NFSLock
Requires: perl-HTML-Tree
Requires: perl-Log-Log4perl
Requires: perl-Module-Build
Requires: perl-SQL-Translator
Requires: perl-Template-Toolkit
Requires: perl-Term-ProgressBar
Requires: perl-TermReadKey
Requires: perl-Tie-UrlEncoder
Requires: perl-XML-Simple
Requires: perl-bioperl
Requires: postgresql >= 7.3
Requires: postgresql-AffxSeq = 1.00-3.20050411
Requires: postgresql-devel
Requires: postgresql-libs
Requires: postgresql-server

#not sure why i have to hardcode this in...
Provides: perl(Chado::AutoDBI)
#XXX these ones actually doesn't exist.  follow up later 20090326 ajd
Provides: perl(Chado::LoadDBI)
Provides: perl(GMOD::Chado::LoadDBI)

Source0: gmod-%{version}.tar.gz
Source1: ATCC.txt
Patch0: chado-1.0-gmod_root.patch
Patch1: chado-1.0-Bio-GMOD.patch 
Patch2: chado-1.0-Bio-GMOD-DB-Adapter.pm.patch

%description
Chado, a modular relational schema at the core of the Generic Model Organism Database (GMOD) project

%prep
%setup -n gmod-%{version}
%patch0 -p0
%patch1 -p1
%patch2 -p0
#get rid of CXGN* perl modules, which depend on nascent biopackages "cview" package.
#cview doesn't build cleanly, it's a clusterfuck.
find . -iname 'CXGN*' | xargs rm -rf

perl -pi -e "s#etc#%{buildroot}/etc#" install_util/log4perl.conf.PLS
mkdir -p %{buildroot}%{gmod_root}
mkdir -p %{buildroot}/etc

%build
export GMOD_ROOT=%{buildroot}%{gmod_root}

echo "DBHOST=$HOSTNAME"    > build.conf ;
echo "DBUSER=postgres"    >> build.conf ;
echo "LOCAL_TMP=/var/tmp" >> build.conf ;
echo "DBNAME=chado"       >> build.conf ;
echo "DBDRIVER=Pg"        >> build.conf ;
echo "DBPORT=5432"        >> build.conf ;
echo "DBORGANISM="        >> build.conf ;
echo "DBPASS="            >> build.conf ;

echo "Y" | GMOD_ROOT=%{buildroot}%{gmod_root} perl Makefile.PL \
  RECONFIGURE=1 \
  PREFIX=%{buildroot}%{_prefix} \
  INSTALLSITEMAN1DIR=%{buildroot}/usr/share/man/man1 \
  INSTALLSITEMAN3DIR=%{buildroot}/usr/share/man/man3

%install
export GMOD_ROOT=%{buildroot}%{gmod_root}
#make install
%makeinstall ;

#these depend on Datastore::MD5, which i could not find
find %{buildroot} -type f -name cx-enscore2chaos.pl -exec rm -f {} \;
find %{buildroot} -type f -name cx-genbank2chaos.pl -exec rm -f {} \;
find . -type f -name cx-enscore2chaos.pl -exec rm -f {} \;
find . -type f -name cx-genbank2chaos.pl -exec rm -f {} \;

tmp_chado=chado_`date | md5sum | awk '{print $1}' | head -c 4`

sudo /etc/init.d/postgresql start
# on fresh Postgres installs this needs a few secs to startup
sleep 15
sudo su postgres -c "createdb $tmp_chado";
sudo su postgres -c "createlang plpgsql $tmp_chado";
#Creating tables, functions, views, triggers, rules, etc for database
sudo su postgres -c "cat /var/lib/gmod/src/chado/modules/default_schema.sql | psql -U postgres $tmp_chado 2>&1 >/dev/null";#| grep -E '(ERROR|FATAL)' | grep -v 'ERROR:  type'";
#Loading generic data into database
sudo su postgres -c "cat load/etc/initialize.sql | psql -U postgres $tmp_chado 2>&1 >/dev/null";#| grep -E '(ERROR|FATAL)'";
#Load in godb bridge
sudo su postgres -c "cat modules/cv/bridges/godb-bridge.plpgsql | psql -U postgres $tmp_chado 2>&1 >/dev/null";
#Bring in AffxSeq functions
sudo su postgres -c "cat %{_datadir}/doc/postgresql-AffxSeq-1.00/affx-seq-lib-defs.sql | psql -U postgres $tmp_chado 2>&1 >/dev/null";#| grep -E '(ERROR|FATAL)'";

#Load ATCC Cell lines.  ATCC is 3 given the above sequence of commands, but may change!
cat %{SOURCE1} | awk -F '	' '{print 3,"\t",$2,"\t",$3," ",$4}' | perl -ne 's!^3 !3!;print' > ATCC.munged
sudo su postgres -c "cat ATCC.munged | psql -U postgres $tmp_chado -c 'COPY dbxref (db_id,accession,description) FROM stdin' 2>&1 >/dev/null";

#need
obo[12]='gene_ontology_edit.chadoxml';
obo[17]='plant_trait.chadoxml';
obo[18]='po_anatomy.chadoxml';
obo[19]='po_temporal.chadoxml';
obo[23]='so.chadoxml';


#ok
#obo[0]='adult_mouse_anatomy.chadoxml';
#obo[1]='amphibian_anatomy.chadoxml';
#obo[2]='caro.chadoxml';
#obo[3]='cell.chadoxml';
#obo[4]='envo.chadoxml';
#obo[5]='evidence_code.chadoxml';
#obo[6]='fly_anatomy.chadoxml';
#obo[11]='fungal_anatomy.chadoxml';
#obo[14]='infectious_disease.chadoxml';
#obo[15]='mammalian_phenotype.chadoxml';
#obo[16]='mosquito_insecticide_resistance.chadoxml';
#obo[20]='pro.chadoxml';
#obo[21]='psi-mi.chadoxml';
#obo[24]='teleost_anatomy.chadoxml';
#obo[27]='worm_development.chadoxml';
#obo[28]='worm_phenotype.chadoxml';

#unknown
#obo[9]='fly_development.chadoxml';
#obo[10]='fma2_obo.chadoxml';
#obo[13]='human_disease.chadoxml';
#obo[22]='ro.chadoxml';
#obo[25]='tick_anatomy.chadoxml';
#obo[26]='transmission_process.chadoxml';
#obo[29]='yeast_phenotype.chadoxml';

#dead
#obo[]='chebi.chadoxml';
#obo[]='dictyostelium_anatomy.chadoxml';
#obo[]='xenopus_anatomy.chadoxml';
#obo[]='zebrafish_anatomy.chadoxml';

/usr/bin/go2fmt.pl -w xml -e /dev/null ./load/etc/feature_property.obo > ./load/etc/feature_property.oboxml
/usr/bin/go-apply-xslt oboxml_to_chadoxml ./load/etc/feature_property.oboxml > ./load/etc/feature_property.chadoxml
sudo su postgres -c "stag-storenode.pl -d 'dbi:Pg:dbname=$tmp_chado' ./load/etc/feature_property.chadoxml"

for i in ${obo[*]} ; do
  echo "* Loading ontology: '$i'";
  sudo su postgres -c "stag-storenode.pl -d 'dbi:Pg:dbname=$tmp_chado' %{_datadir}/obo*1.0.1/chadoxml/$i" ;
done ;

#for i in ${rel[*]} ; do
#  echo "  * Loading DAG-Edit relationships: $i" ;
#  /usr/bin/go2fmt.pl -p go_ont -w xml -e /dev/null /usr/share/obo/$i | go-apply-xslt oboxml_to_chadoxml - > %{_tmppath}/rel.xml ;
#  if [[ `wc -c /var/tmp/rel.xml | awk '{print $1}'` != 0 ]] ; then
#    sudo su postgres -c "stag-storenode.pl -d 'dbi:Pg:dbname=$tmp_chado' %{_tmppath}/rel.xml" ;
#  fi ;
#done ;

#for i in ${def[*]} ; do
#  echo "  * Loading DAG-Edit definitions: $i" ;
#  /usr/bin/go2fmt.pl -p go_def -w xml -e /dev/null /usr/share/obo/$i | go-apply-xslt oboxml_to_chadoxml - > %{_tmppath}/def.xml ;
#  if [[ `wc -c /var/tmp/def.xml | awk '{print $1}'` != 0 ]] ; then
#    sudo su postgres -c "stag-storenode.pl -d 'dbi:Pg:dbname=$tmp_chado' %{_tmppath}/def.xml" ;
#  fi ;
#done ;

#materialize the godb GO bridge views
sudo su postgres -c " psql $tmp_chado -c 'INSERT INTO godb.go_acc SELECT * FROM godb.v_go_acc'";
sudo su postgres -c " psql $tmp_chado -c 'INSERT INTO godb.dbxref SELECT * FROM godb.v_dbxref'";
sudo su postgres -c " psql $tmp_chado -c 'INSERT INTO godb.db SELECT * FROM godb.v_db'";
sudo su postgres -c " psql $tmp_chado -c 'INSERT INTO godb.term SELECT * FROM godb.v_term'";
#v_term2term is a view on the same table as term2term.  can't do this
#sudo su postgres -c " psql $tmp_chado -c 'INSERT INTO godb.term2term SELECT * FROM godb.v_term2term'";
sudo su postgres -c " psql $tmp_chado -c 'UPDATE godb.term SET is_root = 1 WHERE id IN (SELECT cvterm_id FROM public.cvterm WHERE cvterm_id NOT IN (SELECT DISTINCT subject_id FROM public.cvterm_relationship) AND is_obsolete = 0 AND is_relationshiptype = 0)'";


#repair SO
sudo su postgres -c " psql $tmp_chado -c 'DELETE FROM cvterm_relationship WHERE subject_id = (SELECT cvterm_id FROM cvterm WHERE name = '\''precursor_siRNA'\'') AND object_id = (SELECT cvterm_id FROM cvterm WHERE name = '\''precursor_rasiRNA'\'')' " ;

for i in `sudo su postgres -c "psql $tmp_chado -tAF '	' -c 'SELECT cv_id FROM cv'"` ; do
  sudo su postgres -c "psql $tmp_chado -tAF '	' -c 'SELECT * FROM fill_cvtermpath($i)'";
done ;

#finish materializing the godb GO bridge views, now that cvtermpath is populated
#v_graph_path is a view on the same table as graph_path.  can't do this
#sudo su postgres -c " psql $tmp_chado -c 'INSERT INTO godb.graph_path SELECT * FROM godb.v_graph_path'";

sudo su postgres -c "pg_dump -O $tmp_chado" | gzip > %{name}-%{version}.sql.gz
sudo su postgres -c "dropdb   $tmp_chado"

install -m 444 load/etc/initialize.sql $RPM_BUILD_ROOT%{gmod_root}

[ -x /usr/lib/rpm/brp-compress ] && /usr/lib/rpm/brp-compress
find $RPM_BUILD_ROOT -type f -exec perl -p -i -e "s!$RPM_BUILD_ROOT!!g" {} \;
find $RPM_BUILD_ROOT -type f | sed "s@^$RPM_BUILD_ROOT@%dir @g" >> %{name}-%{version}-%{release}-filelist

%files -f %{name}-%{version}-%{release}-filelist
%defattr(-,root,root)
%doc Changes* INSTALL* LICENSE README* TODO build.conf *.sql.gz

%clean
[ "${RPM_BUILD_ROOT}" != "/" ] && [ -d ${RPM_BUILD_ROOT} ] && rm -rf ${RPM_BUILD_ROOT};

%post
/etc/init.d/postgresql start
# on fresh Postgres installs this needs a few secs to startup
sleep 15
su postgres -c 'dropdb chado || exit 1';

#Creating PostgreSQL database 'chado' as user 'postgres'
su postgres -c 'createdb chado 2>&1' 2>&1 > /dev/null
#Adding plpgsql language to database 'chado'
su postgres -c 'createlang plpgsql chado 2>&1' 2>&1 > /dev/null
#Creating tables, functions, views, triggers, rules, etc for database 'chado'
su postgres -c 'zcat %{_datadir}/doc/%{name}-%{version}/%{name}-%{version}.sql.gz | psql chado 2>&1' 2>&1 > /dev/null
#Granting SELECT to PUBLIC on tables
for i in `su postgres -c "psql %{name} -tAF '      ' -c '\dt'" | awk '{print $2}'` ; do
  su postgres -c "psql %{name} -c 'GRANT SELECT ON $i TO PUBLIC' 2>&1" 2>&1;
done
true ;

%preun
/etc/init.d/postgresql start
# on fresh Postgres installs this needs a few secs to startup
sleep 15
su postgres -c 'dropdb chado';
true;

%changelog
* Mon Oct  3 2005 Brian O'Connor <boconnor@ucla.edu> 0.003-11
- updates to the modules/default_nofuncs.sql file so they will build in SQLFairy (for Turnkey/GmodWeb)
* Mon Jul 11 2005 Allen Day <allenday@ucla.edu> 0.003-10
- godb.graph_path now populated.
* Fri Jul  8 2005 Allen Day <allenday@ucla.edu> 0.003-9
- Updated to real 0.003 release
* Tue Jul  5 2005 Allen Day <allenday@ucla.edu> 0.003-8
- Dropped %preun and %post warning silliness
- Moved perl-go-perl and obo-* to BuildRequires, where they belong
- Bumped obo-core prereq to 1.0.0-7 to pull in new mouse ontology
- Added mpath_obo.ontology to default schema
- Added ATCC cell lines to db/dbxref tables
- Added godb bridge so chado can be used by gene ontology tools like go-perl and go-db-perl
- Populated godb bridge materialized views
- Added Affymetrix 10K, 100K, and 500K mapping arrays to arraydesign.
- Removed SOFA ontology from load.  GFF3 was the only thing requiring it, and GFF3 now accepts full SO
- Added contact module to database
* Tue Apr 26 2005 Allen Day <allenday@ucla.edu> 0.003-6
- Updated chado tarball to CVS HEAD.  This contains new cvterm
  graph traversal code, as well as a more uniform system for
  naming algorithms, tables, and arraydesigns for affy data.
* Wed Apr 13 2005 Allen Day <allenday@ucla.edu> 0.003-5
- Updated chado tarball to CVS HEAD
- Populated cvtermpath as part of build
- Granted select on all tables to public
* Tue Mar 22 2005 Allen Day <allenday@ucla.edu> 0.003-4
- moved to noarch build
* Tue Mar 8 2005 Allen Day <allenday@ucla.edu> 0.003-1
- New specfile.
%changelog
