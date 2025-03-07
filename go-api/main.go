// go-api/main.go
package main

import (
	"bytes"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	"github.com/gin-gonic/gin"
)

func main() {
	// Create a new Gin router
	router := gin.Default()

	// Define an endpoint that receives a request and forwards it to the ML service
	router.POST("/predict", func(c *gin.Context) {
		// Read the raw JSON payload from the client request
		jsonData, err := c.GetRawData()
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request payload"})
			return
		}

		// Forward the request to the Python ML service
		// In a Docker environment, "python-ml" is the service name defined in docker-compose
		mlServiceURL := os.Getenv("ML_SERVICE_URL")
		if mlServiceURL == "" {
			mlServiceURL = "http://python-ml:8000/predict"
		}
		resp, err := http.Post(mlServiceURL, "application/json", bytes.NewBuffer(jsonData))
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "ML service unreachable"})
			return
		}
		defer resp.Body.Close()

		// Read the response from the ML service
		body, err := ioutil.ReadAll(resp.Body)
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "Error reading ML response"})
			return
		}

		// Return the ML service response back to the client
		c.Data(resp.StatusCode, "application/json", body)
	})

	// Start the Go API server on port 8080
	if err := router.Run(":8080"); err != nil {
		log.Fatal(err)
	}
}
