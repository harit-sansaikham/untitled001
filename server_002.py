import socket,threading,sys
from random import randrange 

# set variable
turn_count = 0
name_possible = [i for i in'ABCDEFGHIJKLMNOPQRSTUVWXYZ']
player = '' 
bot = ''
cursed = ''
contorled = ''
history = dict()
item = []
thread_list = []
get_item = dict()
pos = dict()
map_size = 9
in_turn = False
processing = True
acting = 0
deck = [i for i in 'K'*14 + 'C'*4 + '123456789'*2 + 'D'*7 + 'U'*3 + 'H'*5 + 'R'*1]
card_used = []
card_name = {'K':'[K]ill.','C':'[C]hain kill.','R':'[R]eset deck.'
                ,'1':'detect[1].','2':'detect[2].','3':'detect[3].'
                ,'4':'detect[4].','5':'detect[5].','6':'detect[6].'
                ,'7':'detect[7].','8':'detect[8].','9':'detect[9].'
                ,'D':'[D]ouble draw','U':'[U]ncursed.','H':'[H]istory'}

item_name = {'H':'Hack','P':'Push','E':'Exchange','C':'Curse','F':'Fake Curse'
                ,'L':'kill Lane.','X':'kill Xcross.','Z':'kill Zone.'}
CARD = dict()
for i in card_name:
    CARD[i]= 0 #Item begin
for i in item_name:
    history[i]=0
notif = []

def random_name():
    global name_possible
    return name_possible.pop(randrange(0,len(name_possible)))

def add_card():
    global CARD,deck,card_name
    if  len(deck) == 0 :
        print("Deck is Empty")
        return False
    x = deck.pop(randrange(0,len(deck)))
    print("Draw >>",card_name[x])
    CARD[x] += 1

