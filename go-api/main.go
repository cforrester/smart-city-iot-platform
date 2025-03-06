package main

import (
	"bytes"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"

	"github.com/gin-gonic/gin"
)

func main() {
	r := gin.Default()

	// Simple endpoint that calls the Python ML service
	r.POST("/predict", func(c *gin.Context) {
		// Forward the JSON request to the ML service
		jsonData, err := c.GetRawData()
		if err != nil {
			c.JSON(http.StatusBadRequest, gin.H{"error": "Invalid request"})
			return
		}

		resp, err := http.Post("http://python-ml:8000/predict", "application/json", bytes.NewBuffer(jsonData))
		if err != nil {
			c.JSON(http.StatusInternalServerError, gin.H{"error": "ML service unreachable"})
			return
		}
		defer resp.Body.Close()

		body, _ := ioutil.ReadAll(resp.Body)
		c.Data(resp.StatusCode, "application/json", body)
	})

	if err := r.Run(":8080"); err != nil {
		log.Fatal(err)
	}
}
