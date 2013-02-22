"""Encapsulated Security Protocol."""

from .. import pypacker

class ESP(pypacker.Packet):
	__hdr__ = (
		("spi", "I", 0),
		("seq", "I", 0)
		)
