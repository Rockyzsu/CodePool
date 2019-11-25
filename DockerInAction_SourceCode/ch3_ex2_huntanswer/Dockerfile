FROM busybox
ADD . /

CMD head Dockerfile | sha1sum | cut -d ' ' -f 0
