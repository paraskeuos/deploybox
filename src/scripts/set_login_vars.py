import sys
from lib.hostutils import load_hosts, get_key_path

if __name__ == "__main__":
	hosts = load_hosts()
	host = hosts[sys.argv[1]]

	sys.stdout.write(f"username=\"{host['username']}\";")
	sys.stdout.write(f"host=\"{host['host']}\";")
	sys.stdout.write(f"key=\"{get_key_path(sys.argv[1])}\";")
