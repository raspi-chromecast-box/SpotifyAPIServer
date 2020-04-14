FROM alpine:latest
RUN apk add nano
RUN apk add python3-dev
RUN apk add bash
RUN apk add python3
RUN apk add py3-pip
RUN pip3 install pychromecast
RUN pip3 install pathlib
RUN pip3 install UUID
RUN pip3 install redis
RUN pip3 install schedule
RUN pip3 install pprint
RUN pip3 install Flask
RUN pip3 install gevent

COPY python_app /home/python_app
WORKDIR "/home/python_app"
ENTRYPOINT [ "flask" , "run" ]