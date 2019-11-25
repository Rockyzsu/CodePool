FROM centos:6
MAINTAINER Jeff Nickoloff "jeff@allingeek.com"
LABEL dia_excercise=ch9_ftpd
RUN yum -y install vsftpd && \
    chmod -R a-w /var/ftp && \
    mkdir /var/ftp/pub/incoming && \
    chown -R ftp:ftp /var/ftp && \
    chmod a+w /var/ftp/pub/incoming
COPY ./vsftpd.conf /etc/vsftpd/vsftpd.conf
ENTRYPOINT ["/usr/sbin/vsftpd","/etc/vsftpd/vsftpd.conf"]
