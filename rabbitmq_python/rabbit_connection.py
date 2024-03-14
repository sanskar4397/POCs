import time
from pika import PlainCredentials, ConnectionParameters, BlockingConnection, exceptions
from pika.adapters.blocking_connection import BlockingChannel
class Connection:
    __connection = None
    
    def __create(self):
        host = "rabbitmq"
        port = 5672
        password= "guest"
        username = "guest"
        retries=0
        while retries < 10:
            try:
                credentials = PlainCredentials(username, password)
                parameters = ConnectionParameters(host=host, port=port, credentials=credentials) # NOSONAR
                self.__connection = BlockingConnection(parameters)
                print("Connected to RabbitMQ")
                return
            except exceptions.AMQPConnectionError as e:
                print(f"Failed to connect to RabbitMQ: {e}")
                retries += 1
                wait_time = 3 ** retries
                print(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)

    def get_connection(self):
        if not self.__connection:
            self.__create()
        return self.__connection
    
    def close(self):
        if self.__connection and self.__connection.is_open:
            self.__connection.close()

    def get_channel(self) -> BlockingChannel:
        if not self.__connection or self.__connection.is_closed:
            self.get_connection()
        return self.__connection.channel()
    



    