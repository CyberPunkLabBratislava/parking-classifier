import argparse
import logging
logger = logging.getLogger('root')

def arg_parser():
    # Defaults
    config = {}
    config["port"] = 5000
    config["host"] = "127.0.0.1"
    config["path"] = "."
    # Parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="Set custom port (default 5000)")
    parser.add_argument("-u", "--host", help="Set custom home dir")
    parser.add_argument("-d", "--homepath", help="Set custom home dir")
    args = parser.parse_args()
    if args.homepath:
        config["path"] = args.homepath
        logger.debug("Home dir is changed to " + config["path"])
    if args.port:
        config["port"] = args.port
        logger.debug("Port is changed to " + config["port"])
    if args.host:
        config["host"] = args.host
        logger.debug("Host is changed to " + config["host"])
    return config
    
