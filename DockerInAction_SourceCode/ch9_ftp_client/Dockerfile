FROM gliderlabs/alpine:3.1
MAINTAINER Jeff Nickoloff "jeff@allingeek.com"
LABEL dia_excercise=ch9_ftp_client
RUN apk-install lftp
VOLUME ["/data"]
WORKDIR /data
ENTRYPOINT ["lftp"]
CMD ["ftp_server"]
