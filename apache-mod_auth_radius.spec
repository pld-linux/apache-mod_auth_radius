%define 	apxs		%{_sbindir}/apxs
Summary:	RADIUS authentication module for the Apache 2 webserver
Summary(pl.UTF-8):	Moduł uwierzytelniający RADIUS dla serwera WWW Apache 2
Name:		apache-mod_auth_radius
Version:	1.5.8
Release:	1
License:	Apache-like
Group:		Networking/Daemons/HTTP
Source0:	ftp://ftp.freeradius.org/pub/freeradius/mod_auth_radius-%{version}.tar
# Source0-md5:	87d8ef049736254cc09f8b34667f0e59
Patch0:		%{name}-apache.patch
Patch1:		%{name}-conf.patch
URL:		http://www.freeradius.org/
BuildRequires:	%{apxs}
BuildRequires:	apache-devel >= 2.4
BuildRequires:	rpmbuild(macros) >= 1.268
Requires:	apache(modules-api) = %apache_modules_api
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_pkglibdir	%(%{apxs} -q LIBEXECDIR 2>/dev/null)
%define		_sysconfdir	%(%{apxs} -q SYSCONFDIR 2>/dev/null)/conf.d

%description
This is the Apache RADIUS authentication module. It allows any Apache
web-server to become a RADIUS client for authentication and accounting
requests. You will, however, need to supply your own RADIUS server to
perform the actual authentication.

%description -l pl.UTF-8
Ten pakiet zawiera moduł uwierzytelniający RADIUS dla serwera WWW
Apache. Pozwala dowolnemu serwerowi Apache stać się klientem RADIUS na
potrzeby żądań uwierzytelniania i rozliczania. Aby wykonywać właściwe
uwierzytelnianie potrzebny jest własny serwer RADIUS.

%prep
%setup -q -n mod_auth_radius-%{version}
%patch -P0 -p1
%patch -P1 -p1

%build
%{apxs} -c -o mod_auth_radius.so mod_auth_radius-2.0.c

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_pkglibdir},%{_sysconfdir}}

install -p .libs/mod_auth_radius.so $RPM_BUILD_ROOT%{_pkglibdir}
cp -p httpd.conf $RPM_BUILD_ROOT%{_sysconfdir}/90_mod_auth_radius.conf

%clean
rm -rf $RPM_BUILD_ROOT

%post
%service -q httpd restart

%postun
if [ "$1" = "0" ]; then
	%service -q httpd restart
fi

%files
%defattr(644,root,root,755)
%doc README htaccess index.html
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/90_mod_auth_radius.conf
%attr(755,root,root) %{_pkglibdir}/mod_auth_radius.so
