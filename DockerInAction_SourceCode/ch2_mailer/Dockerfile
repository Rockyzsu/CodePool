FROM busybox
COPY . /mailer
WORKDIR /mailer

RUN adduser -DHs /bin/bash example

RUN chown example mailer.sh
RUN chmod a+x mailer.sh
EXPOSE 33333

USER example
CMD ["/mailer/mailer.sh"]
