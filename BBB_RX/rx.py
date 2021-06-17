import socket


if __name__ == '__main__':
    BBB_rx_host = '192.168.0.4'
    # BBB_rx_host = '127.0.0.1'   # test
    BBB_rx_port = 10002

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((BBB_rx_host, BBB_rx_port))

    while True:
        msg_recv, addr = udp_socket.recvfrom(2048)
        print("Message from", addr, ":\n" + str(msg_recv, encoding="utf-8"))

    # udp_socket.close()