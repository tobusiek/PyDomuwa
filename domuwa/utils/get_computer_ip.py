import socket


def get_ip_address(port: int = 80) -> str:
    hostname = socket.gethostname()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.connect(("8.8.8.8", port))
    return s.getsockname()[0]


if __name__ == '__main__':
    print("IP addr:", get_ip_address())
