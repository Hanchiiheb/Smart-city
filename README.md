# Smart City IoT Data Streaming Platform

## 🏙️ Overview

This project implements a real-time IoT data streaming platform for smart city applications. It simulates various IoT sensors from a vehicle journey between London and Birmingham, processing the data through Apache Kafka and Apache Spark, and storing it in AWS S3 for analytics.

## 🏗️ Architecture

```
IoT Data Generator → Apache Kafka → Apache Spark Streaming → AWS S3
     (main.py)         (Topics)        (smart-city.py)       (Parquet)
```

### Data Flow
1. **Data Generation**: Simulates IoT sensors generating vehicle, GPS, traffic, weather, and emergency data
2. **Message Streaming**: Kafka handles real-time data ingestion across 5 topics
3. **Stream Processing**: Spark Streaming processes and validates data with structured schemas
4. **Data Storage**: Processed data is stored in AWS S3 in Parquet format for analytics

## 📊 Data Sources

The platform simulates 5 types of IoT data streams:

| Data Type | Description | Update Frequency |
|-----------|-------------|------------------|
| **Vehicle Data** | Location, speed, fuel efficiency, vehicle specifications | ~50s intervals |
| **GPS Data** | Device tracking, speed, direction | Real-time |
| **Traffic Camera** | Camera snapshots, location monitoring | Per location |
| **Weather Data** | Temperature, humidity, wind, pressure | Environmental |
| **Emergency Incidents** | Accidents, medical, fire, police events | Event-driven |

## 🛠️ Technology Stack

- **Data Generation**: Python with Confluent Kafka
- **Message Broker**: Apache Kafka with Zookeeper
- **Stream Processing**: Apache Spark (PySpark)
- **Cloud Storage**: AWS S3
- **Containerization**: Docker & Docker Compose
- **Data Format**: JSON (streaming) → Parquet (storage)

## 📋 Prerequisites

- Docker and Docker Compose
- Python 3.8+
- AWS Account with S3 access
- 8GB+ RAM recommended for Spark cluster

## 🚀 Quick Start

### 1. Clone and Setup

```bash
git clone <repository-url>
cd Smart-city
```

### 2. Configure AWS Credentials

Create a `config.py` file in the `jobs/` directory:

```python
configuration = {
    'AWS_ACCESS_KEY': 'your-aws-access-key',
    'AWS_SECRET_KEY': 'your-aws-secret-key'
}
```

**⚠️ Security Note**: Never commit AWS credentials to version control. Use environment variables in production.

### 3. Fix Docker Compose Issues

Before running, fix these configuration errors in `docker-compose.yml`:

```yaml
# Line 47: Fix environment variable name
KAFKA_ZOOKEEPER_CONNECT: 'zookeeper:2181'  # was: kafka_ZOOKEEPER_CONNECT

# Line 49: Fix listener configuration
KAFKA_ADVERTISED_LISTENERS: PLAINTEXT://broker:29092,PLAINTEXT_HOST://localhost:9092

# Line 58: Fix hostname case
KAFKA_JMX_HOSTNAME: localhost  # was: Localhost
```

### 4. Start Infrastructure

```bash
# Start Kafka, Zookeeper, and Spark cluster
docker-compose up -d

# Verify services are running
docker-compose ps
```

### 5. Install Python Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run Data Generation

```bash
cd jobs
python main.py
```

### 7. Run Stream Processing

```bash
# Submit Spark job
docker exec -it <spark-master-container> spark-submit \
  --packages org.apache.spark:spark-sql-kafka-0-10_2.13:3.5.0 \
  /opt/bitnami/spark/jobs/smart-city.py
```

## 📁 Project Structure

```
Smart-city/
├── docker-compose.yml          # Infrastructure orchestration
├── requirements.txt            # Python dependencies
├── README.md                  # This file
└── jobs/
    ├── main.py               # IoT data generator & Kafka producer
    ├── smart-city.py         # Spark streaming consumer
    └── config.py             # AWS configuration (create this)
```

