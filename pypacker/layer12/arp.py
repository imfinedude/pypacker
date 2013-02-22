"""Address Resolution Protocol."""

from .. import pypacker
# Hardware address format
ARP_HRD_ETH	= 0x0001	# ethernet hardware
ARP_HRD_IEEE802	= 0x0006	# IEEE 802 hardware

# Protocol address format
ARP_PRO_IP	= 0x0800	# IP protocol

# ARP operation
ARP_OP_REQUEST		= 1	# request to resolve ha given pa
ARP_OP_REPLY		= 2	# response giving hardware address
ARP_OP_REVREQUEST	= 3	# request to resolve pa given ha
ARP_OP_REVREPLY		= 4	# response giving protocol address

class ARP(pypacker.Packet):
	__hdr__ = (
		("hrd", "H", ARP_HRD_ETH),
		("pro", "H", ARP_PRO_IP),
		("hln", "B", 6),	# hardware address length
		("pln", "B", 4),	# protocol address length
		("op", "H", ARP_OP_REQUEST),
		("sha", "6s", b""),
		("spa", "4s", b""),
		("tha", "6s", b""),
		("tpa", "4s", b"")
		)
