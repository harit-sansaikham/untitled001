import socket,time
from random import randrange 

def print_notif(x):
    global player,name,s,bot
    for i in sorted(x):
        i = i.upper()
        if i[0] == 'K':
            if name == i[1]:
                print("You die..")
                s.send("-".encode('ascii'))
                s.close()
                return False
            else :
                print("<< %s(%s) was killed >>"%(i[1],'player' if i[1] in player else 'bot'))
            bot = bot.replace(i[1],'')
        elif i[0] == 'E':
            if i[1] == name:
                name = i[2]
                print("Your Name Is \'%s\'"%name)
            bot = bot.replace(i[2],'')
            player = player.replace(i[1],'')
            bot = "%s%s"%(bot,i[1])
            player = "%s%s"%(player,i[2])
            print("bot =",bot)
            print("player =",player)

        elif i[0] == 'I' and i[1]==name:
            add_item()
        elif i[0] == 'D' and name in i[1:]:
            print("<< You was Detected >>")
        elif i[0] == 'C':
            print("<< Cursing >>")
        elif i[0] == 'U':
            print("<< Uncursing >>")
    return True

def print_map(x):
    size = 9
    map_ = [[] for i in range(size*size)]
    stack = []
    for i in x:
        map_[int(i[0])*size+int(i[1])].append(i[2]if i[2]in player else i[2].lower())
    for i in range(size):
        if i %3 ==0:
            print('-'*(size//3*4+1))
        for j in range(size):
            if j%3 == 0:
                print('|',end='')
            if  len(map_[i*size + j])>1:    
                map_[i*size + j] = [ k for k in map_[i*size + j] if k !='?']
            if len(map_[i*size + j])==0:
                print(' ',end='')
            elif len(map_[i*size + j])==1:
 
                print(map_[i*size+j][0],end='')
            else :
                print(len(stack),end='')
                stack.append(map_[i*size+j])
        print("|")
    print('-'*(size//3*4+1))
    for i in range(len(stack)):
        print('*%d'%i,"=",stack[i])

def add_item():
    global item_name,ITEM
    possible = '2223335'+'P'*2+'E'*1+'C'*1+'F'*2+'LXZ'
    ans = possible[randrange(0,len(possible))]
    if '0'<= ans <= '9':
        ITEM['H'] += int (ans)
        print("Get >>",item_name['H'],'x'+ans)
    else :
        ITEM[ans]+=1
        print("Get >>",item_name[ans])


# connect to server
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
port = 9999
size = 2048 
item_name = {'H':'[H]ack','P':'[P]ush','E':'[E]xchange','C':'[C]urse','F':'[F]ake Curse'
                ,'L':'kill [L]ane.','X':'kill [X]cross.','Z':'kill [Z]one.'}
ITEM = dict()
for i in item_name:
    ITEM[i]=0
while True:
    try:
        host = input("Connect to HOST = ")
        #host = socket.gethostname()
        s.connect((host,port))
        s.settimeout(99999)
        print("Connecting Complete")
        break
    except:
        print("Cant Connnect to Server")

# Game Start
name = s.recv(4).decode('ascii')
print("Your Name Is \'%s\'"%name)
print("WAITING for other player")
player,bot = s.recv(1024).decode('ascii').split()
print(player)
msg = s.recv(2048).decode('ascii')
strmap = msg
print_map(msg.split())

# loop for each turn
while True:
    msg = '...'
    while True:
        print("[M]ove.: [U]p,[D]own,[L]eft,[R]ight")
        for i in sorted(ITEM):
                if ITEM[i]>0:
                    print(' -',item_name[i],'x%d'%ITEM[i])
        print("End[.]")
        x = input(" -> ").upper()
        #x = 'M'+'UDLRI'[randrange(0,5)]
        if x[0:3] == '\\\\ ':
            msg = x[3:]
            break
        else :
            if len(x)>0:
                i = x[0]
                x = x[1:]
            else :
                print("INPUT ERROR: please try again")
                continue
            # Case Move
            if i=='M':
                if len(x)>0:
                    i = x[0]
                    x = x[1:]
                else :
                    print("[U]p,[D]own,[L]eft,[R]ight")
                    i = input(" -> ").upper()
                    if i == '..' :
                        continue
                if i in ['U','D','L','R','I']:
                    msg = "%s %s"%(msg,name+'m'+i + name)
                    break
                else :
                    print("INPUT ERROR: please try again")
                    continue
            elif i=='H' and ITEM['H']>0:
                can_ = name+bot.lower()
                if len(x)>0:
                    i = x[0]
                    x = x[1:]
                else :
                    print("\'%s\'"%can_)
                    i = input(" -> ").upper()
                    if i == '..' :
                        continue
                if i in [j for j in can_.upper()]:
                    if len(x)>0:
                        j = x[0]
                        x = x[1:]
                    else :
                        print("[U]p,[D]own,[L]eft,[R]ight")
                        j = input(" -> ").upper()
                        if j == '..' :
                            continue
                    if j in ['U','D','L','R','I']:
                        msg = "%s %s"%(msg,i+'H'+ j + name)
                        print("Hack >> %s %s"%(i,j))
                        ITEM['H']-=1
                    else :
                        print("INPUT ERROR: please try again")
                        continue
            elif i=='P' and ITEM['P']>0:
                can_ = name + bot.lower()
                if len(x)>0:
                    i = x[0]
                    x = x[1:]
                else :
                    print("\'%s\'"%can_)
                    i = input(" -> ").upper()
                    if i == '..' :
                        continue
                if i in [j for j in can_.upper()]:
                    if len(x)>0:
                        j = x[0]
                        x = x[1:]
                    else :
                        print("[U]p,[D]own,[L]eft,[R]ight")
                        j = input(" -> ").upper()
                        if j == '..' :
                            continue
                    if j in ['U','D','L','R','I']:
                        if len(x)>0:
                            k = x[0]
                            x = x[1:]
                        else :
                            print("Distance [0-8]")
                            k = input(" -> ").upper()
                            if k == '..' :
                                continue
                        if  '0'<=k<='8':
                            msg = "%s%s"%(msg,(' '+i+'P'+ j + name)*int(k))
                            print("Push >> %s %s %s"%(i,j,k))
                            ITEM['P']-=1
                        else :
                            print("INPUT ERROR: please try again")
                            continue
                    else :
                        print("INPUT ERROR: please try again")
                        continue
                else :
                    print("INPUT ERROR: please try again")
                    continue
            elif i=='E' and ITEM['E']>0:
                can_ = name + bot.lower()
                if len(x)>0:
                    i = x[0]
                    x = x[1:]
                else :
                    print("\'%s\'"%can_)
                    i = input(" -> ").upper()
                    if i == '..' :
                        continue
                if i in [j for j in can_.upper()]:
                    msg = "%s %s"%(msg,(name + 'E' +i))
                    print("Exchange >>",i)
                    ITEM['E']-=1
                else :
                    print("INPUT ERROR: please try again")
                    continue
            elif i=='C' and ITEM['C']>0:
                can_ = name + bot.lower()
                if len(x)>0:
                    i = x[0]
                    x = x[1:]
                else :
                    print("\'%s\'"%can_)
                    i = input(" -> ").upper()
                    if i == '..' :
                        continue
                if i in [j for j in can_.upper()]:
                    msg = "%s %s"%(msg,(i+'C'))
                    print("Curse >>",i)
                    ITEM['C']-=1
                else :
                    print("INPUT ERROR: please try again")
                    continue
            elif i=='F' and ITEM['F']>0:
                msg = "%s %s"%(msg,('_F'))
                print("Fake Curse")
                ITEM['F'] -= 1
            elif i in ['L','X','Z'] and ITEM[i]>0:
                map_ = strmap.split()
                can_ = []
                for k in map_:
                    if k[2] == name :
                        mypos = k[0:2]
                        break
                if i == 'L':
                    for k in map_:
                        if k[2] in bot :
                            if k[0] == mypos[0] or k[1] == mypos[1]:
                                can_.append(k[2])
                elif i == 'X':
                    for k in map_:
                        if k[2] in bot :
                            if int(k[0])-int(k[1]) == int(mypos[0])-int(mypos[1]) or int(k[0])+int(k[1]) == int(mypos[0])+int(mypos[1]):
                                can_.append(k[2])
                elif i == 'Z':
                    for k in map_:
                        if k[2] in bot :
                            if int(k[0])//3*3+int(k[1])//3 == int(mypos[0])//3*3+int(mypos[1])//3 :
                                can_.append(k[2])              
                if len(x)>0:
                    j = x[0]
                    x = x[1:]
                else :
                    print("\'%s\'"%''.join(can_))
                    j = input(" -> ").upper()
                    if j == '..' :
                        continue
                if j in can_:
                    msg = "%s %s"%(msg,('_'+ i + j))
                    print("Kill >>",j)
                    ITEM[i]-=1
                    break
                else :
                    print("INPUT ERROR: please try again")
                    continue
            elif i=='.':
                break
            else:
                print("INPUT ERROR: please try again")
                continue
    s.send(msg.encode('ascii'))

    print("WAITING for other player")
    while True:
        try :
            msg  = s.recv(2048).decode('ascii')
            break
        except:
            pass

    #print("\'%s\'"%msg)

    notif,strmap = msg.split(',')
    notif = notif.split()
    if '-' in notif:
        print("YOU WIN!!")
        s.close()
        break
    if print_notif(notif) == False:
        break
    print_map(strmap.split())
