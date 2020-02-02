import argparse
import logging
logger = logging.getLogger('root')

def arg_parser():
    # Defaults
    config = {}
    config["port"] = 5000
    # Parsing
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--port", help="Set custom port (default 5000)")
    parser.add_argument("-d", "--homepath", help="Set custom home dir", required=True)
    args = parser.parse_args()
    config["path"] = args.homepath
    logger.debug("Home dir is changed to " + config["path"])
    if args.port:
        config["port"] = args.port
        logger.debug("Port is changed to " + config["port"])
    return config
    