## ⚙️ Configuration

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `KAFKA_BOOTSTRAP_SERVERS` | `localhost:9092` | Kafka broker endpoints |
| `VEHICLE_TOPIC` | `vehicle_data` | Vehicle data topic |
| `GPS_TOPIC` | `gps_data` | GPS data topic |
| `TRAFFIC_TOPIC` | `traffic_data` | Traffic camera topic |
| `WEATHER_TOPIC` | `weather_data` | Weather data topic |
| `EMERGENCY_TOPIC` | `emergency_data` | Emergency incident topic |

### Spark Configuration

- **Workers**: 2x workers with 2GB memory each
- **Master URL**: `spark://spark-master:7077`
- **Checkpointing**: Enabled for fault tolerance
- **Watermarking**: 2-minute window for late data

### AWS S3 Configuration

Data is stored in the following S3 structure:
```
s3://smartcityprojectt/
├── data/
│   ├── vehicle_data/
│   ├── gps_data/
│   ├── traffic_data/
│   ├── weather_data/
│   └── emergency_data/
└── checkpoints/
    ├── vehicle_data/
    ├── gps_data/
    ├── traffic_data/
    ├── weather_data/
    └── emergency_data/
```

## 🚨 Known Issues & Fixes Needed

### Critical Issues
1. **Docker Configuration**: Multiple typos in `docker-compose.yml` (see Quick Start #3)
2. **Missing Configuration**: `config.py` file needs to be created
3. **Code Typos**: 
   - Line 147 in `main.py`: `trafffic_camera_data` → `traffic_camera_data`
   - Line 149 in `main.py`: `emegency_incident_data` → `emergency_incident_data`
   - Line 152-155: Missing `break` statement in journey termination logic

### Schema Mismatches
- Vehicle type field: `vehicle_type` (generated) vs `vehicleType` (expected)
- Weather schema: Generated fields don't match consumption schema

### Security Improvements Needed
- Move AWS credentials to environment variables
- Implement proper secrets management
- Add authentication for Kafka and Spark

## 📊 Monitoring & Observability

### Access Points
- **Spark UI**: http://localhost:9090
- **Kafka**: localhost:9092

### Logs
```bash
# View service logs
docker-compose logs kafka
docker-compose logs spark-master
docker-compose logs spark-worker-1

# View streaming logs
docker exec -it <spark-master> tail -f /opt/bitnami/spark/logs/spark-master.out
```

## 🔧 Development

### Adding New Data Sources
1. Create data generation function in `main.py`
2. Define Kafka topic and schema
3. Add schema definition in `smart-city.py`
4. Update stream processing logic

### Scaling
- **Horizontal**: Add more Spark workers in `docker-compose.yml`
- **Vertical**: Increase worker memory/cores
- **Kafka**: Add more broker instances for higher throughput

## 🧪 Testing

### Data Generation Verification
```bash
# Check Kafka topics
docker exec -it <broker-container> kafka-topics --list --bootstrap-server localhost:9092

# Monitor topic data
docker exec -it <broker-container> kafka-console-consumer \
  --topic vehicle_data --bootstrap-server localhost:9092 --from-beginning
```

### S3 Data Verification
```bash
# List S3 objects (requires AWS CLI)
aws s3 ls s3://smartcityprojectt/data/vehicle_data/ --recursive
```

## 🚀 Future Enhancements

### Planned Features
- [ ] Real-time analytics dashboard
- [ ] Machine learning models for predictive analytics
- [ ] Stream processing optimizations
- [ ] Data quality monitoring
- [ ] Alerting system for emergency incidents
- [ ] API for real-time data access

### Potential Integrations
- **Grafana**: Real-time dashboards
- **Elasticsearch**: Advanced search and analytics
- **Apache Airflow**: Workflow orchestration
- **Kubernetes**: Production-grade orchestration

## 🤝 Contributing

1. Fix the known issues listed above
2. Add comprehensive error handling
3. Implement proper logging
4. Add unit tests
5. Improve documentation

## 📝 License

This project is for educational and demonstration purposes.

## 📧 Support

For questions or issues:
1. Check the Known Issues section
2. Verify all prerequisites are met
3. Check Docker container logs
4. Ensure AWS credentials are properly configured

---

**Note**: This is a demonstration project. For production use, implement proper security, monitoring, and error handling practices.
