Summary:	Davenport Group DocBook DTD for technical documentation
Summary(pl):	DocBook DTD przeznaczone do pisania dokumentacji technicznej
%define ver	4.1.2
%define sver	412
Name:		docbook-dtd%{sver}-xml
Version:	1.0
Release:	5
Vendor:		OASIS
License:	Free
Group:		Applications/Publishing/XML
URL:		http://www.oasis-open.org/docbook/
Source0:	http://www.oasis-open.org/docbook/xml/%{ver}/docbkx%{sver}.zip
BuildRequires:	unzip
Requires:	libxml2-progs >= 2.4.17-6
Provides:	%{name}-xmlcatalog
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
%setup -q -c
chmod -R a+rX *

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_datadir}/sgml/docbook/xml-dtd-%{ver}

install *.{cat,dtd,mod} $RPM_BUILD_ROOT%{_datadir}/sgml/docbook/xml-dtd-%{ver}
cp -a ent $RPM_BUILD_ROOT%{_datadir}/sgml/docbook/xml-dtd-%{ver}

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_bindir}/xmlcatalog --noout --add public \
	"-//OASIS//DTD DocBook XML V%{ver}//EN" \
	http://www.oasis-open.org/docbook/xml/%{ver}/docbookx.dtd \
	/etc/xml/catalog
%{_bindir}/xmlcatalog --noout --add rewriteSystem \
	http://www.oasis-open.org/docbook/xml/%{ver}/docbookx.dtd \
	file://%{_datadir}/sgml/docbook/xml-dtd-%{ver}/docbookx.dtd \
	/etc/xml/catalog

%postun
%{_bindir}/xmlcatalog --noout --del \
	"-//OASIS//DTD DocBook XML V%{ver}//EN" \
	/etc/xml/catalog

%files
%defattr(644,root,root,755)
%doc *.txt
%{_datadir}/sgml/docbook/*
