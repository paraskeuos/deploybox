import sys
from lib.hostutils import load_hosts, remote_command, get_key_path

if __name__ == "__main__":
	if len(sys.argv) != 2:
		sys.stderr.write("Incorrect usage\n")
		exit(1)
	
	hosts = load_hosts()
	if sys.argv[1] not in hosts:
		sys.stderr.write(f"Could not find host with name '{sys.argv[1]}'\n")
		exit(1)

	host = hosts[sys.argv[1]]
	return_code, _, stderr = remote_command(
		username = host["username"],
		host = host["host"],
		key = get_key_path(sys.argv[1]),
		command = "exit"
		)

	if return_code != 0:
		sys.stderr.write(stderr)
		exit(1)
	
	sys.stdout.write(f"Connection to host '{sys.argv[1]}' successful.\n")
