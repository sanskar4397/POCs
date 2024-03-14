import json
from random import randint
from rabbit_connection import Connection
from pika.exchange_type import ExchangeType
from pika.adapters.blocking_connection import BlockingChannel


class RabbitMQConsumer:
    def start_process(self, channel: BlockingChannel, basic_deliver, basic_properties,body: bytes):
        msg = json.loads(body)
        num = randint(0, 9)
        if num % 2 == 0:
            print(f"Consumed incoming message: {msg}")
            channel.basic_ack(delivery_tag=basic_deliver.delivery_tag)
        else:
            print(f"sent to dlq incoming message: {msg}")
            channel.basic_nack(delivery_tag=basic_deliver.delivery_tag, requeue=False)



if __name__=='__main__':
    DLQ = "dlq_my_test_queue"
    DLX = "dlx_exchange"
    Q = "my_test_queue"
    arguments={
        "x-dead-letter-routing-key": DLQ,
        "x-dead-letter-exchange": DLX,
    }
    channel = Connection().get_channel()

    #add dl-exchange
    ex = channel.exchange_declare(DLX, ExchangeType.direct)

    #DLQ queue declare and bind with exchange
    dlq = channel.queue_declare(queue=DLQ, durable=True, )
    channel.queue_bind(dlq.method.queue, DLX, dlq.method.queue)

    # Main queue declare 
    q = channel.queue_declare(queue=Q, durable=True, arguments=arguments)

    channel.basic_qos(prefetch_count=1)
    consumer = RabbitMQConsumer()
    channel.basic_consume(queue=Q, on_message_callback=consumer.start_process, \
    auto_ack=False) 
    print('Started Consuming')
    channel.start_consuming()
    channel.close()    
