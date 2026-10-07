# Production image: a static file server for the prebuilt site/ folder.
# Only package*.json and site/ go into the image (see .dockerignore); sources, photos and ads stay out.
FROM node:20-alpine
WORKDIR /app
COPY package.json package-lock.json ./
RUN npm ci --omit=dev && npm cache clean --force
COPY site ./site
ENV NODE_ENV=production
CMD ["npm", "start"]
