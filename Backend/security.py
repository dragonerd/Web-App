import configparser

def load_config():
    config = configparser.ConfigParser()
    config.read('data.ini')
    return config

config = load_config()

max_attempts = int(config['security']['max_attempts'])
