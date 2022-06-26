import configparser


# Method to read config file settings
import os


def read_config(path):
    config = configparser.ConfigParser()
    config.read(path)
    return config


def write_new_config(section, value):
    config_object = configparser.ConfigParser()
    config_object[section] = value
    with open('config.ini', 'w') as conf:
        config_object.write(conf)
