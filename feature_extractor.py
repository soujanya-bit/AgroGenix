# backend/utils/feature_extractor.py

import numpy as np

def extract_features(pkt):
    """
    Given a single PyShark packet, extract a 78-element feature list.
    We're using a simplified set of fields here; fill in more as needed.
    """

    try:
        # 1) Protocol: 0=Other, 1=TCP, 2=UDP, 3=ICMP
        proto = 0
        if "TCP" in pkt:
            proto = 1
        elif "UDP" in pkt:
            proto = 2
        elif "ICMP" in pkt:
            proto = 3

        # 2) Packet length (bytes)
        ip_len = int(pkt.length) if hasattr(pkt, "length") else 0

        # 3) Source & destination ports (0 if not TCP/UDP)
        if hasattr(pkt, pkt.transport_layer):
            src_port = int(pkt[pkt.transport_layer].srcport)
            dst_port = int(pkt[pkt.transport_layer].dstport)
        else:
            src_port = 0
            dst_port = 0

        # 4) TCP flags (only if TCP; else all zeros)
        fin = syn = rst = psh = ack = urg = 0
        if "TCP" in pkt:
            flags_hex = pkt.tcp.flags  # e.g., "0x002" or a decimal string
            # PyShark sometimes presents flags as decimal or hex. Convert to int.
            flags_int = int(flags_hex, 16) if flags_hex.startswith("0x") else int(flags_hex)
            fin = (flags_int & 0x01) >> 0
            syn = (flags_int & 0x02) >> 1
            rst = (flags_int & 0x04) >> 2
            psh = (flags_int & 0x08) >> 3
            ack = (flags_int & 0x10) >> 4
            urg = (flags_int & 0x20) >> 5

        # 5) IP header length
        ip_hdr_len = int(pkt.ip.hdr_len) if "IP" in pkt and hasattr(pkt.ip, "hdr_len") else 0

        # 6) Time To Live
        ttl = int(pkt.ip.ttl) if "IP" in pkt and hasattr(pkt.ip, "ttl") else 0

        # 7) TCP payload length (application data) 
        payload_len = int(pkt.tcp.len) if "TCP" in pkt and hasattr(pkt.tcp, "len") else 0

        # 8) TCP window size
        win_size = int(pkt.tcp.window_size_value) if "TCP" in pkt and hasattr(pkt.tcp, "window_size_value") else 0

        # 9) Flow identifiers (hash of 5-tuple) – if you want to track flows,
        #    but here we’ll store src_ip and dst_ip as dummy numeric codes.
        src_ip = pkt.ip.src if "IP" in pkt and hasattr(pkt.ip, "src") else "0.0.0.0"
        dst_ip = pkt.ip.dst if "IP" in pkt and hasattr(pkt.ip, "dst") else "0.0.0.0"
        # Convert last byte of IP to int (just an example placeholder)
        src_ip_code = int(src_ip.split('.')[-1]) if src_ip != "0.0.0.0" else 0
        dst_ip_code = int(dst_ip.split('.')[-1]) if dst_ip != "0.0.0.0" else 0

        # 10) Interarrival time: PyShark provides sniff_timestamp (seconds)
        timestamp = float(pkt.sniff_timestamp)
        # We'll leave actual IAT calculation to later; for now store timestamp
        iat = timestamp  # real IAT requires previous packet timestamp

        # Build a partial list of the features we have (total so far: 12)
        raw = [
            proto,
            ip_len,
            src_port,
            dst_port,
            fin, syn, rst, psh, ack, urg,
            ip_hdr_len,
            ttl,
            payload_len,
            win_size,
            src_ip_code,
            dst_ip_code,
            iat
        ]

        # At this point, len(raw) == 17. Now we pad with zeros to reach 78:
        while len(raw) < 78:
            raw.append(0)

        # If for some reason it goes beyond 78, just truncate
        return raw[:78]

    except Exception as e:
        # In production, log this error. For now, skip packet.
        # print(f"Skipped packet: {e}")
        return None
