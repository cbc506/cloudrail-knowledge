from typing import Optional, Union


class IpProtocol:
    ALL = 'ALL'

    def __init__(self, protocol: Optional[Union[str, int]]):
        self._protocol: str
        if not protocol or str(protocol).lower() in ('-1', 'all', 'any', -1, '*'):  # Representation for 'all' protocols in all cloud vendors.
            self._protocol = self.ALL
        elif isinstance(protocol, int) or protocol.isdigit():
            protocol = int(protocol)
            self._protocol = self._from_int(protocol)
        else:
            self._assert_textual_protocol(protocol)
            self._protocol = protocol.upper()

    @staticmethod
    def _from_int(protocol: int):
        return ip_protocol_table[protocol]

    @staticmethod
    def _assert_textual_protocol(protocol: str):
        # Make sure the protocol is actually a valid protocol from the list of protocols
        if not any(proto.lower() == protocol.lower() for proto in ip_protocol_table.values()):
            raise ValueError(f'The value: "{protocol}" is not a valid protocol type.')

    def __eq__(self, other):
        return (isinstance(other, IpProtocol) and self._protocol == other._protocol) or \
               (isinstance(other, str) and self._protocol == other.upper())

    def __repr__(self):
        return self._protocol

    def __contains__(self, item):
        return self._protocol == self.ALL or self == item

    def intersection(self, item):
        if self._protocol == self.ALL:
            return item
        if item == self.ALL:
            return self
        if item == self:
            return item
        return None



ip_protocol_table = {
  0: "HOPOPT",
  1: "ICMP",
  2: "IGMP",
  3: "GGP",
  4: "IPv4 encapsulation",
  5: "ST",
  6: "TCP",
  7: "CBT",
  8: "EGP",
  9: "IGP",
  10: "BBN-RCC-MON",
  11: "NVP-II",
  12: "PUP",
  13: "ARGUS",
  14: "EMCON",
  15: "XNET",
  16: "CHAOS",
  17: "UDP",
  18: "MUX",
  19: "DCN-MEAS",
  20: "HMP",
  21: "PRM",
  22: "XNS-IDP",
  23: "TRUNK-1",
  24: "TRUNK-2",
  25: "LEAF-1",
  26: "LEAF-2",
  27: "RDP",
  28: "IRTP",
  29: "ISO-TP4",
  30: "NETBLT",
  31: "MFE-NSP",
  32: "MERIT-INP",
  33: "DCCP",
  34: "3PC",
  35: "IDPR",
  36: "XTP",
  37: "DDP",
  38: "IDPR-CMTP",
  39: "TP++",
  40: "IL",
  41: "IPv6 encapsulation",
  42: "SDRP",
  43: "IPv6-Route",
  44: "IPv6-Frag",
  45: "IDRP",
  46: "RSVP",
  47: "GRE",
  48: "DSR",
  49: "BNA",
  50: "ESP",
  51: "AH",
  52: "I-NLSP",
  53: "SWIPE",
  54: "NARP",
  55: "MOBILE",
  56: "TLSP",
  57: "SKIP",
  58: "IPv6-ICMP",
  59: "IPv6-NoNxt",
  60: "IPv6-Opts",
  61: "any host internal protocol",
  62: "CFTP",
  63: "any local network",
  64: "SAT-EXPAK",
  65: "KRYPTOLAN",
  66: "RVD",
  67: "IPPC",
  68: "any distributed file system",
  69: "SAT-MON",
  70: "VISA",
  71: "IPCV",
  72: "CPNX",
  73: "CPHB",
  74: "WSN",
  75: "PVP",
  76: "BR-SAT-MON",
  77: "SUN-ND",
  78: "WB-MON",
  79: "WB-EXPAK",
  80: "ISO-IP",
  81: "VMTP",
  82: "SECURE-VMTP",
  83: "VINES",
  84: "IPTM",
  85: "NSFNET-IGP",
  86: "DGP",
  87: "TCF",
  88: "EIGRP",
  89: "OSPFIGP",
  90: "Sprite-RPC",
  91: "LARP",
  92: "MTP",
  93: "AX.25",
  94: "IPIP",
  95: "MICP",
  96: "SCC-SP",
  97: "ETHERIP",
  98: "ENCAP",
  99: "any private encryption scheme",
  100: "GMTP",
  101: "IFMP",
  102: "PNNI",
  103: "PIM",
  104: "ARIS",
  105: "SCPS",
  106: "QNX",
  107: "A/N",
  108: "IPComp",
  109: "SNP",
  110: "Compaq-Peer",
  111: "IPX-in-IP",
  112: "VRRP",
  113: "PGM",
  114: "any 0-hop protocol",
  115: "L2TP",
  116: "DDX",
  117: "IATP",
  118: "STP",
  119: "SRP",
  120: "UTI",
  121: "SMP",
  122: "SM",
  123: "PTP",
  124: "ISIS",
  125: "FIRE",
  126: "CRTP",
  127: "CRUDP",
  128: "SSCOPMCE",
  129: "IPLT",
  130: "SPS",
  131: "PIPE",
  132: "SCTP",
  133: "FC",
  134: "RSVP-E2E-IGNORE",
  135: "Mobility Header",
  136: "UDPLite",
  137: "MPLS-in-IP",
  138: "manet",
  139: "HIP",
  140: "Shim6",
  141: "WESP",
  142: "ROHC",
  143: "Ethernet"
}
