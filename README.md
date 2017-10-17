# Deploy-NSX-T using ANSIBLE: 
# Automatically deploy and configure NSX-T (for Lab environment)

This project contains ANSIBLE playbooks to automatically Install and Configure NSX-T (any version of NSX-T).


Playbooks are:
* 1-install_nsx.yaml
* 2-activate_nsx_cluster.yaml
* 3-configure_nsx.yaml

A final playbook 'all-install_activate_configure_nsx.yaml' uses the aboves playbooks in sequence.
You have the choice to either launch each playbook one after the other (advantage is to check all steps) - or - launch the 
'all-install_activate_configure_nsx.yaml' playbook that will automate all sequences.


#### 1-install_nsx.yaml
Creates the following NSX-T components:
* 1 NSX Manager (NSX Manager will be instantiated in the MGMT cluster)
* 1 NSX Controller (NSX Controller will be instantiated in the MGMT cluster) [option to set to 3 Controllers]
* 1 NSX Edge ((NSX Edge will be instantiated in the COMPUTE cluster)

#### 2-activate_nsx_cluster.yaml
* Form NSX-T cluster (NSX Controller and NSX Edge will be registered with NSX Manager)

#### 3-configure_nsx.yaml
Create following NSX-T objects:
* Creating VLAN transport zone
* Creating OVERLAY transport zone
* Creating uplink profile
* Creating IP address pool
* Configuring Edge transport node
* Creating Edge cluster
* Creating T0 router
* Creating logical switch
* Creating logical port
* Creating router port
* Adding static route
* Creating T1 router



## System requirements
To run these scripts, you need:
* 1 ANSIBLE Control Server VM (Ubuntu tested here)
* OVFtool installed on the VM

Note: you can use you MAC laptop as well.

## Lab requirements
NSX-T will be deployed in the lab with the following config:
* 1 MGMT cluster (will host NSX Manager and NSX Controller)
* 1 COMPUTE cluster (will host NSX Edge)

## OVA bits
It's up to the user to download all NSX OVA bits (from vmware.com for instance).
location of NSX Manager, NSX Controller and NSX Edge OVA files will then be provided to env vars in file install_nsx.env. 


## Install ANSIBLE Control Server
* Install Ubuntu (16.04 used here)

* Install ANSIBLE:

```
apt-get update
apt-get install software-properties-common
apt-add-repository ppa:ansible/ansible
apt-get update
apt-get install ansible
```

* Install OVFtool:

Download bundle from vmware.com (for instance VMware-ovftool-4.2.0-4586971-lin.x86_64.bundle)

```
chmod +x VMware-ovftool-4.2.0-4586971-lin.x86_64.bundle
./VMware-ovftool-4.2.0-4586971-lin.x86_64.bundle
```

Check:

```
ovftool -v
```


## Prepare ANSIBLE Control Server
the playbooks needs some additional Python modules to operate.

Install and Upgrapde pip:

```
apt install python-pip
pip install --upgrade pip
```
 
Install requested Python modules:

```
pip install requests
pip install pyVim
pip install pyOpenSSL
pip install pyvmomi
```

Check:
```
pip list
```
You should be able to see:
ansible (2.4.0.0)
asn1crypto (0.23.0)
certifi (2017.7.27.1)
cffi (1.11.2)
chardet (3.0.4)
cryptography (2.1.1)
docopt (0.6.2)
ecdsa (0.13)
enum34 (1.1.2)
httplib2 (0.9.1)
idna (2.6)
ipaddress (1.0.16)
Jinja2 (2.8)
MarkupSafe (0.23)
paramiko (1.16.0)
pip (9.0.1)
prompt-toolkit (1.0.15)
pyasn1 (0.1.9)
pycparser (2.18)
pycrypto (2.6.1)
pyflakes (1.6.0)
Pygments (2.2.0)
pyOpenSSL (17.3.0)
pyvim (0.0.21)
pyvmomi (6.5.0.2017.5.post1)
PyYAML (3.11)
requests (2.18.4)
setuptools (20.7.0)
six (1.10.0)
urllib3 (1.22)
wcwidth (0.1.7)
wheel (0.29.0)


# Deploy and Configure NSX-T

## step 1: Install NSX


Customize file named 'hosts' with your environment attributes:
```
[localhost]
localhost       ansible_connection=local ansible_become_pass=VMware1!


[nsx-managers]
nsx-manager 		ansible_ssh_host=10.40.207.33		ansible_ssh_user=root ansible_ssh_pass=VMware1!

[nsx-controllers]
nsx-controller01	ansible_ssh_host=10.40.207.34		ansible_ssh_user=root ansible_ssh_pass=VMware1!

[nsx-edges]
nsx-edge		ansible_ssh_host=10.40.207.35		ansible_ssh_user=root ansible_ssh_pass=VMware1!

[nsxtransportnodes]
esx1        ansible_ssh_host=192.168.110.54        ansible_ssh_user=root ansible_ssh_pass=VMware1!
esx2        ansible_ssh_host=192.168.110.55        ansible_ssh_user=root ansible_ssh_pass=VMware1!

[all:vars]
number_of_controllers='1'
```

Customize file named 'answerfile.yml' with your environment attributes:

```
ovfToolPath: '/usr/bin'
deployDataCenterName: 'Datacenter'

deployMgmtPortGroup: 'CNA-VM'

deployClusterMgmt: 'MGMT-Cluster'
deployDatastoreMgmt: 'NFS-LAB-DATASTORE'

deployClusterComp: 'COMP-Cluster-1'
deployDatastoreComp: 'NFS-LAB-DATASTORE'

deployMgmtDnsServer: '10.20.20.1'
deployNtpServers: '10.113.60.176'
deployMgmtDnsDomain: 'corp.local'
deployMgmtDefaultGateway: '10.40.207.253'
deployMgmtNetmask: '255.255.255.0'
nsxAdminPass: 'VMware1!'
nsxCliPass: 'VMware1!'
nsxOvaPath: '/DATA/BINARIES/NSX-T-2-0-0/'
deployVcIPAddress: '10.40.206.61'
deployVcUser: 'administrator@vsphere.local'
deployVcPassword: 'VMware1!'
sshEnabled: True
allowSSHRootAccess: True

nodes:
  nsxMan:
    hostname: 'nsx-man.corp.local'
    vmName: 'NSX-T Manager 01'
    ipAddress: '10.40.207.33'
    ovaFile: 'nsx-unified-appliance-2.0.0.0.0.6522097.ova'
  nsxController01:
    hostname: 'controller1.corp.local'
    vmName: 'NSX-T Controller 01'
    ipAddress: '10.40.207.34'
    ovaFile: 'nsx-controller-2.0.0.0.0.6522091.ova'
  nsxEdge:
    hostname: 'edge.corp.local'
    vmName: 'NSX-T Edge 01'
    ipAddress: '10.40.207.35'
    ovaFile: 'nsx-edge-2.0.0.0.0.6522113.ova'
    portgroupExt: 'CNA-INFRA'
    portgroupTransport: 'CNA-INFRA'

controllerClusterPass: 'VMware1!'

api_origin: 'localhost'

ippool:
  name: 'tep-ip-pool'
  cidr: '192.168.213.0/24'
  gw: '192.168.213.1'
  start: '192.168.213.10'
  end: '192.168.213.200'


transportZoneName: 'tz1'
hostSwitchName: 'hostswitch1'
tzType: 'OVERLAY'
transport_vlan: '0'

t0:
  name: 'DefaultToRouter'
#  ha: 'ACTIVE_ACTIVE'
  ha: 'ACTIVE_STANDBY'
```


Then run the first playbook:
```
ansible-playbook ./1-install_nsx.sh
```


## Step 2: Activate NSX cluster

Make sure NSX Manager, NSX Controller and NSX Edge are up and running before moving forward.

Run the second playbook:
```
ansible-playbook ./2-enable_nsx_cluster.sh
```


## Step 3: Configure NSX

Run the third playbook:
```
ansible-playbook ./3-configure_nsx.sh
```

## END

