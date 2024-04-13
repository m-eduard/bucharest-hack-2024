FROM node:lts-alpine3.19
WORKDIR /app

COPY package.json .
RUN npm install -y

COPY . .
RUN npx hardhat test

CMD	npx hardhat node


#RUN npm init -y
#RUN npm install -y --save-dev "hardhat@^2.22.2"
#run npm install -g -y --save-dev hardhat
#RUN npx hardhat -y init
#ENTRYPOINT /bin/sh

