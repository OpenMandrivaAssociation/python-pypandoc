# Created by pyp2rpm-2.0.0

Name:           python-pypandoc
Version:        1.17
Release:        1
Summary:        Thin wrapper for pandoc

License:        MIT
Group:        Development/Python
URL:            https://github.com/bebraw/pypandoc
Source0:        https://files.pythonhosted.org/packages/source/p/pypandoc/pypandoc-%{version}.tar.gz
BuildArch:      noarch

# for tests
#BuildRequires:  pandoc
#BuildRequires:  pandoc-citeproc
BuildRequires:  texlive-scheme-basic
BuildRequires:  texlive-collection-fontsrecommended
#BuildRequires:  tex(ecrm1000.tfm)

BuildRequires:	python%{pyver}dist(pip)
BuildRequires:	python%{pyver}dist(hatchling)
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

%build
%py_build

%install
%py_install

%global _docdir_fmt %{name}

%files
%license LICENSE
%doc README.md
%{_bindir}/pypandoc
%{python_sitelib}/pypandoc
%{python_sitelib}/pypandoc-%{version}.dist-info
