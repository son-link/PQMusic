#!/usr/bin/env bash

# Remove AppDir
rm -r AppDir

# Grab AppImageTools
ARCH=$(uname -m)
wget -nc "https://raw.githubusercontent.com/TheAssassin/linuxdeploy-plugin-conda/master/linuxdeploy-plugin-conda.sh"
wget -nc "https://github.com/linuxdeploy/linuxdeploy/releases/download/continuous/linuxdeploy-${ARCH}.AppImage"
wget -nc "https://github.com/AppImage/AppImageKit/releases/download/12/appimagetool-${ARCH}.AppImage"
chmod +x linuxdeploy-${ARCH}.AppImage linuxdeploy-plugin-conda.sh appimagetool-${ARCH}.AppImage

# Install App

# Set Environment
export CONDA_CHANNELS='local;conda-forge'
export PIP_REQUIREMENTS='pyqt5 mutagen python-magic psutil .'
install -Dm644 bin/io.sonlink.pqmusic.png AppDir/usr/share/icons/pqmusic.png
install -Dm644 bin/io.sonlink.pqmusic.appdata.xml AppDir/usr/share/metainfo/io.sonlink.pqmusic.appdata.xml
# Deploy
./linuxdeploy-x86_64.AppImage \
   --appdir AppDir \
    -i bin/io.sonlink.pqmusic.png \
    -d bin/io.sonlink.pqmusic.desktop \
    --plugin conda \
    --custom-apprun bin/AppRun.sh \
    --output appimage
