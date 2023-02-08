# Building ng-app
FROM node:12-stretch AS build
RUN mkdir /home/task-clarity
WORKDIR /home/task-clarity
COPY application-code/package*.json ./
RUN npm ci
COPY application-code .
RUN npm run build

# Serving ng-app using node server
FROM node:12-alpine
USER node
RUN mkdir /home/node/task-clarity
WORKDIR /home/node/task-clarity
COPY --from=build --chown=node:node /home/task-clarity/dist /home/node/task-clarity/dist
COPY --chown=node:node node-server/package*.json /home/node/task-clarity/
RUN npm ci
COPY --chown=node:node node-server/server.js /home/node/task-clarity/server.js
CMD ["npm", "run", "start"]