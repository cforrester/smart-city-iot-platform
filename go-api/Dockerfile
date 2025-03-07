# Use the official Golang image as a base
FROM golang:1.23

WORKDIR /app

# Copy go.mod and go.sum and download dependencies
COPY go.mod go.sum ./
RUN go mod download

# Copy the source code
COPY . .

# Build the Go application
RUN go build -o api

# Expose port 8080
EXPOSE 8080

# Run the API
CMD ["./api"]
