FROM debian:jessie
LABEL source=dockerinaction
LABEL category=utility
RUN apt-get update && apt-get upgrade -y && apt-get install -y apache2-utils
ENTRYPOINT ["htpasswd"]
