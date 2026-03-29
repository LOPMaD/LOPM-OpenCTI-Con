FROM python:3.12-alpine

# TimeZone
# ENV TZ=Europe/Kyiv
# RUN apk add --no-cache tzdata && \
#     cp /usr/share/zoneinfo/$TZ /etc/localtime && \
#     echo $TZ > /etc/timezone && \
#     apk del tzdata


COPY src /opt/opencti-connector-lopmconnector
COPY requirements.txt /opt/opencti-connector-lopmconnector

# RUN apk update && apk upgrade
# RUN apk add git
# RUN apk add python3
# RUN apk add py3-pip
RUN apk add --no-cache file libmagic git
RUN cd /opt/opencti-connector-lopmconnector && \
    pip install -r requirements.txt --break-system-packages


COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]


#RUN apk add git build-base libmagic libffi-dev


# FROM ubuntu:24.04

# COPY src /opt/opencti-connector-lopmconnector
# COPY requirements.txt /opt/opencti-connector-lopmconnector


# RUN apt update && apt upgrade
# RUN apt install -y git
# #Возможно хуета
# #RUN apt install -y build-essential libmagic1 libffi-dev libxml2-dev libxslt1-dev 

# RUN apt install -y python3.12 python3 python3-pip
# RUN pip install -r requirements.txt --break-system-packages

# # COPY entrypoint.sh /entrypoint.sh
# # RUN chmod +x /entrypoint.sh
# # ENTRYPOINT ["/entrypoint.sh"]