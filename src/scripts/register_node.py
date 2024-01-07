import sys
from lib.hostutils import load_hosts, save_hosts, save_key, remote_command, remote_copy, get_key_path
import subprocess as sp

if __name__=="__main__":
	if len(sys.argv) != 8:
		sys.stderr.write(f"Incorrect usage\n")
		exit(1)
	
	host = ""
	username = ""
	key_path = ""
	node_name = ""

	i = 1
	while i < len(sys.argv):
		match sys.argv[i]:
			case "--host":
				host = sys.argv[i+1]
				i += 1
			case "--username":
				username = sys.argv[i+1]
				i += 1
			case "--key":
				key_path = sys.argv[i+1]
				i += 1
			case default:
				node_name = sys.argv[i]
		i += 1

	# Test connection
	return_code, _, stderr = remote_command(
		username = username,
		host = host,
		key = key_path,
		command = "exit"
		)

	if return_code != 0:
		sys.stderr.write(stderr)
		exit(1)
	
	hosts = load_hosts()
	hosts[node_name] = {
		"host": host,
		"username": username,
		"instances": []
	}
	
	save_key(name=node_name, key=key_path)
	save_hosts(hosts)

	# Upload scripts
	return_code, stdout, stderr = remote_command(
		username = username,
		host = host,
		key = get_key_path(node_name),
		command = "mkdir .deploybox"
	)
	
	if return_code != 0:
		sys.stderr.write(stderr)
		#exit(1)
	sys.stdout.write(stdout)

	return_code, stdout, stderr = remote_copy(
		username = username,
		host = host,
		key = get_key_path(node_name),
		src = "scripts/node_scripts",
		dest = ".deploybox"
	)

	if return_code != 0:
		sys.stderr.write(stderr)
		exit(1)
	sys.stdout.write(stdout)

	sys.stdout.write(f"Node '{host}' registered successfully.\n")
