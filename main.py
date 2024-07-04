import os 
from confluent_kafka import SerializingProducer
import simplejson as json
from datetime import datetime
LONDON_COORDINATES = {
    'latitude': 51.5074,
    'longitude': -0.1278
}
BIERMINGHAM_COORDINATES = {
    'latitude': 52.4823,
    'longitude': -1.8900
}
LATITUDE_INCREMENT = (BIERMINGHAM_COORDINATES['latitude']
                      -LONDON_COORDINATES['latitude']) / 100  # convert
LONGITUDE_INCREMENT = (BIERMINGHAM_COORDINATES['longitude']
                       -LONDON_COORDINATES['longitude']) / 100  # convert


KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
VEHICLE_TOPIC = os.getenv('VEHICLE_TOPIC' ,'vehicle_data')
GPS_TOPIC = os.getenv('GPS_TOPIC','gps_data')
TRAFFIC_TOPIC = os.getenv('TRAFFIC_TOPIC','traffic_data')
WEATHER_TOPIC = os.getenv('WEATHER_TOPIC','weather_data')
EMERGENCY_TOPIC = os.getenv('EMERGENCY_TOPIC','emergency_data')

start_time = datetime.now()
start_location = LONDON_COORDINATES.copy()


def simulate_journey(producer , device_id):
    while True:
        vehicle_data = generate_vehicle_data(device_id)
        

if __name__ == '__main__':
    producer_config = {
        'bootstrap.servers': KAFKA_BOOTSTRAP_SERVERS,
        'error_cb': lambda err: print(f'kafka error: {err}')
    }
    producer = SerializingProducer(producer_config) 
    
    try:
       
       simulate_journey(producer , 'Vehicle-123')
       
    except KeyboardInterrupt :  
        print('simulation ended by the user')
    except Exception as e : 
        print(f'Unexpected Error occured : {e}')
        