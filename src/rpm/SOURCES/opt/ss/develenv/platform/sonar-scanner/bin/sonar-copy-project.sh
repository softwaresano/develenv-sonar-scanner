#!/bin/bash -ex
build_url="${1:?}"
mkdir -p sonar
rm -Rf sonar/*
cd sonar
curl -fO "${build_url:?}/artifact/sonar-project.properties"
repo=$(grep -Po '(?<=sonar.links.scm=git@github.com:Telefonica/).*(?=\.git)' sonar-project.properties)
git clone "git@github.com:Telefonica/${repo:?}.git"
cd "${repo:?}"
curl -fO "${build_url:?}"/artifact/target/reports/*zip*/reports.zip
mkdir -p target/
cd target
unzip ../reports.zip
cd ..
cp -vf ../sonar-project.properties .
if [[ -f target/reports/rake/coverage.xml ]]; then
  jenkins_workspace=$(grep -Po '(?<=<source>).*(?=<)' target/reports/rake/coverage.xml)
  sed -i "s#${jenkins_workspace}#${PWD}#g" target/reports/rake/coverage.xml
  sed -i "s#${jenkins_workspace}#${PWD}#g" target/reports/rake/.resultset.json
fi
mkdir -p target/logs
sonar-scanner -Dsonar.host.url=http://cdn-metrics-center.cdn.hi.inet 2>&1 | tee target/logs/sonar.log
