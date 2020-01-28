# Created by pyp2rpm-2.0.0

Name:           python-pypandoc
Version:        1.4
Release:        11%{?dist}
Summary:        Thin wrapper for pandoc

License:        MIT
URL:            https://github.com/bebraw/pypandoc
Source0:        https://files.pythonhosted.org/packages/source/p/pypandoc/pypandoc-%{version}.tar.gz
BuildArch:      noarch

Patch0001:	0001-tests-gracefuly-handle-network-access-failure-in-tes.patch

# for tests
BuildRequires:  pandoc
BuildRequires:  pandoc-citeproc
BuildRequires:  texlive-scheme-basic
BuildRequires:  texlive-collection-fontsrecommended
BuildRequires:  tex(ecrm1000.tfm)

BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools

%global _description \
pypandoc provides a thin Python wrapper for pandoc, a universal \
document converter, allowing parsing and conversion of          \
pandoc-formatted text.

%description %_description

%package -n     python%{python3_pkgversion}-pypandoc
Summary:        %{summary}
%{?python_provide:%python_provide python%{python3_pkgversion}-pypandoc}
Requires:       pandoc
Requires:       pandoc-citeproc
%if 0%{?fedora}
Recommends:     texlive-scheme-basic
Recommends:     texlive-collection-fontsrecommended
%endif

%description -n python%{python3_pkgversion}-pypandoc  %_description

%prep
%autosetup -n pypandoc-%{version}

# Upstream pins pip and wheel in install_requires, but they're not needed at runtime
# https://github.com/bebraw/pypandoc/commit/c91c6d6fd23fb133a3676bce7af2a710ae7990d8
sed -Ei -e "s/(, )?'pip>=[^']+'//" -e "s/(, )?'wheel>=[^']+'//" setup.py

%build
%py3_build

%install
%py3_install

%check
# Old pandoc on EL7, no docx, no twiki
%if 0%{?rhel} && 0%{?rhel} <= 7
sed -i -e '/twiki/d' tests.py
%endif

# Disable test that requires network
sed -i -r 's/test_basic_conversion_from_http_url/_disabled_\0/' tests.py

# Disable tests where the rendering in pandoc-2 is different
# https://github.com/bebraw/pypandoc/issues/149
sed -i -r 's/\b(test_convert_with_custom_writer|test_basic_conversion_from_file|test_basic_conversion_from_file_with_format|test_basic_conversion_from_string|test_basic_conversion_to_file|test_conversion_from_markdown_with_extensions|test_conversion_from_non_plain_text_file|test_get_pandoc_version)\b/_disabled_\0/' tests.py

%{__python3} tests.py

%global _docdir_fmt %{name}

%files -n python%{python3_pkgversion}-pypandoc
%license LICENSE
%doc README.md examples/
%{python3_sitelib}/pypandoc
%{python3_sitelib}/pypandoc-%{version}-py?.?.egg-info

%changelog
* Thu Nov 14 2019 Miro Hrončok <mhroncok@redhat.com> - 1.4-11
- Subpackage python2-pypandoc has been removed
  See https://fedoraproject.org/wiki/Changes/Mass_Python_2_Package_Removal

* Mon Sep 02 2019 Miro Hrončok <mhroncok@redhat.com> - 1.4-10
- Drop unneeded runtime dependency on pip and wheel

* Mon Aug 19 2019 Miro Hrončok <mhroncok@redhat.com> - 1.4-9
- Rebuilt for Python 3.8

* Fri Jul 26 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-8
- Rebuilt for https://fedoraproject.org/wiki/Fedora_31_Mass_Rebuild

* Sat Feb 02 2019 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-7
- Rebuilt for https://fedoraproject.org/wiki/Fedora_30_Mass_Rebuild

* Sun Nov 18 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.4-6
- Drop explicit locale setting
  See https://fedoraproject.org/wiki/Changes/Remove_glibc-langpacks-all_from_buildroot

* Sat Jul 14 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.4-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_29_Mass_Rebuild

* Tue Jun 19 2018 Miro Hrončok <mhroncok@redhat.com> - 1.4-4
- Rebuilt for Python 3.7

* Mon Mar 26 2018 Iryna Shcherbina <ishcherb@redhat.com> - 1.4-3
- Update Python 2 dependency declarations to new packaging standards
  (See https://fedoraproject.org/wiki/FinalizingFedoraSwitchtoPython3)

* Thu Mar 15 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.4-2
- Disable tests that require network and/or are incompatible with pandoc-2 (#1556255)

* Wed Feb 14 2018 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.4-1
- Update to latest version

* Fri Feb 09 2018 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Thu Jul 27 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_27_Mass_Rebuild

* Sat Feb 11 2017 Fedora Release Engineering <releng@fedoraproject.org> - 1.3.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_26_Mass_Rebuild

* Mon Dec 19 2016 Miro Hrončok <mhroncok@redhat.com> - 1.3.3-3
- Rebuild for Python 3.6

* Tue Nov 29 2016 Orion Poplawski <orion@cora.nwra.com> - 1.3.3-2
- Also exclude test_convert_with_custom_writer with old pandoc

* Mon Nov 28 2016 Orion Poplawski <orion@cora.nwra.com> - 1.3.3-1
- Update to 1.3.3

* Mon Nov 28 2016 Orion Poplawski <orion@cora.nwra.com> - 1.1.3-3
- Enable EPEL builds

* Tue Jul 19 2016 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-2
- https://fedoraproject.org/wiki/Changes/Automatic_Provides_for_Python_RPM_Packages

* Thu Apr 07 2016 Zbigniew Jędrzejewski-Szmek <zbyszek@in.waw.pl> - 1.1.3-1
- Initial package.
