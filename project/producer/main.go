package main

import (
	"fmt"
	"log"
	"os"
	"time"

	"github.com/nats-io/nats.go"
	"github.com/shirou/gopsutil/cpu"
	"github.com/shirou/gopsutil/disk"
	"github.com/shirou/gopsutil/mem"
)

func main() {
	// Connect to NATS server
	nc, err := nats.Connect(nats.DefaultURL)
	if err != nil {
		log.Fatalf("Error connecting to NATS: %v", err)
	}
	defer nc.Close()

	// Get the hostname/IP of the system
	hostname, err := os.Hostname()
	if err != nil {
		log.Fatalf("Error getting hostname: %v", err)
	}
	log.Printf("Hostname/IP: %s", hostname)

	// Start collecting metrics periodically
	ticker := time.NewTicker(5 * time.Second)
	defer ticker.Stop()

	for range ticker.C {
		// Collect CPU metrics
		cpuPercent, err := cpu.Percent(time.Second, false)
		if err != nil {
			log.Printf("Error getting CPU percent: %v", err)
		}

		// Collect memory metrics
		memInfo, err := mem.VirtualMemory()
		if err != nil {
			log.Printf("Error getting memory info: %v", err)
		}

		// Collect disk metrics
		partitions, err := disk.Partitions(false)
		if err != nil {
			log.Printf("Error getting disk partitions: %v", err)
		}

		for _, partition := range partitions {
			diskUsage, err := disk.Usage(partition.Mountpoint)
			if err != nil {
				log.Printf("Error getting disk usage for %s: %v", partition.Mountpoint, err)
				continue
			}

			// Construct the message with metrics and hostname/IP
			message := []byte(fmt.Sprintf("Hostname: %s, CPU Usage: %.2f%%, Total Memory: %v, Used Memory: %v, Disk Usage for %s - Total: %v, Used: %v",
				hostname, cpuPercent[0], memInfo.Total, memInfo.Used, partition.Mountpoint, diskUsage.Total, diskUsage.Used))

			// Publish the message to NATS
			err = nc.Publish("system_metrics", message)
			if err != nil {
				log.Printf("Error publishing message to NATS: %v", err)
				continue
			}

			log.Println("Metrics published successfully")
		}
	}
}
