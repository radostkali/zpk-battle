FROM node:12.20.0-alpine3.12 as build-stage

WORKDIR /usr/src/zpk

COPY frontend ./
RUN npm i --silent
RUN npm run build


FROM nginx:1.19-alpine

COPY --from=build-stage  /usr/src/zpk/build /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx/nginx.prod.conf /etc/nginx/conf.d
RUN mv /etc/nginx/conf.d/nginx.prod.conf /etc/nginx/conf.d/nginx.conf
