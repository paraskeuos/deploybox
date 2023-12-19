import sys
from lib.hostutils import load_hosts

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
	
	hosts = load_hosts()
