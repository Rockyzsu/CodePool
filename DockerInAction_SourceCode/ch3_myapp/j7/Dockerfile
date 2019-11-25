FROM java:7
COPY . /example
WORKDIR /example

RUN adduser --system --no-create-home --disabled-password --disabled-login --shell /bin/sh example
RUN chown example /example
RUN chown example /example/*
USER example

RUN javac Main.java
CMD ["java", "Main"]
