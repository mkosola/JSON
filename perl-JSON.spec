# This spec file is from Fedora and adapted to Mer
Name:           perl-JSON
Summary:        Parse and convert to JSON (JavaScript Object Notation)
Version:        2.55
Release:        1
License:        GPL+ or Artistic
Source0:        JSON-%{version}.tar.gz 
URL:            http://search.cpan.org/dist/JSON/
Requires:       perl(:MODULE_COMPAT_%(eval "`%{__perl} -V:version`"; echo $version))
BuildArch:      noarch

BuildRequires:  perl(base)
BuildRequires:  perl(Carp)
BuildRequires:  perl(CGI)
BuildRequires:  perl(constant)
BuildRequires:  perl(Data::Dumper)
BuildRequires:  perl(Encode)
BuildRequires:  perl(Exporter)
BuildRequires:  perl(ExtUtils::MakeMaker)
BuildRequires:  perl(File::Spec)
BuildRequires:  perl(Math::BigFloat)
BuildRequires:  perl(Math::BigInt)
BuildRequires:  perl(lib)
BuildRequires:  perl(Scalar::Util)


%{?perl_default_filter:
%filter_from_provides /^perl(JSON::\(Backend::PP\|backportPP::Boolean\|Boolean\|PP\|PP::IncrParser\))/d
%filter_from_requires /^perl(JSON::backportPP)$/d
%perl_default_filter}
%global __provides_exclude %{?__provides_exclude:%__provides_exclude|}perl\\(JSON::(Backend::PP|backportPP::Boolean|Boolean|PP|PP::IncrParser)\\)
%global __requires_exclude %{?__requires_exclude:%__requires_exclude|}perl\\(JSON::backportPP\\)

%description
This module converts between JSON (JavaScript Object Notation) and Perl
data structure into each other. For JSON, see http://www.crockford.com/JSON/.

%prep
# Adjusting %%setup since git-pkg unpacks to src/
# %%setup -q -n JSON-%%{version}
%setup -q -n src

# make rpmlint happy...
find .  -type f -exec chmod -c -x {} +
find t/ -type f -exec perl -pi -e 's|^#! perl|#!%{__perl}|' {} +
sed -i 's/\r//' README t/*

%build
%{__perl} Makefile.PL INSTALLDIRS=vendor
make %{?_smp_mflags}

%install
make pure_install DESTDIR=%{buildroot}

find %{buildroot} -type f -name .packlist -exec rm -f {} +
find %{buildroot} -depth -type d -exec rmdir {} 2>/dev/null \;

%{_fixperms} %{buildroot}/*

%files
%doc Changes README
%{perl_vendorlib}/*
%{_mandir}/man3/*
