FROM node
MAINTAINER Jeff Nickoloff <jeff@allingeek.com>
RUN adduser --system --group --disabled-password -shell /bin/bash example
COPY ./service /usr/src/app
COPY ./Calaca /usr/src/app/public
WORKDIR /usr/src/app
RUN npm install

CMD [ "npm", "start" ]
