FROM node:12-alpine 
RUN mkdir /nodeapp 
WORKDIR /nodeapp 
RUN npm i npm@latest -g 
COPY package.json package-lock.json* /nodeapp/ 
RUN npm install --no-optional && npm cache clean --force 
COPY . /nodeapp 
CMD [ "npm", "start" ]


