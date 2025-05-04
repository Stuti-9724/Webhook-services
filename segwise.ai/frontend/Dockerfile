# Build stage
FROM node:18-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Start development server with host flag for Docker
CMD ["npm", "run", "dev", "--", "--host"]