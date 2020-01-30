Name: 		git-minimal
Version: 	2.25.0
Release: 	1
Summary:  	Core git tools, cut-down version
License: 	GPLv2
URL: 		https://git.sailfishos.org/mer-core/git
Source: 	%{name}-%{version}.tar.bz2

Patch1:		0001-lang-do-not-build-install-unused-stuff.patch
BuildRequires:	zlib-devel >= 1.2, openssl-devel, curl-devel, expat-devel, gettext

Requires:	zlib >= 1.2, openssh-clients, expat
Provides:	git-core = %{version}-%{release}
Obsoletes:	git-core <= 1.5.4.2
Provides:	git = %{version}-%{release}
Conflicts:	git-all
Provides:	git-p4 = %{version}-%{release}
Obsoletes:	git-p4

%description
Git is a fast, scalable, distributed revision control system with an
unusually rich command set that provides both high-level operations
and full access to internals.

The git-minimal is the cut-down version of core tools prepared for the
Mer. It does not depend on tools and libraries not included in Mer
(perl, python, rsync...)

%define path_settings ETC_GITCONFIG=/etc/gitconfig prefix=%{_prefix} mandir=%{_mandir} htmldir=%{_docdir}/%{name}-%{version} gitexecdir=%{_bindir}


%define extra_make_flags NO_RSYNC=1 NO_PERL=1 NO_TCLTK=1 NO_PYTHON=1 DEFAULT_PAGER=more

%prep
%autosetup -p1 -n %%{name}-%%{version}/git

%build
make %{extra_make_flags} %{_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" \
     %{path_settings} \
     all

%install
rm -rf %{buildroot}
make  %{extra_make_flags} %{_smp_mflags} CFLAGS="$RPM_OPT_FLAGS" DESTDIR=%{buildroot} \
     %{path_settings} \
     INSTALLDIRS=vendor install

find %{buildroot} -type f -name .packlist -exec rm -f {} ';'
find %{buildroot} -type f -name '*.bs' -empty -exec rm -f {} ';'
find %{buildroot} -type f -name perllocal.pod -exec rm -f {} ';'

(find %{buildroot}%{_bindir} -type f | grep -vE "archimport|svn|cvs|email|gitk|git-gui|git-citool" | sed -e s@^%{buildroot}@@) > bin-files
rm -rf %{buildroot}%{_mandir}
rm -rf %{buildroot}%{_datadir}/locale
# don't need on minimal installation and at the moment fsmonitor-watchman.sample would pull in perl
rm %{buildroot}%{_datadir}/git-core/templates/hooks/*.sample

mkdir -p %{buildroot}%{_sysconfdir}/bash_completion.d
install -m 644 -T contrib/completion/git-completion.bash %{buildroot}%{_sysconfdir}/bash_completion.d/git

%files -f bin-files
%defattr(-,root,root)
%{_datadir}/git-core/
%dir %{_bindir}/mergetools
%doc README.md 
%license COPYING
%{_sysconfdir}/bash_completion.d
