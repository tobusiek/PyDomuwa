import socket


def get_ip_address(port: int = 80) -> str:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", port))
    ip_addr = s.getsockname()[0]
    s.close()
    return ip_addr


if __name__ == '__main__':
    print("IP addr:", get_ip_address())
