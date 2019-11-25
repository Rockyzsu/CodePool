FROM busybox:latest
ADD . /packed/tools
VOLUME ["/operations/tools"]
ENTRYPOINT /packed/tools/loader.sh
