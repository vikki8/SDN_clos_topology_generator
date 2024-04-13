from mininet.net import Containernet
from mininet.node import RemoteController, OVSKernelSwitch
from mininet.cli import CLI
from mininet.link import TCLink
from mininet.log import info, setLogLevel

import argparse

setLogLevel('info')
exec(open("/home/tein/sflow-rt/extras/sflow.py").read())

info('*** Adding controller\n')
net = Containernet(controller=None)
net.addController('c0', switch=OVSKernelSwitch, controller=RemoteController, ip='controller-IP', port=6653)

parser = argparse.ArgumentParser(description="Enterprise Topology Generator")
parser.add_argument('-bwc', '--bandwidthcore', type=int, metavar='', required=False, default=30,
                    help="Core Layer Bandwidth")
parser.add_argument('-bwd', '--bandwidthdistribution', type=int, metavar='', required=False, default=20,
                    help="Distribution Layer Bandwidth")
parser.add_argument('-bwa', '--bandwidthaccess', type=int, metavar='', required=True, default=10,
                    help="Access Layer Bandwidth")
parser.add_argument('-c', '--core', type=int, metavar='', required=False, default=0,
                    help="Number of Core Layer Switches")
parser.add_argument('-d', '--distribution', type=int, metavar='', required=False, default=0,
                    help="Number of Distribution Layer Switches")
parser.add_argument('-a', '--access', type=int, metavar='', required=True, default=1,
                    help="Number of Access Layer Switches")
parser.add_argument('-ho', '--host', type=int, metavar='', required=True, default=20,
                    help="Number of Docker Hosts")

args = parser.parse_args()

bw_access = args.bandwidthaccess
bw_distribution = args.bandwidthdistribution
bw_core = args.bandwidthcore

h = []

info('*** Adding docker containers\n')
for i in range(1, args.host + 1):
    num = hex(i).lstrip("0x")
    if i <= 15:
        num = "0" + num
    h.append(net.addDocker(f'h{i}', mac=f'00:00:00:00:00:{num}', dimage="ubuntu:latest", ipc_mode="shareable",
                           devices=["/dev/net/tun"]))

core = []
distribution = []
access = []

info('*** Adding switches\n')
if args.core > 0:
    for i in range(1, args.core + 1):
        core.append(net.addSwitch(f's{i}', protocols='OpenFlow13'))
if args.distribution > 0:
    for i in range(1 + len(core), 1 + len(core) + args.distribution):
        distribution.append(net.addSwitch(f's{i}', protocols='OpenFlow13'))
for i in range(1 + len(core) + len(distribution), 1 + len(core) + len(distribution) + args.access):
    access.append(net.addSwitch(f's{i}', protocols='OpenFlow13'))

# Add links
info('*** Creating links\n')
if args.core > 0:
    for i in range(len(core)):
        if i + 1 == len(core):
            break
        net.addLink(core[i], core[i + 1], cls=TCLink, bw=bw_core)

    for i in range(len(core)):
        for j in range(len(distribution)):
            net.addLink(core[i], distribution[j], cls=TCLink, bw=bw_distribution)

if args.distribution > 0:
    for i in range(len(distribution)):
        if i + 1 == len(distribution):
            break
        net.addLink(distribution[i], distribution[i + 1], cls=TCLink, bw=bw_distribution)

    for i in range(len(distribution)):
        for j in range(len(access)):
            net.addLink(distribution[i], access[j], cls=TCLink, bw=bw_access)

count = 0
port = len(access)

for i in range(len(h)):
    if count == len(access):
        port += 1
        count = 0
    net.addLink(access[count], h[i], cls=TCLink, bw=bw_access)
    count += 1

info('*** Starting network\n')
net.start()
for i in range(1, args.host + 1):
    net.get(f'h{i}').cmd('service ssh start')

info('*** Testing connectivity\n')
# net.ping([host[0], host[1]])

info('*** Running CLI\n')
CLI(net)

info('*** Stopping network')
net.stop()


