#!/bin/bash

set -e

browser=$1

if [ -z "$browser" ]; then
  echo "Specify browser (chrome or firefox):"
  exit 1
fi

# set current working directory to directory of the shell script
cd "$(dirname "$0")"


# cleanup
rm -rf ../vendor
rm -f ../color-finder-exension.zip
mkdir -p ../vendor

### Install packages ###

# npm install package.json
npm ci 2> /dev/null || npm i

# tmp for mdc
mkdir -p tmp
echo "Linha 28"

# copy bootstrap
cp node_modules/bootstrap/dist/css/bootstrap.min.css ../vendor/bootstrap.min.css
cp node_modules/bootstrap/dist/js/bootstrap.bundle.js ../vendor/bootstrap.bundle.js

# Copy Jquery
curl https://cdnjs.cloudflare.com/ajax/libs/jquery/3.1.1/jquery.min.js --output ../vendor/jquery.min.js

curl https://cdnjs.cloudflare.com/ajax/libs/jquery-jcrop/0.9.12/js/jquery.Jcrop.min.js --output ../vendor/jquery.Jcrop.min.js
curl https://cdnjs.cloudflare.com/ajax/libs/jquery-jcrop/0.9.12/css/jquery.Jcrop.min.css --output ../vendor/jquery.Jcrop.min.css
curl https://cdnjs.cloudflare.com/ajax/libs/jquery-jcrop/0.9.12/css/Jcrop.gif --output ../vendor/Jcrop.gif

# mdc.min.js
npx rollup --config mdc/rollup.mjs --input mdc/mdc.mjs --file tmp/mdc.js
npx terser --compress --mangle -- tmp/mdc.js > tmp/mdc.min.js

# mdc.min.css
npx node-sass --include-path node_modules/ mdc/mdc.scss tmp/mdc.css
npx csso --input tmp/mdc.css --output tmp/mdc.min.css

# copy
cp tmp/mdc.min.* ../vendor/

# after
rm -rf node_modules/ tmp/

### Build extension ###

mkdir -p tmp
mkdir -p tmp/color-finder-extension

cd ..
cp -r background content icons vendor page build/tmp/color-finder-extension

if [ "$browser" = "chrome" ]; then
  cp manifest.chrome.json build/tmp/color-finder-extension/manifest.json
  cp manifest.chrome.json manifest.json
elif [ "$browser" = "firefox" ]; then
  cp manifest.firefox.json build/tmp/color-finder-extension/manifest.json
  cp manifest.firefox.json manifest.json
fi

if [ "$browser" = "chrome" ]; then
  cd build/tmp/
  zip -r ../../color-finder-extension.zip color-finder-extension
  cd ..
elif [ "$browser" = "firefox" ]; then
  cd build/tmp/color-finder-extension/
  zip -r ../../../color-finder-extension.zip .
  cd ../../
fi

rm -rf tmp/

echo "Build created."