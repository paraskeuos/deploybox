from os import environ

PROG_DIR = ("/").join([environ["HOME"], ".deploybox"])
DATA_DIR = ("/").join([PROG_DIR, "data"])
KEYS_DIR = ("/").join([PROG_DIR, "keys"])
HOSTS_FILE = ("/").join([DATA_DIR, "hosts.json"])

def load_hosts():
	import os
	import json

	hosts = {}

	# If program dir doesn't exist, initialize it and return empty dict
	if not os.path.isdir(PROG_DIR):
		os.mkdir(PROG_DIR)
		os.mkdir(DATA_DIR)
		os.mkdir(KEYS_DIR)

		with open(HOSTS_FILE, "w") as f:
			json.dump(hosts, f)
	else:
		with open(HOSTS_FILE, "r") as f:
			hosts = json.load(f)

	return hosts

def save_hosts(data):
	import json

	with open(HOSTS_FILE, "w") as f:
		json.dump(data, f)

def get_key_path(name):
	return ("/").join([KEYS_DIR, name])

def save_key(name, key):
	from shutil import copy
	
	copy(key, dst=get_key_path(name))
