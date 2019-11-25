FROM ubuntu:latest
MAINTAINER Jeff Nickoloff <jeff@allingeek.com>
RUN apt-get update && apt-get install -y stress
CMD /usr/bin/stress -c 4 -t 30
