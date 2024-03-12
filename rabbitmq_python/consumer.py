import json
from rabbit_connection import Connection



class RabbitMQConsumer:
    def start_process(self, channel, basic_deliver, basic_properties,body: bytes):
        msg = json.loads(body)
        print(f"Consumed incoming message: {msg}")
        channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)



if __name__=='__main__':
    channel = Connection().get_channel()
    channel.queue_declare(queue="dlq_my_test_queue", durable=True)
    channel.queue_declare(queue="my_test_queue", durable=True)
    channel.basic_qos(prefetch_count=1)
    consumer = RabbitMQConsumer()
    channel.basic_consume(queue="my_test_queue", on_message_callback=consumer.start_process, \
    auto_ack=False) 
    print('Started Consuming')
    channel.start_consuming()
    channel.close()    
