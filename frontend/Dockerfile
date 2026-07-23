# Stage 1: Build
FROM node:20-alpine as builder

WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

# Stage 2: Serve
FROM node:20-alpine

WORKDIR /app
RUN npm install -g serve
COPY --from=builder /app/dist ./dist

EXPOSE 5173

# using standard vite port for convenience, although serve uses 3000 by default usually, we will bind to 5173
CMD ["serve", "-s", "dist", "-l", "5173"]
