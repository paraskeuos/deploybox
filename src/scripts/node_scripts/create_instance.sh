#!/bin/bash

HOST_NIC="enp30s0"
VM_ARCHIVE_DIR="${HOME}/.deploybox/VM_archives"
VM_EXPORTS_DIR="${HOME}/.deploybox/VM_exports"
VM_BASE_VERSION="ubuntu_22_04_3"
VM_VERSION=1

workdir="${VM_EXPORTS_DIR}/${VM_BASE_VERSION}/${VM_VERSION}"
mkdir -p $workdir 2> /dev/null
#tar -xf ${VM_ARCHIVE_DIR}/${VM_BASE_VERSION}_${VM_VERSION}.tar.gz -C $workdir

VM_ROOT_KEY="${workdir}/init_key"
VM_NETPLAN_CONFIG="00-installer-config.yaml"

VM_NAME="test"
VM_USER="boxdeploy"
VM_NEW_PUBKEY_NAME="${VM_NAME}.pub"

vboxmanage import ${workdir}/${VM_BASE_VERSION}_${VM_VERSION}.ova --vsys 0 --vmname $VM_NAME

# Create temporary hostonlyif and save the name
vboxnet="$(vboxmanage hostonlyif create | sed -E 's/.*(vboxnet[0-9]+).*/\1/')"

host_ip="192.168.56.1"
dhcp_ip="192.168.56.2"
guest_ip="192.168.56.3"

# Set static IP for host on saved hostonlyif
vboxmanage hostonlyif ipconfig $vboxnet --ip $host_ip

# Set up DHCP server for the new hostonlyif
# Lower and higher IP are equal to make the guest IP fixed and known in advance
vboxmanage dhcpserver add --interface $vboxnet --server-ip $dhcp_ip --netmask 255.255.255.0 \
											--lower-ip $guest_ip --upper-ip $guest_ip --enable

# Set the guest to use the new hostonlyif
vboxmanage modifyvm $VM_NAME --nic1 hostonly
vboxmanage modifyvm $VM_NAME --hostonlyadapter1 $vboxnet

# Start guest
vboxmanage startvm $VM_NAME --type headless

# Remote commands as root
ssh_opts="-o StrictHostKeyChecking=no"

echo "Waiting for SSH server to be ready..."
wait_time=10
sleep $wait_time
ssh $ssh_opts -i $VM_ROOT_KEY root@${guest_ip} "exit"
while [ $? -gt 0 ]
do
	echo "Trying again in ${wait_time}s..."
	sleep $wait_time 
	ssh $ssh_opts -i $VM_ROOT_KEY root@${guest_ip} "exit"
done
echo "Instance SSH server is ready - continuing..."
		
# scp netplan .yml file to /etc/netplan
scp $ssh_opts -i $VM_ROOT_KEY $workdir/$VM_NETPLAN_CONFIG root@${guest_ip}:/etc/netplan 


# Set up boxdeploy user's connection with public key
#ssh $ssh_opts -i $VM_ROOT_KEY root@${guest_ip} "mkdir /home/${VM_USER}/.ssh"
scp $ssh_opts -i $VM_ROOT_KEY $workdir/$VM_NEW_PUBKEY_NAME root@${guest_ip}:/home/${VM_USER}/.ssh 
ssh $ssh_opts -i $VM_ROOT_KEY root@${guest_ip} \
	"cat /home/${VM_USER}/.ssh/${VM_NEW_PUBKEY_NAME} > /home/${VM_USER}/.ssh/authorized_keys && \
	 rm /home/${VM_USER}/.ssh/${VM_NEW_PUBKEY_NAME} && \
	 chmod 600 /home/${VM_USER}/.ssh/authorized_keys && \
	 chmod 700 /home/${VM_USER}/.ssh && \
	 chown -R ${VM_USER}:${VM_USER} /home/${VM_USER}/.ssh" 


# Turn off root login in sshd_config, delete root pubkey, netplan apply and restart
# TODO: Currently the command gets executed properly but it gets stuck, therefore the detached mode and killing the process.
#       It should not get stuck after sending remote command
ssh $ssh_opts -i $VM_ROOT_KEY root@${guest_ip} \
	"sleep 3 && \
	 sed -i 's/PermitRootLogin yes/#PermitRootLogin prohibit-password/' /etc/ssh/sshd_config && \
	 rm -rf /root/.ssh && \
     chmod 400 /etc/netplan/${VM_NETPLAN_CONFIG} && \
	 netplan apply && \
	 shutdown now &" &

# Setting up bridged networking...
sleep 10
kill $!

# Wait until the VM is off
echo "Checking if the instance is powered off..."
wait_time=10
sleep $wait_time
vboxmanage showvminfo $VM_NAME | grep -E "State:.*off.*" &> /dev/null
while [ $? -gt 0 ]
do
	echo "The instance is still running. Checking again in ${wait_time}s..."
	sleep $wait_time
	vboxmanage showvminfo $VM_NAME | grep -E "State:.*off.*" &> /dev/null
done

# Set up bridged adapter
vboxmanage modifyvm $VM_NAME --nic1 bridged
vboxmanage modifyvm $VM_NAME --bridgeadapter1 $HOST_NIC

vboxmanage startvm $VM_NAME --type headless

# Remove temporary hostonlyif and DHCP server
vboxmanage dhcpserver remove --interface $vboxnet
vboxmanage hostonlyif remove $vboxnet
