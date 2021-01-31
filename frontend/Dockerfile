FROM node:12.20.0-alpine3.12
WORKDIR /usr/src/zpk

ENV PATH /usr/src/zpk/node_modules/.bin:$PATH

COPY package.json package-lock.json ./
RUN npm install --silent

COPY . ./
