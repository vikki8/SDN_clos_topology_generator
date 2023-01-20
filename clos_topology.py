import json

from mininet.topo import Topo
from mininet.link import TCLink
import os


class MyTopo(Topo):
    def __init__(self):
        # Initialize topology
        Topo.__init__(self)

        bw1 = 1
        bw2 = 10

        h = []
        spine = []
        leaf = []

        d1 = {"app_metric": []}

        for i in range(1, 11):
            h.append(self.addHost(f'h{i}'))
        for i in range(1, 3):
            spine.append(self.addSwitch(f's{i}'))
        for i in range(1+len(spine), 5+len(spine)):
            leaf.append(self.addSwitch(f's{i}'))

        # Add links
        for i in range(len(spine)):
            for j in range(len(leaf)):
                self.addLink(spine[i], leaf[j], cls=TCLink, bw=bw2)

        # --------------------------------
        count = 0
        port = len(leaf)

        for i in range(len(h)):
            if count == len(leaf):
                port += 1
                count = 0
            self.addLink(leaf[count], h[i], cls=TCLink, bw=bw2)
            count += 1

topos = {'mytopo': (lambda: MyTopo())}
