import os 
import random
import uuid
from confluent_kafka import SerializingProducer
import simplejson as json
from datetime import datetime, time, timedelta
LONDON_COORDINATES = {
    'latitude': 51.5074,
    'longitude': -0.1278
}
BIRMINGHAM_COORDINATES = {
    'latitude': 52.4823,
    'longitude': -1.8900
}
LATITUDE_INCREMENT = (BIRMINGHAM_COORDINATES['latitude']
                      -LONDON_COORDINATES['latitude']) / 100  # convert
LONGITUDE_INCREMENT = (BIRMINGHAM_COORDINATES['longitude']
                       -LONDON_COORDINATES['longitude']) / 100  # convert


KAFKA_BOOTSTRAP_SERVERS = os.getenv('KAFKA_BOOTSTRAP_SERVERS', 'localhost:9092')
VEHICLE_TOPIC = os.getenv('VEHICLE_TOPIC' ,'vehicle_data')
GPS_TOPIC = os.getenv('GPS_TOPIC','gps_data')
TRAFFIC_TOPIC = os.getenv('TRAFFIC_TOPIC','traffic_data')
WEATHER_TOPIC = os.getenv('WEATHER_TOPIC','weather_data')
EMERGENCY_TOPIC = os.getenv('EMERGENCY_TOPIC','emergency_data')

random.seed(42)
start_time = datetime.now()
start_location = LONDON_COORDINATES.copy()

def get_next_time():
    global start_time
    start_time += timedelta(seconds=random.randint(38 , 68 ))
    return start_time 
   
def generate_gps_data(device_id,timestamp,vehicle_type='private'):
    return {
     'id' : uuid.uuid4() ,
     'deviceId': device_id ,
     'timestamp': timestamp,
     'speed': random.uniform(10,40) , 
     'direction' : 'North-East' ,
     'vehicle_type' : vehicle_type 
     }

def generate_traffic_camera_data(device_id,timestamp,location,camera_id):
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'timestamp': timestamp,
        'cameraId': camera_id,
        'location': location,
        'snapshot': 'Base64EncodedString'
        }
    
def generate_weather_data(device_id,timestamp,location):
    return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'timestamp': timestamp,
        'location': location,
        'temperature': random.uniform(-5,27),
        'weathercondition': random.choice(['Sunny','Cloudy','Rain','Snow']),
        'humidity': random.uniform(60, 80),
        'pressure': random.uniform(980, 1030),
        'windSpeed': random.uniform(0, 10),
        'windDirection': 'North-East'
    }
    

def generate_emergency_incident_data(device_id, timestamp, location):
      return {
        'id': uuid.uuid4(),
        'deviceId': device_id,
        'incidentId': uuid.uuid4(),
        'type': random.choice(['Accident','Fire','Medical','Police','None'] ),
        'timestamp': timestamp,
        'location': location,
        'status': random.choice(['Active' , 'Resolved']) , 
        'description': 'Description of the incident'
      }
def simulate_vehicle_movement(): 
    global start_location
    
    #location 
    start_location['latitude'] += LATITUDE_INCREMENT
    start_location['longitude'] += LONGITUDE_INCREMENT
    
    #add random location
    start_location['latitude'] += random.uniform(-0.0005 , 0.0005)
    start_location['longitude'] += random.uniform(-0.0005  , 0.0005)
     
    return start_location
    
    
    
    

def generate_vehicle_data(device_id):
     location = simulate_vehicle_movement()
     return {
        'id': uuid.uuid4() ,
        'deviceId': device_id ,
        'timestamp': get_next_time().isoformat(),
        'location': (location['latitude'] , location['longitude'] ) , 
        'speed': random.uniform(10,40) , 
        'direction' : 'North-East' ,
        'make': 'Range-Rover' , 
        'model': 'Evoque',
        'year': 2020,
        'fuelEfficiency': 15,
        'fuelLevel': random.uniform(0, 100),
        'fuelType': 'Diesel',
     }
     
def json_serializer(obj):
    if isinstance(obj, uuid.UUID):
        return obj.isoformat()
    raise TypeError(f'Object of type {type(obj).__name__} cannot be serialized')

def delivery_report(err,msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')
    
def produce_data_to_kafka(producer,topic,data) : 
    producer.produce(
        topic, 
        key=str(data['id']),
        value=json.dumps(data,default=json_serializer).encode('utf-8') ,
        on_delivery=delivery_report )
    producer.flush()
        
         
     
        


def simulate_journey(producer , device_id):
    while True:
        vehicle_data = generate_vehicle_data(device_id)
       # print(vehicle_data)
      #  break
        gps_data = generate_gps_data(device_id , vehicle_data['timestamp'])
        trafffic_camera_data = generate_traffic_camera_data(device_id, vehicle_data['timestamp'], location='location1' ,camera_id='camera1' )
        weather_data = generate_weather_data(device_id, vehicle_data['timestamp' ], vehicle_data['location'])
        emegency_incident_data = generate_emergency_incident_data(device_id, vehicle_data['timestamp'], vehicle_data['location'] )
        
        
        if (vehicle_data['location'][0] >= BIRMINGHAM_COORDINATES['latitude']
               and vehicle_data['location'][1] <= BIRMINGHAM_COORDINATES['longitude'] ): 
                   print('Vehicle has reached Birmingham. Simulation ending')
                         
        
        
        produce_data_to_kafka(producer, VEHICLE_TOPIC,vehicle_data)
        produce_data_to_kafka(producer, GPS_TOPIC,gps_data)
        produce_data_to_kafka(producer, TRAFFIC_TOPIC,trafffic_camera_data)
        produce_data_to_kafka(producer, WEATHER_TOPIC,weather_data)
        produce_data_to_kafka(producer, EMERGENCY_TOPIC, emegency_incident_data)
        
        time.sleep(4)

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
        