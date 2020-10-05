#! /bin/bash

wget "https://raw.githubusercontent.com/uboot/conan-ci/master/kubernetes/conan-server/server.conf.in" \
&& sed -e "s/SECRET/$CONAN_USER_PASSWORD/g" /config/server.conf.in > /config/server.conf \
&& rm /config/server.conf.in \
&& rm /config/setup_server_config.sh
