from socket import *
import os, sys

SERVER_ADDR = ('0.0.0.0', 8888)

#发送消息
def send_msg(sockfd, name):
    while True:
        text = input("发言：")
        if text == "exit":
            msg = "E %s %s" % (name, text)
            sockfd.sendto(msg.encode(), SERVER_ADDR)
            break
        msg = "C %s %s"%(name, text)
        sockfd.sendto(msg.encode(), SERVER_ADDR)

#接收消息
def recv_msg(sockfd):
    while True:
        msg, addr = sockfd.recvfrom(1024)
        if msg.decode() == 'EXIT':
            sys.exit()
        print(msg.decode())

#创建网络连接
def main():
    sockfd = socket(AF_INET, SOCK_DGRAM)
    while True:
        name = input("输入姓名")
        msg = "L " + name
        sockfd.sendto(msg.encode(), SERVER_ADDR)
        data, addr = sockfd.recvfrom(1024)
        if data.decode() == "OK":
            print("成功进入聊天室")
            break
        else:
            print(data.decode())
    pid = os.fork()

    if pid < 0:
        sys.exit("Error!")
    elif pid == 0:
        send_msg(sockfd, name)
    else:
        recv_msg(sockfd)
    sockfd.close()

if __name__ == '__main__':
    main()