#!/bin/bash
sudo docker run -dit --restart='always' \
--name 'alpine-spotify-api-server' \
--network host \
alpine-spotify-api-server