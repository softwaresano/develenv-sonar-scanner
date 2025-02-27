%define sonar_version %(grep -A1 "<artifactId>sonar-scanner-cli</artifactId>" pom.xml|tail -1|grep -Po --color=no "(?<=<version>).*(?=<)")
Name:        sonar-scanner
Version:     %{versionModule}
Release:     %{sonar_version}.r%{releaseModule}
Epoch:       2
Summary:     Sonar scanner
Group:       develenv
License:     http://creativecommons.org/licenses/by/3.0/
Packager:    softwaresano.com
URL:         https://www.sonarqube.org/
BuildArch:   x86_64
BuildRoot:   %{_topdir}/BUILDROOT
Requires:    java-17-openjdk
AutoReqProv: no

Vendor:      softwaresano

%define package_name sonar-scanner
%define target_dir /
%define sonar_home /opt/ss/develenv/platform/%{package_name}
%define sonar_home_logs /var/log/sonar
%define sonar_home_data /var/lib/sonar

%description
Sonar is the central place to manage code quality, offering visual reporting on
and across projects and enabling to replay the past to follow metrics evolution

# ------------------------------------------------------------------------------
# CLEAN
# ------------------------------------------------------------------------------
%clean
rm -rf $RPM_BUILD_ROOT

# ------------------------------------------------------------------------------
# INSTALL
# ------------------------------------------------------------------------------
%install
SONAR_VERSION=%{sonar_version}
%{__mkdir_p} $RPM_BUILD_ROOT/%{sonar_home}

cd $RPM_BUILD_ROOT
mkdir build
cd build
curl -L -k -O https://binaries.sonarsource.com/Distribution/sonar-scanner-cli/sonar-scanner-cli-${SONAR_VERSION}.zip
unzip sonar-scanner-cli-${SONAR_VERSION}.zip
cd sonar-scanner-${SONAR_VERSION}
sed -i 's#exec "$java_cmd" #exec "$java_cmd" --add-opens java.base/sun.nio.ch=ALL-UNNAMED --add-opens java.base/java.io=ALL-UNNAMED #' bin/sonar-scanner
cd ../../
mv build/sonar-scanner-${SONAR_VERSION}/* $RPM_BUILD_ROOT/%{sonar_home}/
rm -rf build
rsync -arv %{_sourcedir}/* $RPM_BUILD_ROOT/%{target_dir}
mkdir -p $RPM_BUILD_ROOT/usr/bin
ln -sf %{sonar_home}/bin/sonar-scanner $RPM_BUILD_ROOT/usr/bin/sonar-scanner
ln -sf %{sonar_home}/bin/sonar-scanner-debug $RPM_BUILD_ROOT/usr/bin/sonar-scanner-debug
ln -sf %{sonar_home}/bin/sonar-copy-project.sh $RPM_BUILD_ROOT/usr/bin/sonar-copy-project.sh
mkdir -p $RPM_BUILD_ROOT/etc
ln -sf %{sonar_home}/conf $RPM_BUILD_ROOT/etc/%{package_name}

%files
%defattr(-,root,root,-)
%{sonar_home}/*
/usr/bin/*
/etc/%{package_name}
%config %{sonar_home}/conf/*

%doc ../../../../README.md
