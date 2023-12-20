from sys
from lib.hostutils import load_hosts

if __name__ == "__main__":
	if len(sys.argv != 2):
		sys.stderr.write("Incorrect usage\n")
		exit(1)
	
	hosts = load_hosts()
	if sys.argv[1] not in hosts:
		sys.stderr.write(f"Could not find host with name '{sys.argv[1]}'\n")
		exit(1)
	

