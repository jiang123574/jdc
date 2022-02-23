FROM alpine
LABEL AUTHOR="ClegeA <amlhbmcxMjM1NzRAMTYzLmNvbQ==>"
RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.tuna.tsinghua.edu.cn/g' /etc/apk/repositories \
    && set -ex && apk update && apk upgrade \
    && apk add --update --no-cache curl tzdata python3 python3-dev py3-configobj py3-pip py3-setuptools git \
    && pip install --upgrade pip \
    && ln -sf /usr/share/zoneinfo/Asia/Shanghai /etc/localtime \
    && echo "Asia/Shanghai" > /etc/timezone \
    && mkdir /jdc \
    && cd /jdc \
    && git clone https://github.com/jiang123574/jdc.git \
    && crontab /jdc/jdc/mycrontab.sh \

