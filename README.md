# Containernet CLOS Topology Generator

## Project Description
This project aims to leverage Containernet, a fork of the renowned Mininet network emulator, to facilitate the creation of SDN network topologies using Docker containers as hosts. By harnessing the capabilities of Containernet, developers can explore a wide range of networking and cloud emulation scenarios while benefitting from the flexibility and scalability of Docker containers. <br>

The script is used to create a Campus LAN topology with docker hosts.

## Usage
### Step 1: Setup Containernet
Refer to this guide [here](https://containernet.github.io/), to do a bare-metal installation in Ubuntu-20.04 LTS

### Step 2: Bring up ONOS (SDN Controller)
This project uses ONOS version 2.7.0 LTS.

### Step 3: Configure the script 
1. Find this line in the script and replace the controller-IP <br> 
`net.addController('c0', switch=OVSKernelSwitch, controller=RemoteController, ip='controller-IP', port=6653)` 

2. Build a Ubuntu Docker Image <br>
Refer to my other repository [here](https://github.com/vikki8/real_life_traffic_generator), to create a custom Ubuntu image with a real-life traffic generator


### Step 4: Run the script
Required Arguments:
```
 -a --access 	        Number of Access Layer Switches 

 -d --distribution    Number of Distribution Layer Switches

 -bwa --bandwidthaccess 	       Access Layer Bandwidth 

 -bwd --bandwidthdistribution    Distribution Layer Bandwidth

 -ho --host              Number of Docker Hosts  

```

Optional Arguments:
```
-c --core 	          Number of Core Layer Switches

-bwc --bandwidthcore 	         Core Layer Bandwidth
```

Example: <br>
`sudo python3 docker_topology.py -a 4 -bwa 10 -d 2 -bwd 20 -c 2 -bwc 30 -ho 4` 

## License
This project is licensed under Mininet 2.3.1b1 License
