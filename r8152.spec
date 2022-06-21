# Conditional build:
%bcond_with	verbose		# verbose build (V=1)

# nothing to be placed to debuginfo package
%define		_enable_debug_packages	0

%define		rel	1
%define		pname	r8152
Summary:	A kernel module for Realtek RTL8152/RTL8153 Based USB Ethernet Adapters
Name:		%{pname}%{_alt_kernel}
Version:	2.16.1
Release:	%{rel}%{?_pld_builder:@%{_kernel_ver_str}}
License:	GPL v2
Group:		Base/Kernel
URL:		http://www.realtek.com.tw/
# Check for new versions at
# https://www.realtek.com/en/component/zoo/category/network-interface-controllers-10-100-1000m-gigabit-ethernet-usb-3-0-software
# unfortunately this download is not DF-friendly.
Source0:	%{pname}-%{version}.tar.bz2
# Source0-md5:	66ec60f9b775cfe475ec589e6378d7d1
BuildRequires:	rpmbuild(macros) >= 1.701
%{expand:%buildrequires_kernel kernel%%{_alt_kernel}-module-build}
BuildRoot:	%{tmpdir}/%{pname}-%{version}-root-%(id -u -n)

%description
A kernel module for Realtek RTL8152/RTL8153 Based USB Ethernet
Adapters.

%define	kernel_pkg()\
%package -n kernel%{_alt_kernel}-net-r8152\
Summary:	A kernel module for Realtek RTL8152/RTL8153 Based USB Ethernet Adapters\
Release:	%{rel}@%{_kernel_ver_str}\
Group:		Base/Kernel\
Requires(post,postun):	/sbin/depmod\
%requires_releq_kernel\
Requires(postun):	%releq_kernel\
\
%description -n kernel%{_alt_kernel}-net-r8152\
A kernel module for Realtek RTL8152/RTL8153 Based USB Ethernet\
Adapters.\
\
%files -n kernel%{_alt_kernel}-net-r8152\
%defattr(644,root,root,755)\
%doc ReadMe.txt\
%config(noreplace) %verify(not md5 mtime size) /etc/depmod.d/%{_kernel_ver}/r8152.conf\
/lib/modules/%{_kernel_ver}/misc/*.ko*\
\
%post	-n kernel%{_alt_kernel}-net-r8152\
%depmod %{_kernel_ver}\
\
%postun	-n kernel%{_alt_kernel}-net-r8152\
%depmod %{_kernel_ver}\
%{nil}

%define build_kernel_pkg()\
%build_kernel_modules -m r8152 KERNELRELEASE=%{_kernel_ver}\
%install_kernel_modules -D installed -m r8152 -d misc\
%{nil}

%define install_kernel_pkg()\
install -d installed/etc/depmod.d/%{_kernel_ver}\
echo override r8152 %{_kernel_ver} misc > installed/etc/depmod.d/%{_kernel_ver}/r8152.conf\
%{nil}

%{expand:%create_kernel_packages}

%prep
%setup -q -n %{pname}-%{version}

%build
%{expand:%build_kernel_packages}
%{expand:%install_kernel_packages}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT

cp -a installed/* $RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT
