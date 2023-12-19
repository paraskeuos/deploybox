import sys
from lib.hostutils import load_hosts, save_hosts, save_key
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
	cmd = f"ssh -o StrictHostKeyChecking=no -o PasswordAuthentication=no -i {key_path} {username}@{host} exit"
	proc = sp.Popen(cmd, shell=True, stdout=sp.PIPE, stderr=sp.PIPE)
	_, stderr = proc.communicate()
	if proc.returncode != 0:
		sys.stderr.write(stderr.decode())
		exit(1)
	
	hosts = load_hosts()
	hosts[node_name] = {
		"host": host,
		"username": username,
		"instances": []
	}
	
	save_key(name=node_name, key=key_path)
	save_hosts(hosts)
