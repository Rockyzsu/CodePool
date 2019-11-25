FROM debian:jessie
RUN apt-get update && \
    apt-get install -y figlet ruby && \
    gem install lolcat
COPY magic.sh /magic.sh
RUN chmod a+x /magic.sh
ENTRYPOINT ["/magic.sh"]
CMD ["Welcome to painted text!"]
