FROM node:20-slim AS build
WORKDIR /app
ARG VITE_API_URL
ENV VITE_API_URL=${VITE_API_URL}
COPY frontend/package.json frontend/package-lock.json* /app/
RUN npm install
COPY frontend /app
RUN npm run build

FROM node:20-slim
WORKDIR /app
RUN npm install -g serve
COPY --from=build /app/dist /app/dist
EXPOSE 4173
CMD ["serve", "-s", "dist", "-l", "4173"]
