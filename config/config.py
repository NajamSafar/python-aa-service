from configparser import ConfigParser

env = ConfigParser()
env.read('config/env.ini')

def get_env(section, option, msg) -> str: 
    if env.has_option(section, option):
        return env[section][option] 
    else:
        raise Exception(msg)
