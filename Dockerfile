FROM python:3.7-alpine
RUN apk add bash
RUN apk add nano
RUN apk add alpine-sdk
RUN apk add g++
RUN apk add build-base
RUN apk add linux-headers
RUN apk add autoconf
RUN apk add musl-dev
RUN apk add python3-dev
RUN apk add curl
RUN apk add wget
RUN apk add git
RUN apk add automake
RUN apk add libtool
RUN apk add bzip2-dev
RUN apk add ncurses-dev
RUN apk add openssl
RUN apk add openssl-dev
RUN apk add readline-dev
RUN apk add sqlite-dev
RUN apk add m4
RUN apk add intltool
RUN apk add libc-dev
RUN apk add libffi
RUN apk add libffi-dev
RUN apk add libuv
RUN apk add libuv-dev
RUN apk add libxml2
RUN apk add libxml2-dev
RUN apk add libxslt-dev
RUN apk add libxslt-dev

RUN apk add ca-certificates
RUN update-ca-certificates

RUN pip install -U pip
RUN pip install setuptools
RUN pip install psutil
RUN pip install pyOpenSSL
RUN pip install flake8
RUN pip install sphinx
RUN pip install pychromecast
RUN pip install pathlib
RUN pip install UUID
RUN pip install redis
RUN pip install schedule
RUN pip install pprint
RUN pip install sanic
RUN wget https://github.com/raspi-chromecast-box/Alpine-Linux-lxml-whl-4.5.0/raw/master/lxml-4.5.0-cp37-cp37m-linux_armv7l.whl
RUN pip install lxml-4.5.0-cp37-cp37m-linux_armv7l.whl
RUN pip install spotify_token
RUN pip install spotipy

COPY python_app /home/python_app
WORKDIR "/home/python_app"
ENTRYPOINT [ "python" , "server.py" ]