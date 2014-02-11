import logging
import yaml

def load_data(world_name, data_name):
    try:
        full_path = "worlds/" + world_name + "/" + data_name + ".yaml"
        with open(full_path) as file_data:
            logging.info("Loading file " + full_path)
            return yaml.load(file_data)
    except IOError:
        return None

def save_data(world_name, data_name, obj):
    full_path = "worlds/" + world_name + "/" + data_name + ".yaml"
    with open(full_path, 'w') as file_data:
        logging.info("Saving file " + full_path)
        yaml.dump(obj, file_data)
