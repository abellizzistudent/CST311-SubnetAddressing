#!/usr/bin/env python

# legacy_network.py
# CST 311: Introduction to Computer Networks
# June 17, 2022
# Programming Assignment #4
# Anna Bellizzi, David Debow, Justin Johnson, Ryan Parker
# Pacific Analytics
# Modified code to create topology of three routers, two switches, and four hosts
# Establishes trace routes and ip addresses
# All components can ping each other

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import CPULimitedHost, Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call
from mininet.term import makeTerm
import time

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/24')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)
 
    info( '*** Add switches\n')
    #move switches ahead
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    
    r3 = net.addHost('r3', cls=Node, ip='10.0.0.3/24')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')

    r4 = net.addHost('r4', cls=Node, ip='192.168.0.2/30')
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    r5 = net.addHost('r5', cls=Node, ip='10.0.1.3/24')
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')
    
    #add link
    #change add link values
    
    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1/24', defaultRoute='via 10.0.0.3')
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2/24', defaultRoute='via 10.0.0.3') 
    h3 = net.addHost('h3', cls=Host, ip='10.0.1.1/24', defaultRoute='via 10.0.1.3')
    h4 = net.addHost('h4', cls=Host, ip='10.0.1.2/24', defaultRoute='via 10.0.1.3')

    info( '*** Add links\n')
    
    net.addLink(s1, h1)
    net.addLink(s1, h2)
    net.addLink(s2, h3)
    net.addLink(s2, h4)
    
    net.addLink(r3, s1, intfName1='r3-eth0', params1={ 'ip' : '10.0.0.3/24' })
    net.addLink(r5, s2, intfName1='r5-eth0', params1={ 'ip' : '10.0.1.3/24' })

    net.addLink( r3, r4, intfName1='r3-eth1', params1={ 'ip' : '192.168.0.1/30' }, intfName2='r4-eth0', params2={ 'ip' : '192.168.0.2/30' }, )
    net.addLink( r5, r4, intfName1='r5-eth1', params1={ 'ip' : '192.168.1.1/30' }, intfName2='r4-eth1', params2={ 'ip' : '192.168.1.2/30' }, )

    info( '*** Starting network\n')
    net.build()
    
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s2').start([c0])
    net.get('s1').start([c0])
    
    info( '*** Post configure switches and hosts\n')
    
    r3.cmd('sudo ip route add 10.0.1.0/24 via 192.168.0.2 dev r3-eth1')
    r3.cmd('sudo ip route add 192.168.1.0/30 via 192.168.0.2 dev r3-eth1')
    r4.cmd('sudo ip route add 10.0.0.0/24 via 192.168.0.1 dev r4-eth0')
    r4.cmd('sudo ip route add 10.0.1.0/24 via 192.168.1.1 dev r4-eth1')
    r5.cmd('sudo ip route add 192.168.0.0/30 via 192.168.1.2 dev r5-eth1')
    r5.cmd('sudo ip route add 10.0.0.0/24 via 192.168.1.2 dev r5-eth1')
    
    info('r3 \n')
    info( net[ 'r3' ].cmd( 'route' ) )
    info('r4 \n')
    info( net[ 'r4' ].cmd( 'route' ) )
    info('r5 \n')
    info( net[ 'r5' ].cmd( 'route' ) )
    
    # makeTerm( h1, title='h1', term='xterm', display='Yes', cmd='python3 hello.py' )
    #makeTerm( h1, title='h1', term='xterm', display=None, cmd='bash')
    #makeTerm( h2, title='h2', term='xterm', display=None, cmd='bash')
    #makeTerm( h3, title='h3', term='xterm', display=None, cmd='bash')
    
    makeTerm( h1, title='h1', term='xterm', display=None, cmd='sudo python3 ~/CST311/PA4/chatServer.py')
    time.sleep(1)
    makeTerm( h2, title='h2', term='xterm', display=None, cmd='sudo python3 ~/CST311/PA4/chatClient.py')
    #makeTerm( h2, title='h2', term='xterm', display=None, cmd='bash')
    time.sleep(1)
    makeTerm( h3, title='h3', term='xterm', display=None, cmd='sudo python3 ~/CST311/PA4/chatClient.py')
    #makeTerm( h3, title='h3', term='xterm', display=None, cmd='bash')
    
    CLI(net)
    net.stop()

#add Kernel IP Routing Table / not working
def run():
    "Test linux router"
    topo = myNetwork()
    net = Mininet( topo=topo, waitConnected=True )  # controller is used by s1-s3
    net.start()

if __name__ == '__main__':
    setLogLevel( 'info' )
    run()
    

