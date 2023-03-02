FROM ubuntu:jammy as builder

# Setup build dependencies
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates \
    build-essential \
    git \
    zlib1g-dev \
    libpcre3-dev

# get source files for mod_zip and nginx

RUN : \
    && git clone https://github.com/evanmiller/mod_zip.git \
    && git clone https://github.com/nginx/nginx.git && cd ./nginx && git checkout release-1.22.1 \
    && :

# build the mod_zip module

RUN : \
    && cd ./nginx \
    && ./auto/configure --with-compat --add-dynamic-module=../mod_zip/ \
    && make -f ./objs/Makefile modules \
    && :


FROM nginx:1.22 as runner

COPY --from=builder ./nginx/objs/ngx_http_zip_module.so /usr/lib/nginx/modules/

# setup mod_zip plugin

RUN : \
    && chmod 644 /usr/lib/nginx/modules/ngx_http_zip_module.so \
    && sed -i '1 s/^/load_module modules\/ngx_http_zip_module.so;\n/' /etc/nginx/nginx.conf \
    && :

# setup demo FastAPI application

RUN : \
    && rm /etc/nginx/conf.d/default.conf \
    && apt-get update && apt-get install -y --no-install-recommends python3 python3-pip \
    && python3 -m pip install virtualenv \
    && virtualenv venv \
    && . ./venv/bin/activate \
    && python -m pip install fastapi uvicorn \
    && :

COPY main.py  .
COPY fastapi_demo.conf /etc/nginx/conf.d/
COPY test1.txt /usr/share/nginx/html/
COPY test2.txt /usr/share/nginx/html/
