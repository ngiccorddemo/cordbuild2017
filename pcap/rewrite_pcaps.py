#!/usr/bin/env python

import argparse
import socket

from scapy.all import UDP, IP, Ether, conf, atol, srp1, ARP, \
    get_if_hwaddr, ConditionalField, Packet, SetGen
from scapy.utils import rdpcap, wrpcap
from scapy.contrib import gtp_v2  # This is used. Lint lies.


class host(object):
    """host class just for argparse"""

    def __init__(self, addr):
        try:
            self.addr = socket.gethostbyname(addr)
        except:
            raise ValueError


def checksum_silent(p):
    """
    Recalcs checksum (like show2) without prints
    Somehow it seems Scapy currently lacks this feature.
    """
    for f in p.fields_desc:
        if isinstance(f, ConditionalField) and not f._evalcond(p):
            continue
        fvalue = p.getfieldval(f.name)
        if isinstance(fvalue, Packet) or \
                (f.islist and f.holds_packets and isinstance(fvalue, list)):
            SetGen(fvalue, _iterpacket=0)
    if p.payload:
        checksum_silent(p.payload)


def send_pkts(args, rewriteinfo):
    """Replays the pcap after rewriting with supplied details"""

    proto, iface, ethsrc, ethdst, ipsrc, ipdst = rewriteinfo

    pkts = rdpcap('{}.pcap'.format(proto))
    for p in pkts:

        # Update Ether common for all proto
        p.getlayer(Ether).src = ethsrc
        p.getlayer(Ether).dst = ethdst

        # Update IP for s11 and s1u
        if proto in ['s11', 's1u']:
            del p[IP].chksum
            del p[UDP].chksum

            p.getlayer(IP).src = ipsrc
            p.getlayer(IP).dst = ipdst
            if proto == 's11':
                # Update s11 MME GTPC IP for Create Session
                if p.getlayer(UDP).gtp_type == 32:
                    p.getlayer(UDP).IE_list[8].ipv4 = ipsrc
                # Update s11 MME GTPC IP and s1u ENB GTPU IP for Modify Bearer
                if p.getlayer(UDP).gtp_type == 34:
                    p.getlayer(UDP).IE_list[0][2].ipv4 = args.s1u.addr
                    p.getlayer(UDP).IE_list[1].ipv4 = ipsrc

            checksum_silent(p)

    wrpcap('tosend-{}.pcap'.format(proto), pkts)


def main(args, proto, host):
    """Main fn"""

    # Currently we work with directly connected subnets
    for net, mask, gwy, iface, saddr in conf.route.routes:
        if atol(host.addr) & mask == net and gwy == '0.0.0.0':

            # ARP ping the IP to find the dst.MAC
            arpres = srp1(Ether(dst='ff:ff:ff:ff:ff:ff') / ARP(pdst=host.addr),
                          iface=iface, verbose=0, timeout=0.1, retry=10)
            if arpres is None:
                print 'Host {} is not yet up. Retry later'.format(host.addr)
                return

            rewriteinfo = (proto, iface, get_if_hwaddr(iface), arpres[Ether].src,
                           saddr, host.addr)
            send_pkts(args, rewriteinfo)
            return
    print 'Host {} does not belong to directly conencted subnet'.format(host.addr)


if __name__ == "__main__":

    # Args handling
    parser = argparse.ArgumentParser(epilog="Ex: ./rewrite_pcaps.py \
                      spgw.s11.ngic spgw.s1u.ngic spgw.sgi.ngic")
    parser.add_argument("s11", type=host, help="s11 target IP or name")
    parser.add_argument("s1u", type=host, help="s1u target IP or name")
    parser.add_argument("sgi", type=host, help="sgi target IP or name")
    args = parser.parse_args()

    for arg in vars(args):
        print arg
        main(args, arg, getattr(args, arg))
