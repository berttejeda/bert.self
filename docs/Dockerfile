FROM python:3.8.3-alpine3.12

ENV USER=svcdocs
ENV USERHOME=/docs
ENV USERPASSWORD=svcdocs
ENV UID=8888
ENV GID=7777

RUN echo "===> Creating docs service user ..."  &&\
adduser \
    --disabled-password \
    --gecos "" \
    --uid "$UID" \
    "$USER"

RUN addgroup $USER wheel 

RUN echo "===> Add the main & community repos"  &&\
    echo "http://dl-cdn.alpinelinux.org/alpine/v3.12/main" > /etc/apk/repositories &&\
    echo "http://dl-cdn.alpinelinux.org/alpine/v3.12/community" >> /etc/apk/repositories &&\
    cat /etc/apk/repositories

RUN apk update && apk -U upgrade

RUN apk --update add curl-dev coreutils

RUN echo "===> Adding Runtime packages ..."  &&\
apk --update add libcurl openssl ca-certificates &&\
apk --update add --virtual build-dependencies libxml2-dev \
libffi-dev libxslt-dev openssl-dev python3-dev build-base cargo

RUN echo "===> Installing handy tools (not absolutely required)..."  &&\
apk --no-cache --update add \
bash \
gcc \
musl-dev \
libffi-dev \
libxml2-dev \
py-dnspython \
bind-tools \
html2text \
git \
jq \
curl

RUN echo "===> Installing pip ..."  &&\
python3 -m ensurepip &&\
pip3 install --trusted-host=pypi.org --trusted-host=github.com \
--trusted-host=files.pythonhosted.org --upgrade pip setuptools wheel 

RUN echo "===> Removing package list..."  &&\
apk del build-dependencies &&\
rm -rf /var/cache/apk/*

RUN mkdir -p /home/$USER/.local/lib/python3.8/site-packages

RUN chown -R $USER:$USER /home/${USER}/.local

RUN ln -s $(which python3) /usr/bin/python

# clean apk cache
RUN  rm -rf /var/cache/apk/*

USER $USER

COPY requirements.* ./

ENV PATH="/home/${USER}/.local/bin:${PATH}"

RUN echo "===> Installing mkdocs and Related Packages ..."  &&\
pip3 install --trusted-host=pypi.org --trusted-host=github.com \
--trusted-host=files.pythonhosted.org -r requirements.txt

WORKDIR $USERHOME

EXPOSE 8000

ENTRYPOINT ["mkdocs"]
CMD [ "serve", "-a", "0.0.0.0:8000" ]