FROM node:14.14.0 as build_stage

WORKDIR /app
COPY reactapp/package.json .
COPY reactapp/.env.production .env
RUN yarn
COPY reactapp .
RUN yarn build

FROM nginx:1.16.0-alpine

COPY --from=build_stage /app/build /usr/share/nginx/html
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

ENTRYPOINT ["nginx", "-g", "daemon off;"]