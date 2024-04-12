package main

import (
	"log"
	"os"
	"strconv"
	"strings"
	"time"

	influxdb2 "github.com/influxdata/influxdb-client-go/v2"
	"github.com/nats-io/nats.go"
)

func main() {
	// Connect to NATS server
	nc, err := nats.Connect(nats.DefaultURL)
	if err != nil {
		log.Fatalf("Error connecting to NATS: %v", err)
	}
	defer nc.Close()

	// Subscribe to NATS subject for metrics
	sub, err := nc.SubscribeSync("system_metrics")
	if err != nil {
		log.Fatalf("Error subscribing to NATS subject: %v", err)
	}

	// Initialize InfluxDB client with default values or environment variables
	influxURL := getEnvOrDefault("INFLUXDB_URL", "http://localhost:8086")
	influxToken := getEnvOrDefault("INFLUXDB_TOKEN", "ueT24d11Q11a87e1HT2lPXJFOADF6HppaL89htNxRkkBPmWXF4FCipSxewX-6pLheGVCuAHqFVLcFDsEiiQH4w==")
	influxOrg := getEnvOrDefault("INFLUXDB_ORG", "org1")
	influxBucket := getEnvOrDefault("INFLUXDB_BUCKET", "bucket1")

	client := influxdb2.NewClient(influxURL, influxToken)
	defer client.Close()

	writeAPI := client.WriteAPI(influxOrg, influxBucket)

	// Infinite loop to read messages from NATS
	for {
		time.Sleep(10 * time.Second)
		msg, err := sub.NextMsg(-1)
		if err != nil {
			log.Printf("Error reading message from NATS: %v", err)
			continue
		}

		// Process the message (e.g., parse metrics and push to InfluxDB)
		log.Printf("Received message: %s", msg.Data)

		message := string(msg.Data)
		// Example parsing and pushing metrics to InfluxDB
		parts := strings.Split(message, ",")
		if len(parts) != 6 {
			log.Printf("Invalid message format: %s, length: %d", message, len(parts))
			return
		}

		// Extract metrics and hostname/IP from message parts
		hostname := parts[0]
		totalMemory := parts[2]
		usedMemory := parts[3]
		diskUsage := parts[4]
		usedDisk := parts[5]

		cpuUsageSuffix := strings.TrimSpace(strings.TrimSuffix(parts[1], "%"))
		cpuUsage := strings.TrimSpace(strings.TrimPrefix(cpuUsageSuffix, "CPU Usage: "))
		cpuUsageFloat, err := strconv.ParseFloat(cpuUsage, 64)
		if err != nil {
			log.Printf("Error parsing CPU usage: %v", err)
			continue
		}
		//
		// Prepare data point
		point := influxdb2.NewPoint("system_metrics",
			map[string]string{"hostname": hostname},
			map[string]interface{}{
				"cpu_usage":    cpuUsageFloat,
				"total_memory": totalMemory,
				"used_memory":  usedMemory,
				"disk_usage":   diskUsage,
				"used_disk":    usedDisk,
			},
			time.Now(),
		)

		// Write data point to InfluxDB
		writeAPI.WritePoint(point)
		// if err != nil {
		// 	log.Printf("Error writing point to InfluxDB: %v", err)
		// 	return
		// }

		log.Println("Metrics pushed to InfluxDB successfully")
	}
}

func getEnvOrDefault(key, defaultValue string) string {
	value, exists := os.LookupEnv(key)
	if !exists {
		return defaultValue
	}
	return value
}
