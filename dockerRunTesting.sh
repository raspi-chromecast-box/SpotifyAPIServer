#!/bin/bash
sudo docker run -it \
--name 'alpine-spotify-api-server' \
--network host \
alpine-spotify-api-server