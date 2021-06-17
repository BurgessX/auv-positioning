import socket


if __name__ == '__main__':
    raspi_host = '192.168.7.1'
    # raspi_host = '127.0.0.1'   # test
    raspi_port = 10000

    BBB_tx_host = '192.168.7.2'
    # BBB_tx_host = '127.0.0.1'   # test
    BBB_tx_port = 10001

    BBB_rx_host = '192.168.0.4'
    # BBB_rx_host = '127.0.0.1'   # test
    BBB_rx_port = 10002

    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind((BBB_tx_host, BBB_tx_port))

    while True:
        msg_recv, addr = udp_socket.recvfrom(2048)
        print("Message from", addr, ":\n" + str(msg_recv, encoding="utf-8"))

        udp_socket.sendto(msg_recv, (BBB_rx_host, BBB_rx_port))


    # udp_socket.close()