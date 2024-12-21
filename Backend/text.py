import configparser

def load_config():
    config = configparser.ConfigParser()
    config.read('data.ini')
    return config

config = load_config()

text_data = {
    'key1': config['INDEX']['key1'],
    'key2': config['INDEX']['key2'],
    'key3': config['INDEX']['key3'],
    'key4': config['INDEX']['key4'],
    'version': config['INDEX']['version']
}