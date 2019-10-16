'''
chat room 客户端
发送请求，展示结果
'''
import os,sys
from socket import *
ADDR = ('127.0.0.1',4532)

def send_msg(s,name):
    while True :
        try:
            text = input('>>')
        except (KeyboardInterrupt,SyntaxError ):
            text = 'quit'

        if text.strip()=='quit':  ###除去可能有的空格
            msg = 'Q'+name
            s.sendto(msg.encode(), ADDR)
            sys.exit('退出聊天室')      ###只是退出了一个进程，不影响另一个进程，需要服务器将另一个进程退出
        msg = 'C %s %s'%(name,text)
        s.sendto(msg.encode(),ADDR)


def recv_msg(s):
    while True :
        data,addr = s.recvfrom(4096)
        if data.decode() == 'Exit':
            sys.exit()           ###exit有break的作用吗？？？？？？
        print(data.decode()+'\n>>',end = '')



def main():
    s = socket(AF_INET,SOCK_DGRAM )
    #进入聊天室
    while True :
        name  = input('请输入昵称：')
        msg = 'L '+name
        s.sendto(msg.encode() ,ADDR)
        #接受反馈
        data, addr = s.recvfrom(2014)
        if data.decode()  == "OK":
            print('您已进入聊天室')
            break
        else:
            print(data.decode() )
    #已经进入聊天室
    pid = os.fork()
    if pid <0:
        sys.exit('Error')
    elif pid==0:
        send_msg(s,name)
    else:
        recv_msg(s)


if __name__ == '__main__':   ###main Tab
    main()


