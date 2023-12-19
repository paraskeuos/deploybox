def load_hosts():
	import os
	import json
	
	prog_dir = ("/").join([os.environ["HOME"], ".deploybox"])
	data_dir = ("/").join([prog_dir, "data"])
	keys_dir = ("/").join([prog_dir, "keys"])
	hosts_file = ("/").join([data_dir, "hosts.json"])

	hosts = {}

	# If program dir doesn't exist, initialize it and return empty dict
	if not os.path.isdir(prog_dir):
		os.mkdir(prog_dir)
		os.mkdir(data_dir)
		os.mkdir(keys_dir)

		with open(hosts_file, "w") as f:
			json.dump(hosts, f)

		return hosts

	# TODO: If hosts file exists, load json and return dict 
	with open(hosts_file, "r") as f:
		json_data = json.load(f)

	for name, host_data in json_data.items():
		# TODO

	return hosts
