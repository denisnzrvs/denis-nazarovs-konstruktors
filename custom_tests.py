from configparser import ConfigParser
from worker_2_db import *

# Opening the configuration file
config = ConfigParser()
config.read('config.ini')

#Custom config and worker tests
print("Custom tests made by Denis Nazarovs")
print("-----------------------------------")

# Checking if Twitter related options are present in the config file
print("Checking if config has Twitter related options -->")
assert config.has_option('twitter', 'consumer_key') == True
assert config.has_option('twitter', 'consumer_secret') == True
assert config.has_option('twitter', 'access_token') == True
assert config.has_option('twitter', 'access_token_secret') == True
print("OK")
print("----------")

# Testing when providing not a list
print("Testing worker when providing not a list into sort_ast_by_pass_dist([]) -->")

print("Data is a string -->")
data = "Just an example string" #data is string
assert sort_ast_by_pass_dist(data) == []
print("OK");
print("Data is a number -->")
data = 123  #data is number
assert sort_ast_by_pass_dist(data) == []
print("OK")
print("----------")

print("CUSTOM TESTS ALL OK")