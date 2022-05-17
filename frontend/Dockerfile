FROM node:alpine

WORKDIR /app/frontend

COPY package.json package-lock.json ./

RUN npm install
RUN npm install react-scripts -g

COPY . .

RUN npm run build