# build environment
FROM node:13.12.0-alpine as build
WORKDIR /app
ENV PATH /app/node_modules/.bin:$PATH
COPY package.json .

RUN npm i
COPY . .
RUN npm run build

# production environment
FROM nginx:stable-alpine
COPY --from=build /app/build /usr/share/nginx/html/
COPY nginx.conf /etc/nginx/conf.d/default.conf

# logging
RUN mkdir -p /app/logs
RUN touch /app/logs/nginx_error.log
RUN touch /app/logs/nginx_access.log

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]