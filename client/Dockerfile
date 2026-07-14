FROM node:20-slim AS deps
WORKDIR /app/client
COPY client/package.json client/package-lock.json ./
RUN npm ci

FROM deps AS build
COPY client/ ./
ARG LAPP_PUBLIC_HOST
ARG LAPP_PUBLIC_PORT
ENV LAPP_PUBLIC_HOST=$LAPP_PUBLIC_HOST LAPP_PUBLIC_PORT=$LAPP_PUBLIC_PORT
RUN node_modules/.bin/next build

FROM node:20-slim AS runtime
WORKDIR /app/client
COPY --from=build /app/client ./
ARG LAPP_PUBLIC_HOST
ARG LAPP_PUBLIC_PORT
ENV NODE_ENV=production PORT=3000 LAPP_PUBLIC_HOST=$LAPP_PUBLIC_HOST LAPP_PUBLIC_PORT=$LAPP_PUBLIC_PORT
EXPOSE 3000
CMD ["node_modules/.bin/next", "start"]
