# TODO:
# - use XML ISO entities from sgml-common
Summary:	Davenport Group DocBook DTD for technical documentation
Summary(pl):	DocBook DTD przeznaczone do pisania dokumentacji technicznej
%define ver	4.1.2
%define sver	412
Name:		docbook-dtd%{sver}-xml
Version:	1.0
Release:	6
Vendor:		OASIS
License:	Free
Group:		Applications/Publishing/XML
URL:		http://www.oasis-open.org/docbook/
Source0:	http://www.oasis-open.org/docbook/xml/%{ver}/docbkx%{sver}.zip
BuildRequires:	unzip
Requires(post,preun):	/usr/bin/xmlcatalog
Requires:	libxml2-progs >= 2.4.17-6
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		dtdpath	%{_datadir}/sgml/docbook/xml-dtd-%{ver}

%description
OASIS DocBook DTD for technical documentation.

%description -l pl
DocBook DTD jest zestawem definicji dokumentów przeznaczonych do
tworzenia dokumentacji programistycznej. Stosowany jest do pisania
podrêczników systemowych, instrukcji technicznych jak i wielu innych
ciekawych rzeczy.

%prep
%setup -q -c
chmod -R a+rX *

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{dtdpath}

install *.{cat,dtd,mod} $RPM_BUILD_ROOT%{dtdpath}
cp -a ent $RPM_BUILD_ROOT%{dtdpath}

# associate default declaration for xml
# and map system identifier for xml because opensp seems to misinterpret
# xml-style system identifiers (file://...)
cat <<EOF >>$RPM_BUILD_ROOT%{_datadir}/sgml/docbook/xml-dtd-%{ver}/catalog
OVERRIDE YES
  -- default decl --
SGMLDECL "../../xml.dcl"
  -- hacks for opensp --
SYSTEM "file://%{_datadir}/sgml/docbook/xml-dtd-%{ver}/docbookx.dtd" "%{_datadir}/sgml/docbook/xml-dtd-%{ver}/docbookx.dtd"
SYSTEM "http://www.oasis-open.org/docbook/xml/%{ver}/docbookx.dtd"                  "%{_datadir}/sgml/docbook/xml-dtd-%{ver}/docbookx.dtd"

xmlcatalog --noout --create $RPM_BUILD_ROOT%{dtdpath}/catalog.xml

xmlcatalog --noout --add rewriteSystem \
	http://www.oasis-open.org/docbook/xml/%{ver}/ \
	file://%{dtdpath}/ \
	$RPM_BUILD_ROOT%{dtdpath}/catalog.xml

grep PUBLIC docbook.cat|grep -v ISO |sed 's/^/xmlcatalog --noout --add /;s/PUBLIC/public/;s=$= '$RPM_BUILD_ROOT'/%{dtdpath}/catalog.xml=' |sh

%clean
rm -rf $RPM_BUILD_ROOT

%post
if ! grep -q /etc/sgml/xml-docbook-%{ver}.cat /etc/sgml/catalog ; then
	/usr/bin/install-catalog --add /etc/sgml/xml-docbook-%{ver}.cat %{dtdpath}/docbook.cat > /dev/null
fi
if ! grep -q %{dtdpath}/catalog.xml /etc/xml/catalog ; then
	/usr/bin/xmlcatalog --noout --add nextCatalog "" %{dtdpath}/catalog.xml /etc/xml/catalog
fi

%preun
if [ "$1" = "0" ] ; then
	/usr/bin/install-catalog --remove /etc/sgml/xml-docbook-%{ver}.cat %{dtdpath}/docbook.cat > /dev/null
	/usr/bin/xmlcatalog --noout --del %{dtdpath}/catalog.xml /etc/xml/catalog
fi

%files
%defattr(644,root,root,755)
%doc *.txt ChangeLog
%{dtdpath}
