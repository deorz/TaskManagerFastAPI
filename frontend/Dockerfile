FROM node:19-bullseye as build

WORKDIR /frontend

COPY package*.json ./

RUN npm install

COPY . ./

RUN npm run build

CMD cp -r build result_build
