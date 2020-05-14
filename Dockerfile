FROM alpine:latest

MAINTAINER Basavaraj Lamani baslama1@in.ibm.com

RUN apk add --no-cache python3 \
    && pip3 install --upgrade pip

WORKDIR /common-tag-schema-api-automation

COPY . /common-tag-schema-api-automation

RUN pip --no-cache-dir install .

#COPY common_tag_api_tests.conf /usr/.common_tag/config/common_tag_api_tests.conf

#ENTRYPOINT "pytest" "-s" "-v" "--cache-clear" "--html=report.html"

RUN "chmod" "+x" "./docker-entrypoint.sh"

ENTRYPOINT ["sh", "./docker-entrypoint.sh"]