FROM busybox
COPY . /watcher
WORKDIR /watcher

RUN adduser -DHs /bin/bash example
RUN chown example watcher.sh
RUN chmod a+x watcher.sh
USER example

CMD ["/watcher/watcher.sh"]
