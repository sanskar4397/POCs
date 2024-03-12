import json
from datetime import datetime
import pika

from rabbit_connection import Connection

class RabbitMQPublisher:

    def publish(self):
        msg = {"message": f"this is my transient message sent at time - {datetime.utcnow()}"}
        print(f"sending message: {msg}")
        try:
            conn = Connection()
            conn.get_channel().basic_publish(
                exchange='', 
                routing_key="my_test_queue", 
                body=json.dumps(msg)
            )   
            conn.close()
        except Exception as e:
            print(f"get the exception: {e.args} while publishing message: {msg}")

    def publish_with_persistant_msg(self):
        msg = {"message": f"this is my persistant message sent at time - {datetime.utcnow()}"}
        print(f"sending message: {msg}")        
        try:
            conn = Connection()
            conn.get_channel().basic_publish(
                exchange='', 
                routing_key="my_test_queue", 
                body=json.dumps(msg),
                properties=pika.BasicProperties(delivery_mode = pika.DeliveryMode.Persistent)
            )   
            conn.close()
        except Exception as e:
            print(f"get the exception: {e.args} while publishing message: {msg}")



if __name__=='__main__':
    pub = RabbitMQPublisher()
    pub.publish()
    pub.publish_with_persistant_msg()