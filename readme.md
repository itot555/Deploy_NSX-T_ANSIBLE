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

* Install sshpass:

```
apt-get install sshpass
```

Check:

```
sshpass -V
```

* Install jq:

Download jq from https://stedolan.github.io/jq/.

```
mv jq-linux64 /usr/bin/jq
chmod +x /usr/bin/jq
```

Check:
```
jq
```

# Deploy and Configure NSX-T

## step 1: Install NSX


Customize file named 'install_nsx.env' with your environment attributes:
```
# Location of OVA files
export NSX_MANAGER_OVA_FILE=/DATA/BINARIES/NSX-T-2-0-0/nsx-unified-appliance-2.0.0.0.0.6522097.ova
export NSX_CONTROLLER_OVA_FILE=/DATA/BINARIES/NSX-T-2-0-0/nsx-controller-2.0.0.0.0.6522091.ova
export NSX_EDGE_OVA_FILE=/DATA/BINARIES/NSX-T-2-0-0/nsx-edge-2.0.0.0.0.6522113.ova

# VM names on vCenter
export NSX_MANAGER_NAME=NSX-T_manager
export NSX_CONTROLLER_NAME=NSX-T_controller
export NSX_EDGE_NAME=NSX-T_edge

# vCenter attributes
export VCENTER_IP=10.40.206.61
export VCENTER_USERNAME="administrator@vsphere.local"
export VCENTER_PASSWORD="VMware1!"

# vCenter DC name
export NSX_HOST_COMMON_DATACENTER=Datacenter

# Compute Cluster (for NSX Edge VM)
export NSX_HOST_COMPUTE_CLUSTER=COMP-Cluster-1
export NSX_HOST_COMPUTE_DATASTORE=NFS-LAB-DATASTORE

# Management Cluster (for NSX Manager and NSX Controller)
export NSX_HOST_MGMT_CLUSTER=MGMT-Cluster
export NSX_HOST_MGMT_DATASTORE=NFS-LAB-DATASTORE

# Network0: MGMT port-group
# Network1: Edge VTEP port-group
# Network2: Edge Uplink port-group
export NSX_HOST_COMMON_NETWORK0=CNA-VM
export NSX_HOST_COMMON_NETWORK1=NSX-VTEP-PG
export NSX_HOST_COMMON_NETWORK2=CNA-INFRA
export NSX_HOST_COMMON_NETWORK3=CNA-INFRA

# NSX Manager, Controller, Edge Network Attributes
export NSX_MANAGER_IP=10.40.207.33
export NSX_CONTROLLER_IP=10.40.207.34
export NSX_EDGE_IP=10.40.207.35
export NSX_COMMON_PASSWORD="VMware1!"
export NSX_COMMON_DOMAIN="nsx.vmware.com"
export NSX_COMMON_NETMASK=255.255.255.0
export NSX_COMMON_GATEWAY=10.40.207.253
export NSX_COMMON_DNS=10.20.20.1
export NSX_COMMON_NTP=10.113.60.176
```

Source it:
```
source install_nsx.env
```

Then run the first script:
```
./1-install_nsx.sh
```


## Step 2: Activate NSX cluster

Make sure NSX Manager, NSX Controller and NSX Edge are up and running before moving forward.

Run the second script:
```
./2-enable_nsx_cluster.sh
```


## Step 3: Configure NSX

Customize file named 'configure_nsx.env' with your environment attributes:
```
export NETWORK_TUNNEL_IP_POOL_CIDR="192.168.150.0/24"
export NETWORK_TUNNEL_IP_POOL_ALLOCATION_START="192.168.150.200"
export NETWORK_TUNNEL_IP_POOL_ALLOCATION_END="192.168.150.250"
export NETWORK_T0_SUBNET_IP_ADDRESS="10.40.206.20"
export NETWORK_T0_SUBNET_PREFIX_LENGTH=25
export NETWORK_T0_GATEWAY="10.40.206.125"
export NETWORK_HOST_UPLINK_PNIC='vmnic1'
```

Source it:
```
source configure_nsx.env
```

Then run the third script:
```
3-configure_nsx.sh
```

## END

