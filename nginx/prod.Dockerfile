FROM nginx:1.19-alpine

COPY ./build /usr/share/nginx/html
RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.prod.conf /etc/nginx/conf.d
RUN mv /etc/nginx/conf.d/nginx.prod.conf /etc/nginx/conf.d/nginx.conf
