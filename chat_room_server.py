from socket import *
import os, sys

user = {}

#服务器地址
SERVER_ADDR = ('0.0.0.0', 8888)

def login(sockfd, name, addr):
    if name in user or "管理员" in name:
        msg = "改昵称已存在"
        sockfd.sendto(msg.encode(), addr)
        return
    else:
        sockfd.sendto(b'OK', addr)

    #发给其他用户提示新成员进入
    msg = "欢迎%s加入群聊！"%name
    for i in user:
        sockfd.sendto(msg.encode(), user[i])
    #加入用户
    user[name] = addr

def chat(sockfd, name, text):
    msg = "%s:%s"%(name, text)
    for i in user:
        if i != name:
            sockfd.sendto(msg.encode(), user[i])

#退出群聊
def quit(sockfd, name):
    msg = "%s退出群聊"%name
    for i in user:
        if i != name:
            sockfd.sendto(msg.encode(), user[i])
        else:
            sockfd.sendto(b'EXIT', user[i])
    if name in user:
        del user[name]
    else:
        return

def do_request(sockfd):
    while True:
        data, addr = sockfd.recvfrom(1024)
        choose = data.decode().split(' ')
        msg = choose[0]
        if msg == 'L':
            login(sockfd, choose[1], addr)
        elif msg == 'C':
            text = ' '.join(msg[2:])
            chat(sockfd, choose[1], choose[2])
        else:
            quit(sockfd, choose[1])

#创建网络连接
def main():
    sockfd = socket(AF_INET, SOCK_DGRAM)
    sockfd.bind(SERVER_ADDR)

    pid = os.fork()
    if pid < 0:
        return
    elif pid == 0:
        #发送管理员消息
        while True:
            msg = input("管理员消息：")
            msg = "C 管理员消息 " + msg
            sockfd.sendto(msg.encode(), SERVER_ADDR)
    else:
        #处理客户端请求
        do_request(sockfd)


if __name__ == "__main__":
    main()