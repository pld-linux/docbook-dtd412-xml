Summary:	Davenport Group DocBook DTD for technical documentation
Summary(pl):	DocBook DTD przeznaczone do pisania dokumentacji technicznej 
%define ver	4.1.2
%define sver	412
Name:		docbook-dtd%{sver}-xml
Version:	1.0
Release:	3
Vendor:		OASIS
License:	Free
Group:		Applications/Publishing/XML
URL:		http://www.oasis-open.org/docbook/
Source0:	http://www.oasis-open.org/docbook/xml/%{ver}/docbkx%{sver}.zip
BuildRequires:	unzip
Requires:	sgml-common >= 0.5
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OASIS DocBook DTD for technical documentation.

%description -l pl 
DocBook DTD jest zestawem definicji dokumentów przeznaczonych do
tworzenia dokumentacji programistycznej. Stosowany jest do pisania
podrêczników systemowych, instrukcji technicznych jak i wielu innych
ciekawych rzeczy.

%prep
%setup -q -c -T 
unzip -qa %{SOURCE0}
chmod -R a+rX *

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/sgml/docbook/xml-dtd-%{ver}

install *.dtd *.mod $RPM_BUILD_ROOT%{_datadir}/sgml/docbook/xml-dtd-%{ver}
install *.ent $RPM_BUILD_ROOT%{_datadir}/sgml/docbook/xml-dtd-%{ver} || :
cp -a ent $RPM_BUILD_ROOT%{_datadir}/sgml/docbook/xml-dtd-%{ver}

# associate default declaration for xml
# and map system identifier for xml because opensp seems to misinterpret
# xml-style system identifiers (file://...)
cat <<EOF >>$RPM_BUILD_ROOT%{_datadir}/sgml/docbook/xml-dtd-%{ver}/catalog

  -- default decl --
DTDDECL "-//OASIS//DTD DocBook XML V%{ver}//EN" "../../xml.dcl"
  -- hacks for opensp --
SYSTEM "file://%{_datadir}/sgml/docbook/xml-dtd-%{ver}/docbookx.dtd" "%{_datadir}/sgml/docbook/xml-dtd-%{ver}/docbookx.dtd"
SYSTEM "http://www.oasis-open.org/docbook/xml/%{ver}/docbookx.dtd"                  "%{_datadir}/sgml/docbook/xml-dtd-%{ver}/docbookx.dtd"

EOF

# install catalog (but filter out ISO entities)
#grep -v 'ISO ' docbook.cat >> $RPM_BUILD_ROOT%{_datadir}/sgml/docbook/xml-dtd-%{ver}/catalog
cat docbook.cat >> $RPM_BUILD_ROOT%{_datadir}/sgml/docbook/xml-dtd-%{ver}/catalog


gzip -9nf *.txt
[ ! -f ChangeLog ] || gzip -9nf ChangeLog

%clean
rm -rf $RPM_BUILD_ROOT

%post
# Update the centralized catalog corresponding to this version of the DTD
/usr/bin/install-catalog --add /etc/sgml/xml-docbook-%{ver}.cat /usr/share/sgml/docbook/xml-dtd-%{ver}/catalog > /dev/null

%postun
/usr/bin/install-catalog --remove /etc/sgml/xml-docbook-%{ver}.cat /usr/share/sgml/docbook/xml-dtd-%{ver}/catalog > /dev/null

%files
%defattr(644,root,root,755)
%doc *.gz 
%{_datadir}/sgml/docbook/*
