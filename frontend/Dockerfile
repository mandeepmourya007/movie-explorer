# ── Stage 1: build (includes lint + tests) ──────────────────────────────────
FROM node:22-slim AS build

WORKDIR /app

# Install dependencies first (layer cache)
COPY package*.json ./
RUN npm ci

# Copy source
COPY . .

# Lint — fail build on any lint error
RUN npm run lint

# Tests — fail build on any test failure
RUN npm run test:run

# Compile TypeScript + build production bundle
RUN npx vue-tsc --noEmit && npm run build -- --mode production

# ── Stage 2: serve via nginx ─────────────────────────────────────────────────
FROM nginx:alpine AS runtime

COPY --from=build /app/dist /usr/share/nginx/html
# Templated so the Django backend's address can be resolved from the
# environment at container start — nginx's built-in entrypoint runs
# envsubst on files under /etc/nginx/templates/ automatically.
COPY nginx.conf.template /etc/nginx/templates/default.conf.template

ENV BACKEND_SCHEME=http
ENV BACKEND_URL=backend:8000

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
