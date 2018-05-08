#!/bin/bash -e

cd /clj

TARGET=target/clombda

rm -rf ${TARGET}
mkdir -p ${TARGET}/package

lein uberjar

native-image -jar ${TARGET}/uberjar/*-standalone.jar\
             -H:Name="${TARGET}/package/clj-native"\
             -H:+ReportUnsupportedElementsAtRuntime

cp /lambda_function.py ${TARGET}/package/

cd ${TARGET}/package/
zip ../package.zip *

echo "built ${TARGET}/package.zip"