def add_item():
    global pos,item
    zone = randrange(0,9)
    pos_use = [''.join(i) for i in pos]
    ans = []
    for i in range(zone//3*3,zone//3*3+3):
        for j in range(zone%3*3,zone%3*3+3):
            k = '%s%s'%(i,j)
            if k in item:
                return False
            elif k not in pos_use:
                ans.append(k)
    item.append(ans[randrange(0,len(ans))])

def sent_item():
    global get_item,item,notif
    for i in get_item :
        notif.append('I'+get_item[i][randrange(0,len(get_item[i]))])
        item.remove(i)
    get_item = dict()

def print_notif(x):
    global player
    for i in sorted(x):
        i = i.upper()
        if i[0] == 'K':
            print("<< %s(%s) was killed >>"%(i[1],'player' if i[1] in player else 'bot'))
        elif i[0] == 'F' or i[0] == 'C':
            print("<< Cursing >>")
        elif i[0] == 'U':
            print("<< Uncursing >>")
        elif i[0] == 'E':
            print("<< Exchanging >>")

def detect_zone(x):
    x = int(x)-1
    global pos,player,cursed,notif
    zone = [False for i in range(9)]
    in_zone =[[] for i in range(9)]
    for i in pos :
        in_zone[(pos[i][0]//3*3)+(pos[i][1]//3)].append(i)
        if i in player or i in cursed:
            zone[(pos[i][0]//3*3)+(pos[i][1]//3)]=True
    ans = zone[x]
    in_ans = in_zone[x]
    if x >=3:
        ans = ans or zone[x-3]
        in_ans.extend(in_zone[x-3])
    if x <6:
        ans = ans or zone[x+3]
        in_ans.extend(in_zone[x+3])
    if x%3>0:
        ans = ans or zone[x-1]
        in_ans.extend(in_zone[x-1])
    if x%3<2:
        ans = ans or zone[x+1]
        in_ans.extend(in_zone[x+1])
    in_ans = ''.join(sorted(in_ans))
    print("Detecting \'%s\'"%in_ans)
    notif.append('D'+in_ans)
    return ans

def print_map(x):
    global map_size
    size = map_size
    map_ = [[] for i in range(size*size)]
    stack = []
    for i in x:
        map_[int(i[0])*size+int(i[1])].append(i[2])
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

def pos_to_strlist():
    ans = []
    global pos,item
    for i in pos:
        ans.append("%d%d"%(pos[i][0],pos[i][1])+i)
    for i in item:
        ans.append(i+'?')
    return ans

def create_bot(n):
    global pos,bot
    for i in range(n):
        name = random_name()
        pos[name]=[map_size//2,map_size//2]
        bot = '%s%s'%(bot,name)

def move_bot():
    global contorled
    ans = []
    for i in bot:
        if i.upper() not in contorled :
            ans.append(i+'M'+'UDLRI'[randrange(0,5)]+'_')
    action(ans)

def action(x):
    global pos,map_size,bot,player,name_possible,get_item,item,contorled,cursed,history
    for i in x:
        i = i.upper()
        name = i[0]

        # Case Move
        if i[1] =='M' or i[1] == 'H' or i[1]=='P':
            if i[1] == 'H' or i[1] == 'P':
                history[i[1]]+=1
            if (name in pos) and (name != i[3] or (name == i[3] and (name not in contorled))):
                if i[2]=='U':
                    pos[name][0] -=1
                    if pos[name][0] < 0:
                        pos[name][0] =0
                elif i[2]=='L':
                    pos[name][1] -=1
                    if pos[name][1] < 0:
                        pos[name][1] =0
                elif i[2]=='D':
                    pos[name][0] +=1
                    if pos[name][0] >= map_size:
                        pos[name][0] = map_size-1
                elif i[2]=='R':
                    pos[name][1] +=1
                    if pos[name][1] >= map_size:
                        pos[name][1] = map_size-1
                k = '%d%d'%(pos[name][0],pos[name][1])
                if k in item:
                        get_item[k] = get_item.get(k,[])+[('_' if len(i)<4 else i[3])]
        # Case Kill
        elif  i[1] in ['K','L','X','Z']:
            if i[1] in ['L','X','Z']:
                history[i[1]] += 1
            if i[2] in bot+player:
                bot = bot.replace(i[2],'')
                del pos[i[2]]
                notif.append('K'+i[2])
                if len(bot) == 0:
                    notif.append('-')
        # Case Exchange
        elif i[1] == 'E':
            history[i[1]] += 1
            if name != i[2]:
                bot = bot.replace(i[2],'')
                cursed = cursed.replace(i[2],'')
                player = player.replace(name,'')
                bot = "%s%s"%(bot,name)
                player = "%s%s"%(player,i[2])
            notif.append('E'+name+i[2])
        # Case Curse
        elif i[1] == 'F' or i[1] == 'C':
            history[i[1]] += 1
            if name in bot:
                cursed = "%s%s"%(cursed,name)
            notif.append('C')

class ThreadedServer(object):
    global turn_count,N
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def listen(self):
        global player,pos
        self.sock.listen(N)
        thread_list = []
        for i in range(N):
            client, addr = self.sock.accept()
            print("Connection from: %s"%str(addr))
            client.settimeout(99999)
            name = random_name()
            client.send(name.encode('ascii'))
            pos[name] = [map_size//2,map_size//2]
            player = '%s%s'%(player,name)
            thread_list.append(threading.Thread(target = self.listenToClient,args = (i,client,addr,name)))

        print("ALL")
        threading.Thread(target = main).start()
        [i.start() for i in thread_list]

    def listenToClient(self,t_id, client, addr,name):
        global turn_count,N,player,bot,pos,map_size,contorled,in_turn,notif,processing,acting,thread_list
        size = 1024
        client.send((player+' '+bot).encode('ascii'))
        msg = ' '.join(pos_to_strlist())
        #print("sending%s : %s"%(addr,msg))
        client.send(msg.encode('ascii'))
        while True:
            try:
                msg = client.recv(size).decode('ascii')
                if msg:
                    if msg =='-':
                        client.close()
                        N -= 1
                        if N == 0:
                            print("YOU WIN!!")
                            sys.exit("YOU WIN!!")
                        break
                    act = msg.split()
                    contorled = '%s%s'%(contorled,''.join([i[0].upper() for i in act if i[1].upper() == 'M' and i[0]!=i[3]]))
                    #if in_turn :
                    #    print("Waiting (%d/%d)"%(turn_count+1,N))
                    [i.join() for i in thread_list]
                    turn_count += 1
                    

                    while not in_turn :
                        pass

                    [i.join() for i in thread_list]

                    action(act)
                    acting +=1
                    while processing :
                        pass
                    msg = ' '.join(notif)+','+' '.join(pos_to_strlist())
                    client.send(msg.encode('ascii'))
                    
                    #print("sending data(%d/%d)"%(turn_count,N))
                    turn_count -= 1
                    [i.join() for i in thread_list]

                    #print("NEXT")
                else:
                    raise error('Client disconnected')
            except:
                client.close()
                return False

def main():
    global in_turn,turn_count,N,CARD,card_name,card_used,deck,bot,player,notif,contorled,cursed,acting,processing,history,item_name
    while True:
        if len(bot) == 0:
            print("You Lose..")
            break
        while True:
            print("Total Bot-Player : %d-%d"%(len(bot),N))
            print_map(pos_to_strlist())
            print("CARD :")
            if len(deck)> 0 :
                print(" - [A]dd.")
            else :
                print("Deck is Empty")
            for i in sorted(CARD):
                if CARD[i]>0:
                    print(' -',card_name[i],'x%d'%CARD[i])
            print(" - End[.]")

            x = input(" -> ").upper()
            #x = 'E'
            if N == 0:
                break
            if x == '':
                continue
            if x == 'A' and len(deck)>0:
                add_card()
                break
            elif x == 'R' and CARD[x]>0:
                CARD[x]-=1
                deck.extend(card_used)
                card_used = []
                print("Return used card to deck")
                break
            elif x == 'D' and CARD[x]>0:
                CARD[x]-=1
                card_used.append(x)
                print("Double draw")
                add_card()
                add_card()
            elif x == 'U' and CARD[x]>0:
                CARD[x]-=1
                card_used.append(x)
                cursed = ''
                print("Uncursed")
                notif.append('U')
            elif x == 'H' and CARD[x]>0:
                CARD[x]-=1
                card_used.append(x)
                print("History >>")
                for i in sorted(history):
                    if history[i]>0:
                        print(' ',item_name[i],'x%d'%history[i])
                notif.append('H')
            elif x[0] == 'K' and CARD['K']>0:
                x = x[1:]
                all_ = sorted(bot+player)
                if len(x)>0:
                    i = x[0]
                    x = x[1:]
                else :
                    print(all_)
                    i = input(" -> ").upper()
                    if i == '..' :
                        continue
                print("\'%s\'"%i)
                if i in [j for j in all_]:
                    CARD['K']-=1
                    card_used.append('K')
                    action(['_K'+i])
                    print("Kill",i)
                    break
                else :
                    print("INPUT ERROR: please try again")
                    continue
            elif x[0] == 'C' and CARD['C']>0 :
                x = x[1:]
                if x =='':
                    print(sorted(bot+player))
                    x = input(" -> ").upper()
                    if x == '..' :
                        continue
                CARD['C']-=1
                card_used.append('C')
                print("Chain kill \'%s\'"%x)
                for i in x:
                    if i in player :
                        action(['_K'+i])
                    elif i in bot :
                        action(['_K'+i])
                        break
                    else :
                        break
                break
            elif '1'<=x<='9' and CARD[x]>0:
                CARD[x] -= 1
                card_used.append(x)
                print("Detection %s >>"%x,"YES" if detect_zone(x) else "NO")
                break
            elif x == '.':
                break
            else :
                print("INPUT ERROR: please try again")
        if N == 0:
            break
        for i in history:
            history[i] =0 
        in_turn = True
        print("Waiting")
        #print("Waiting (%d/%d)"%(turn_count,N))

        while turn_count < N :
            pass

        while acting < N :
            pass
        acting = 0
        move_bot()
        sent_item()
        add_item()
        processing = False

        while turn_count > 0:
            pass

        in_turn = False
        processing = True
        contorled = ''
        print("NEXT")
        print_notif(notif)
        notif = []


print("HOST name is \'%s\'"%socket.gethostname())
N = int(input("Number of Player = "))
#N = 1
create_bot(N+1)
print("Waiting for Player")
port = 9999
ThreadedServer('',port).listen()