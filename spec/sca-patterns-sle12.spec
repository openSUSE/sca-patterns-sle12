# spec file for package sca-patterns-sle12
#
# Copyright (C) 2014 SUSE LLC
#
# This file and all modifications and additions to the pristine
# package are under the same license as the package itself.
#

# norootforbuild
# neededforbuild

%define sca_common sca
%define patdirbase /usr/lib/%{sca_common}
%define patdir %{patdirbase}/patterns
%define patuser root
%define patgrp root
%define mode 544
%define category SLE

Name:         sca-patterns-sle12
Summary:      Supportconfig Analysis Patterns for SLE12
URL:          https://bitbucket.org/g23guy/sca-patterns-sle12
Group:        Documentation/SuSE
License:      GPL-2.0
Autoreqprov:  on
Version:      1.0
Release:      9
Source:       %{name}-%{version}.tar.gz
BuildRoot:    %{_tmppath}/%{name}-%{version}
Buildarch:    noarch
Requires:     sca-patterns-base
%description
Supportconfig Analysis (SCA) appliance patterns to identify known
issues relating to all versions of SLES/SLED 12

Authors:
--------
    Jason Record <jrecord@suse.com>

%prep
%setup -q

%build

%install
pwd;ls -la
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT/%{patdir}/%{category}
install -d $RPM_BUILD_ROOT/%{patdir}/%{category}/sle12all
install -d $RPM_BUILD_ROOT/usr/share/doc/packages/%{sca_common}
install -m 444 patterns/COPYING.GPLv2 $RPM_BUILD_ROOT/usr/share/doc/packages/%{sca_common}
install -m %{mode} patterns/%{category}/sle12all/* $RPM_BUILD_ROOT/%{patdir}/%{category}/sle12all

%files
%defattr(-,%{patuser},%{patgrp})
%dir %{patdirbase}
%dir %{patdir}
%dir %{patdir}/%{category}
%dir %{patdir}/%{category}/sle12all
%dir /usr/share/doc/packages/%{sca_common}
%doc %attr(-,root,root) /usr/share/doc/packages/%{sca_common}/*
%attr(%{mode},%{patuser},%{patgrp}) %{patdir}/%{category}/sle12all/*

%clean
rm -rf $RPM_BUILD_ROOT

%changelog

