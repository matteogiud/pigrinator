import socket

def get_ip_from_mdns(mdns):
    if mdns is None:
        return None
    try:
        try:
            addr_info = socket.getaddrinfo(hostname, 80)[0]
        except:
            addr_info = socket.getaddrinfo(f"{mdns}.local", 80)[0]
        ip_address = addr_info[-1][0]
        return ip_address
    except Exception as e:
        print(e)
        return None
