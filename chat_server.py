'''
chat room          干什么，环境，姓名邮箱
env:python3.6
socket udp & fork exc
'''
from socket import *
import  os,sys
#全局变量：很多封装模块儿都要用或者有特定含义的变量
ADDR = ('0.0.0.0',4532)


#储存用户
user = {}


#处理用户登录
def do_login(s,name,addr):
    if name in user or '管理员'in name:
        s.sendto('用户名存在',addr)
        return
    else:
        s.sendto(b'OK' ,addr)    ##可以进入
    #先通知其他人，再存字典
    msg = '欢迎%s加入群聊'%name
    for i in user:
        s.sendto(msg.encode(),user[i])
    user[name] = addr

#处理聊天
def do_chat(s,name,text):
    msg = '%s:%s'%(name,text)
    for i in user:
        if i !=name:          ###只需发给发话人以外的人
            s.sendto(msg.encode(),user[i])

#响应退出聊天
def do_quit(s,name):
    msg = '%s退出了群聊'%(name)
    for i in user:
        if i == name:
            s.sendto(b'Exit', user[i])
        else:
            s.sendto(msg.encode(),user[i])
    del user[name]


#循环接受客户端请求
def do_request(s):
    while True :
        data,addr = s.recvfrom(1024)
        tmp =data.decode().split(' ')
        #根据不同的请求类型执行不同的事件
        if tmp[0] == 'L':
            do_login(s,tmp[1],addr)
        elif tmp[0] == 'C':
            tmp = data.split(' ',2)   ###只分割前两个的空格
            do_chat(s,tmp[1],tmp[2])
        elif tmp[0] =='Q':
            do_quit(s,tmp[1])


#搭建网络
def main():
    #UDP网络
    s = socket(AF_INET,SOCK_DGRAM )          #######
    s.bind(ADDR)
    pid = os.fork()
    if pid == 0 :
        #完成管理员消息管理
        while True :
            msg = input('管理员消息：')
            text = 'C 管理员 %s'%msg
            s.sendto(text.encode() ,ADDR)   ###管理员消息从子进程发给父进程

    else:
        #接受客户端请求
        do_request(s)




if __name__ == '__main__':
    main()

