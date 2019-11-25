FROM busybox:latest
COPY . /example
WORKDIR /example

RUN adduser -DHs /bin/bash example
RUN chown example *
RUN chmod a+x *
USER example

CMD ["/example/hunt.sh"]
