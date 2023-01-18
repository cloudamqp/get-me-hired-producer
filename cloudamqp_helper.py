import os,json

import pika
# from pika.exchange_type import ExchangeType
from dotenv import load_dotenv


# Load the .env file
load_dotenv()


class CloudAMQPHelper:
    """ The interface between this project and CloudAMQP """

    EXCHANGE = "get_me_hired_exchange"
    EXCHANGE_TYPE = "direct"
    QUEUE_NAME = "get_me_hired_queue"
    ROUTING_KEY = "jobs_search"
    
    def __init__(self) -> None:
        """ Sets up a connection and a channel when this class is instantiated """

        url = os.environ["CLOUDAMQP_URL"]
        params = pika.URLParameters(url)

        self.__connection = pika.BlockingConnection(params) # Connect to CloudAMQP
    
    def __create_channel(self) -> pika.BlockingConnection:
        channel = self.__connection.channel() # start a channel
        return channel
        
    async def __create_exchanges_queues(self) -> None:
        """ Declares a queue and an exchnage using the channel created """
        # Get channel
        channel = self.__create_channel()
        # Create an exchange
        channel.exchange_declare(
            exchange=self.EXCHANGE, exchange_type=self.EXCHANGE_TYPE
        )
        # Create a queue
        channel.queue_declare(queue=self.QUEUE_NAME)
        # Bind queue with exchange
        channel.queue_bind(
            self.QUEUE_NAME,
            self.EXCHANGE, 
            self.ROUTING_KEY # The routing key here is the binding key
        )

    async def publish_message(self, message_body) -> None:
        """ Publishes a message to CloudAMQP """
        # First declare an exchange and a queue
        await self.__create_exchanges_queues()

        # Get channel
        channel = self.__create_channel()

        channel.basic_publish(
            exchange=self.EXCHANGE, 
            routing_key=self.ROUTING_KEY,
            body=json.dumps(message_body)
        )

        print ("[x] Message sent to consumer")

        self.__connection.close()


# Create an instance
cloudamqp: CloudAMQPHelper = CloudAMQPHelper()

    