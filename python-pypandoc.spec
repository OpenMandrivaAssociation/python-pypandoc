# Created by pyp2rpm-2.0.0

Name:           python-pypandoc
Version:        1.5
Release:        1
Summary:        Thin wrapper for pandoc

License:        MIT
URL:            https://github.com/bebraw/pypandoc
Source0:        https://files.pythonhosted.org/packages/source/p/pypandoc/pypandoc-%{version}.tar.gz
BuildArch:      noarch

# for tests
#BuildRequires:  pandoc
#BuildRequires:  pandoc-citeproc
BuildRequires:  texlive-scheme-basic
BuildRequires:  texlive-collection-fontsrecommended
#BuildRequires:  tex(ecrm1000.tfm)

BuildRequires:  python-devel
BuildRequires:  python-setuptools
#Requires:       pandoc
#Requires:       pandoc-citeproc
Recommends:     texlive-scheme-basic
Recommends:     texlive-collection-fontsrecommended
%{?python_provide:%python_provide python-pypandoc}

%description
pypandoc provides a thin Python wrapper for pandoc, a universal \
document converter, allowing parsing and conversion of          \
pandoc-formatted text.


%prep
%autosetup -n pypandoc-%{version}

# Upstream pins pip and wheel in install_requires, but they're not needed at runtime
# https://github.com/bebraw/pypandoc/commit/c91c6d6fd23fb133a3676bce7af2a710ae7990d8
sed -Ei -e "s/(, )?'pip>=[^']+'//" -e "s/(, )?'wheel>=[^']+'//" setup.py

%build
%py_build

%install
%py_install

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

#{__python} tests.py

%global _docdir_fmt %{name}

%files
%license LICENSE
%doc README.md examples/
%{python_sitelib}/pypandoc
%{python_sitelib}/pypandoc-%{version}-py?.?.egg-info
