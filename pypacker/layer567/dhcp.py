"""Dynamic Host Configuration Protocol."""

from .. import pypacker
from ..layer12 import arp
import logging
logger = logging.getLogger("pypacker")


DHCP_OP_REQUEST		= 1
DHCP_OP_REPLY		= 2

DHCP_MAGIC		= 0x63825363

# DHCP option codes
DHCP_OPT_NETMASK	= 1 # I: subnet mask
DHCP_OPT_TIMEOFFSET	= 2
DHCP_OPT_ROUTER		= 3 # s: list of router ips
DHCP_OPT_TIMESERVER	= 4
DHCP_OPT_NAMESERVER	= 5
DHCP_OPT_DNS_SVRS	= 6 # s: list of DNS servers
DHCP_OPT_LOGSERV	= 7
DHCP_OPT_COOKIESERV	= 8
DHCP_OPT_LPRSERV	= 9
DHCP_OPT_IMPSERV	= 10
DHCP_OPT_RESSERV	= 11
DHCP_OPT_HOSTNAME	= 12 # s: client hostname
DHCP_OPT_BOOTFILESIZE	= 13
DHCP_OPT_DUMPFILE	= 14
DHCP_OPT_DOMAIN		= 15 # s: domain name
DHCP_OPT_SWAPSERV	= 16
DHCP_OPT_ROOTPATH	= 17
DHCP_OPT_EXTENPATH	= 18
DHCP_OPT_IPFORWARD	= 19
DHCP_OPT_SRCROUTE	= 20
DHCP_OPT_POLICYFILTER	= 21
DHCP_OPT_MAXASMSIZE	= 22
DHCP_OPT_IPTTL		= 23
DHCP_OPT_MTUTIMEOUT	= 24
DHCP_OPT_MTUTABLE	= 25
DHCP_OPT_MTUSIZE	= 26
DHCP_OPT_LOCALSUBNETS	= 27
DHCP_OPT_BROADCASTADDR	= 28
DHCP_OPT_DOMASKDISCOV	= 29
DHCP_OPT_MASKSUPPLY	= 30
DHCP_OPT_DOROUTEDISC	= 31
DHCP_OPT_ROUTERSOLICIT	= 32
DHCP_OPT_STATICROUTE	= 33
DHCP_OPT_TRAILERENCAP	= 34
DHCP_OPT_ARPTIMEOUT	= 35
DHCP_OPT_ETHERENCAP	= 36
DHCP_OPT_TCPTTL		= 37
DHCP_OPT_TCPKEEPALIVE	= 38
DHCP_OPT_TCPALIVEGARBAGE= 39
DHCP_OPT_NISDOMAIN	= 40
DHCP_OPT_NISSERVERS	= 41
DHCP_OPT_NISTIMESERV	= 42
DHCP_OPT_VENDSPECIFIC	= 43
DHCP_OPT_NBNS		= 44
DHCP_OPT_NBDD		= 45
DHCP_OPT_NBTCPIP	= 46
DHCP_OPT_NBTCPSCOPE	= 47
DHCP_OPT_XFONT		= 48
DHCP_OPT_XDISPLAYMGR	= 49
DHCP_OPT_REQ_IP		= 50 # I: IP address
DHCP_OPT_LEASE_SEC	= 51 # I: lease seconds
DHCP_OPT_OPTIONOVERLOAD = 52
DHCP_OPT_MSGTYPE	= 53 # B: message type
DHCP_OPT_SERVER_ID	= 54 # I: server IP address
DHCP_OPT_PARAM_REQ	= 55 # s: list of option codes
DHCP_OPT_MESSAGE	= 56
DHCP_OPT_MAXMSGSIZE	= 57
DHCP_OPT_RENEWTIME	= 58
DHCP_OPT_REBINDTIME	= 59
DHCP_OPT_VENDOR_ID	= 60 # s: vendor class id
DHCP_OPT_CLIENT_ID	= 61 # Bs: idtype, id (idtype 0: FQDN, idtype 1: M
DHCP_OPT_NISPLUSDOMAIN	= 64
DHCP_OPT_NISPLUSSERVERS = 65
DHCP_OPT_MOBILEIPAGENT	= 68
DHCP_OPT_SMTPSERVER	= 69
DHCP_OPT_POP3SERVER	= 70
DHCP_OPT_NNTPSERVER	= 71
DHCP_OPT_WWWSERVER	= 72
DHCP_OPT_FINGERSERVER	= 73
DHCP_OPT_IRCSERVER	= 74
DHCP_OPT_STSERVER	= 75
DHCP_OPT_STDASERVER	= 76

