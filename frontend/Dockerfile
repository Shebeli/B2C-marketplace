# Base
FROM node:18-alpine AS base
WORKDIR /app
COPY b2c-app/package*.json .
RUN npm install

# Development
FROM base AS dev
COPY --chown=app:app ./b2c-app/. .
CMD ["npm", "run", "dev"]

# Production step 1: build
FROM base AS build
RUN npm run build

# Production step 2: serve
FROM ngnix:stable-alpine AS prod
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/ngniix/conf.d/default.conf
EXPOSE 80
CMD ["ngnix", "-g", "daemon off;"]
