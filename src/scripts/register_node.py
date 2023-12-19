import sys

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
				print(f"Host: {host}")
			case "--username":
				username = sys.argv[i+1]
				i += 1
				print(f"Username: {username}")
			case "--key":
				key_path = sys.argv[i+1]
				i += 1
				print(f"Key: {key_path}")
			case default:
				node_name = sys.argv[i]
				print(f"Name: {node_name}")
		i += 1
	
	print(host, username, key_path, node_name)
			
