import json
from datetime import datetime
import pika

from rabbit_connection import Connection

class RabbitMQPublisher:
    def __init__(self, connection = Connection()) -> None:
        self.__conn = connection

    def __del__(self):
        self.__conn.close()

    def publish(self):
        msg = {"message": f"this is my transient message sent at time - {datetime.utcnow()}"}
        print(f"sending message: {msg}")
        try:
            self.__conn.get_channel().basic_publish(
                exchange='', 
                routing_key="my_test_queue", 
                body=json.dumps(msg)
            )   
        except Exception as e:
            print(f"get the exception: {e.args} while publishing message: {msg}")

    def publish_with_persistant_msg(self):
        msg = {"message": f"this is my persistant message sent at time - {datetime.utcnow()}"}
        print(f"sending message: {msg}")        
        try:            
            self.__conn.get_channel().basic_publish(
                exchange='', 
                routing_key="my_test_queue", 
                body=json.dumps(msg),
                properties=pika.BasicProperties(delivery_mode = pika.DeliveryMode.Persistent)
            )   
        except Exception as e:
            print(f"get the exception: {e.args} while publishing message: {msg}")



if __name__=='__main__':
    pub = RabbitMQPublisher()
    for i in range(100):
        pub.publish()
        pub.publish_with_persistant_msg()