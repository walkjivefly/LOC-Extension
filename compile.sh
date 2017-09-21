#!/bin/bash

#Import tools for compiling extension binaries
export PATH=$PATH:/opt/libreoffice5.3/sdk/bin/

#Setup directories 
mkdir "${PWD}"/LOC/
mkdir "${PWD}"/LOC/META-INF/

#Compile the binaries
idlc -I /opt/libreoffice5.3/sdk/idl "${PWD}"/idl/XLoc.idl
regmerge -v "${PWD}"/LOC/XLoc2.rdb UCR "${PWD}"/idl/XLoc.urd
rm "${PWD}"/idl/XLoc.urd

#Copy extension files and generate metadata
cp -f "${PWD}"/src/loc.py "${PWD}"/LOC/
#cp -f "${PWD}"/src/errors.py "${PWD}"/LOC/
#cp -f "${PWD}"/src/exchange.py "${PWD}"/LOC/
#cp -f "${PWD}"/src/exchanges.py "${PWD}"/LOC/
#cp -f "${PWD}"/src/version.py "${PWD}"/LOC/
cp -f "${PWD}"/src/description-en-US.txt "${PWD}"/LOC/
python "${PWD}"/src/generate_metainfo.py

#Package into oxt file
pushd "${PWD}"/LOC/
zip -r "${PWD}"/LOC.zip ./*
popd
mv "${PWD}"/LOC/LOC.zip "${PWD}"/LOC2.oxt
