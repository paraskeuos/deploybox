import sys
from lib.hostutils import load_hosts, save_hosts

if __name__ == "__main__":
	if len(sys.argv) != 2:
		sys.stderr.write("Incorrect usage.\n")
		exit(1)

	hosts = load_hosts()
	if sys.argv[1] not in hosts.keys():
		sys.stderr.write(f"Could not find node with name '{sys.argv[1]}'.\n")
		exit(1)
