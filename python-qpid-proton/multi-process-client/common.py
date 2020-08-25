import optparse
import logging
import math
import os


def generate_message_body(size, pattern) -> str:
    return (pattern * math.ceil(size / len(pattern)))[:size]


def generate_application_properties(size) -> dict:
    props = {}
    props_size = 0
    i = 0
    while props_size < size:
        k = "key-%d" % i
        v = "value-%d" % i
        size_left = size - props_size
        # adding last key to fill the map with the correct size
        if size_left - len(k) - len(v) < 0:
            k = "k"
            v = ""
            while size_left - len(k) - len(v) > 0:
                v += "v"
        props[k] = v
        props_size += len(k) + len(v)
        i += 1
    return props


def initialize_logging(log_level):
    """
    Initialize python logging with default level set to INFO.
    :return:
    """
    logging.basicConfig(level=log_level,
                        format="%(asctime)s - PID:%(process)-10s - LEVEL:%(levelname)-8s - %(message)s")


def parse_opts(is_sender=False):
    # Arguments parsing
    parser = optparse.OptionParser(usage="usage: %prog [options]")
    parser.add_option("--host", default=os.getenv("AMQP_HOST", "0.0.0.0"),
                      help="The AMQP host to connect (or set AMQP_HOST env var)")
    parser.add_option("--port", default=os.getenv("AMQP_PORT", "5672"),
                      help="AMQP port to connect (or set AMQP_PORT env var)")
    address_help = "Address to %s (or set AMQP_ADDRESS env var)" % \
                   "send messages to" if is_sender else "receive messages from"
    parser.add_option("--address", default=os.getenv("AMQP_ADDRESS", "queue1"),
                      help=address_help)
    parser.add_option("--processes", default=os.getenv("CLIENT_PROCESSES", "2"), type=int,
                      help="number of processes to spawn (or set CLIENT_PROCESSES env var)")
    parser.add_option("--message-size", default=os.getenv("CLIENT_MESSAGE_SIZE", "259"), type=int,
                      help="size of message body (or set CLIENT_MESSAGE_SIZE env var)")
    parser.add_option("--properties-size", default=os.getenv("CLIENT_PROPERTIES_SIZE", "512"), type=int,
                      help="size of application properties (or set CLIENT_PROPERTIES_SIZE env var)")
    reconnect_after_help = "after a given number of messages delivered the %s will recycle its connection " \
                           "(or set CLIENT_RECONNECT_AFTER env var)" % "sender" if is_sender else "receiver"
    parser.add_option("--reconnect-after", default=os.getenv("CLIENT_RECONNECT_AFTER", "1000"), type=int,
                      help=reconnect_after_help)
    if is_sender:
        parser.add_option("--interval-delay", default=os.getenv("CLIENT_INTERVAL_DELAY", "4"), type=int,
                          help="delay in seconds between sending cycle (or set CLIENT_INTERVAL_DELAY env var)")
        parser.add_option("--ttl", default=os.getenv("CLIENT_TTL", 30000), type=int,
                          help="ttl in milliseconds (or set CLIENT_TTL env var)")
    parser.add_option("--log-level", default=os.getenv("LOG_LEVEL", "INFO"),
                      help="logging level (or set LOG_LEVEL env var)")
    parsed_opts, args = parser.parse_args()
    return parsed_opts, args
