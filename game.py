import curses
import random
import time

stdscr = curses.initscr()

curses.noecho()
curses.cbreak()
stdscr.keypad(True)
stdscr.nodelay(True)
curses.curs_set(False)

maxl = curses.LINES -1
maxc = curses.COLS-1
score = 0
enemy = []
world = []
food = []

player_char = '᙭'
food_char = 'Ο'
enemy_char = 'ߡ'

enemy_speed = 0.8
food_age = 500
star_present = 0.03
enemy_count = 3
food_count = 10

player_l = player_c = 0

def in_range(x,min,max):
    if x>max:
        return max
    elif x<min:
        return min+1
    else: return x

def random_place():
    a = random.randint(0,maxl)
    b = random.randint(0,maxc)
    while world[a][b] != ' ':
        a = random.randint(0,maxl)
        b = random.randint(0,maxc)

    return a,b

def init():
    global player_c,player_l
    for i in range(0,maxl+1):
        world.append([])
        for j in range(0,maxc+1):
            world[i].append(' ' if random.random() > star_present else '.')


    for i in range(food_count):
        fl,fc = random_place()
        fa = random.randint(food_age,food_age*2)
        food.append((fl,fc,fa))

    for i in range(enemy_count):
        el,ec = random_place()
        enemy.append((el,ec))

    player_l , player_c = random_place()
  
def draw():
    
    for i in range(maxl):
        for j in range(maxc):
            stdscr.addch(i,j, world[i][j])
    #showing the food
    for f in food:
        fl,fc,fa=f
        stdscr.addch(fl,fc,food_char)

    #showing enemy
    for e in enemy:
        el,ec=e
        stdscr.addch(el,ec,enemy_char)
    #showing the player
    stdscr.addch(player_l,player_c,player_char)
    stdscr.addstr(1,1,f"Score: {score}")
    stdscr.refresh()
    
def move(c):
    global player_l,player_c
    #get one of asdw and move to that direction
    if c == 'w' and world[player_l-1][player_c] != '.':
        player_l = player_l -1
    elif c == 's'and world[player_l+1][player_c] != '.':
        player_l = player_l +1
    elif c == 'd'and world[player_l][player_c+1] != '.':
        player_c = player_c + 1
    elif c == 'a'and world[player_l][player_c-1] != '.':
        player_c = player_c -1
    player_l = in_range(player_l,0,maxl-1)
    player_c = in_range(player_c,0,maxc-1)

def check_food():
    global score
    for i in range(len(food)):
        fl,fc,fa = food[i]
        fa -=1
        if fl == player_l and fc == player_c:
            score += 10
            fl , fc = random_place()
            fa = random.randint(food_age,food_age*2)
       
        if fa <= 0:
            fl , fc = random_place()
            fa = random.randint(food_age,food_age*2)
        food[i] = (fl , fc,fa)


def check_enemy():
    global playing
    for i in range(len(enemy)):
        el,ec = enemy[i]
        if random.random() > enemy_speed:
            if el > player_l:
                el -= 1
        if random.random() >enemy_speed:
            if ec > player_c:
                ec -= 1
        if random.random() > enemy_speed:
            if el < player_l:
                el += 1
        if random.random() > enemy_speed:
            if ec < player_c:
                ec += 1
            el = in_range(el,0,maxl)
            ec = in_range(ec,0,maxc)
            enemy[i]= (el,ec)
        if el == player_l and ec == player_c:
            stdscr.addstr(maxl//2,maxc//2,'YOU DIED!')
            stdscr.refresh()
            time.sleep(3)
            playing = False

init()
playing = True
while playing:
    try:
        c = stdscr.getkey()
    except:
        c = ''
    if c in 'asdw':
        move(c)
    elif c == 'q':
        playing = False
    check_food() 
    check_enemy()
    time.sleep(0.01)
    draw()
stdscr.addstr(maxl//2-2,maxc//2-3,'Thanks for playing..')
stdscr.refresh()
time.sleep(2)
stdscr.clear()
stdscr.refresh()