# DHCP message type values
DHCPDISCOVER		= 1
DHCPOFFER		= 2
DHCPREQUEST		= 3
DHCPDECLINE		= 4
DHCPACK			= 5
DHCPNAK			= 6
DHCPRELEASE		= 7
DHCPINFORM		= 8

class DHCP(pypacker.Packet):
	__hdr__ = (
		("op", "B", DHCP_OP_REQUEST),
		("hrd", "B", arp.ARP_HRD_ETH),	# just like ARP.hrd
		("hln", "B", 6),		# and ARP.hln
		("hops", "B", 0),
		("xid", "I", 0xdeadbeef),
		("secs", "H", 0),
		("flags", "H", 0),
		("ciaddr", "I", 0),
		("yiaddr", "I", 0),
		("siaddr", "I", 0),
		("giaddr", "I", 0),
		("chaddr", "16s", 16 * b"\x00"),
		("sname", "64s", 64 * b"\x00"),
		("file", "128s", 128 * b"\x00"),
		("magic", "I", DHCP_MAGIC)
							# _opts = opts
		)
	#opts = (
	#	(DHCP_OPT_MSGTYPE, chr(DHCPDISCOVER)),
	#	(DHCP_OPT_PARAM_REQ, "".join(map(chr, (DHCP_OPT_REQ_IP,
	#						DHCP_OPT_ROUTER,
	#						DHCP_OPT_NETMASK,
	#						DHCP_OPT_DNS_SVRS))))
	#	)	# list of (type, data) tuples

	def getopts(self):
		if not hasattr(self, "_opts"):
			tl = DHCPTriggerList()
			self._add_headerfield("_opts", "", tl)
		return self._opts
	def setopts(self, value):
		self._opts = value
	opts = property(getopts, setopts)

	def _unpack(self, buf):
		logger.debug("DHCP: parsing options")
		opts = self.__get_opts(buf[self.__hdr_len__:])
		self._add_headerfield("_opts", "", opts)
		pypacker.Packet._unpack(self, buf)

	def __get_opts(self, buf):
		#logger.debug("DHCP: parsing options from: %s" % buf)
		opts = []
		i = 0

		while i < len(buf):
			t = buf[i]
			p = None
			#logger.debug("DHCP: adding option: %d" % t)

			# last option
			if t in [0, 0xff]:
				p = DHCPOptSingle(type=t)
				i += 1
			else:
				dlen = buf[i+1]
				p = DHCPOptMulti(type=t, len=dlen, data=buf[ i+2 : i+2+dlen])
				i += 2+dlen

			opts += [p]

			if t == 0xff:
				break

		#return TriggerList(opts)
		return DHCPTriggerList(opts)

class DHCPTriggerList(pypacker.TriggerList):
	"""DHCP-TriggerList to enable "opts += [(DHCP_OPT_X, b"xyz")], opts[x] = (DHCP_OPT_X, b"xyz")",
	length should be auto-calculated."""
	def __iadd__(self, li):
		"""TCP-options are added via opts += [(TCP_OPT_X, b"xyz")]."""
		return pypacker.TriggerList.__iadd__(self, self.__tuple_to_opt(li))

	def __setitem__(self, k, v):
		"""TCP-options are set via opts[x] = (TCP_OPT_X, b"xyz")."""
		pypacker.TriggerList.__setitem__(self, k, self.__tuple_to_opt([v]))

	def __tuple_to_opt(self, tuple_list):
		"""convert [(DHCP_OPT_X, b""), ...] to [DHCPOptXXX]."""
		opt_packets = []

		# parse tuples to DHCP-option Packets
		for opt in tuple_list:
			p = None
			# single opt
			if opt[0] in [0, 0xff]:
				p = DHCPOptSingle(type=opt[0])
			# multi opt
			else:
				p = DHCPOptMulti(type=opt[0], len=len(opt[1]), data=opt[1])
			opt_packets += [p]
		return opt_packets


class DHCPOptSingle(pypacker.Packet):
	__hdr__ = (
		("type", "B", None),
		)

class DHCPOptMulti(pypacker.Packet):
	__hdr__ = (
		("type", "B", None),
		("len", "B", None),
		)
