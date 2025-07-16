import pyshark

interfaces = pyshark.tshark.tshark.get_tshark_interfaces()
print("📡 Available interfaces:")
for iface in interfaces:
    print("-", iface)
