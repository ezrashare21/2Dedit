import sys, os

argv = sys.argv

if len(argv) != 3:
    sys.exit()

file = "data/programs/" + str(argv[2])
mode = str(argv[1])

if not (mode == "new" or mode == "open"):
    sys.exit()

if mode == "open":
    try:
        if not os.path.isfile(file):
            sys.exit()
    except:
        sys.exit()
else:
    try:
        if os.path.isfile(file) or os.path.exists(file): sys.exit()
    except: sys.exit()

import pygame
from pygame.locals import *

pygame.init()
screen = pygame.display.set_mode((700,500))
pygame.display.set_caption("2DEdit")

font = pygame.font.Font('data/font.ttf', 15)

black = (0,0,0)
white = (255,255,255)
green = (54, 255, 74)
red = (237, 237, 237)

def deferror():
    raise Exception('error', 'deferror')
def renderText(text,pos,color):
    text = font.render(text, True, color)
    screen.blit(text, pos)

pointerx = 0
pointery = 0

scrollx = 0
scrolly = 0

scrollsx = 0
scrollsy = 0

press_left = False
press_right = False
press_up = False
press_down = False

width = 3
height = 3
grid = []
for x in range(width*height):
    grid.append(" ")

def index(x,y):
    return (x+(y*width))
def gridTextRender():
    newline = -1
    string = ""
    for item in grid:
        newline+=1
        if newline > width - 2:
            extra = "\n"
            newline = -1
        else:
            extra = ""
        string += item + extra
    return string

def generate():
    global uistr
    global ui_list
    uistr = gridTextRender()
    ui_list = uistr.split('\n')[:len(uistr.split('\n'))-1]

ui_list = []
uistr = ""
keynum = 0
generate()
press_shift = False
press_alt = False

def convertNS(array):
    con = []
    num = 0
    for x in array:
        num += 1
        if num != len(array):
            con.append("".join(list(x)[:len(x)-1]))
        else:
            con.append(x)
    return con

def getfile(file):
    try: return convertNS(open(file).readlines())
    except: return []

def load_get():
    return getfile(file)

def get_grid():
    nx = width
    ny = -1
    result = []
    for x in grid:
        nx += 1
        if nx > width-1:
            nx = 0
            ny += 1
            result.append([])
        result[len(result)-1].append(x)
    return result

def set_grid(new_grid):
    global grid
    grid = []
    for x in new_grid:
        for y in x:
            grid.append(y)

def save_file():
    global mode
    global file
    if mode == "new":
        open(file,"x")
        mode = "saved_new"
    open(file,"w").write("")
    num = 0
    for x in ui_list:
        num += 1
        if num == len(ui_list): ex = ""
        else: ex = "\n"
        open(file,"a").write(x + ex)

def load_file():
    global grid
    grid = []
    for item in load_get():
        for x in item:
            grid.append(x)
    get_gr = load_get()
    
    global width
    global height
    width = len(get_gr[0])
    height = len(get_gr)
    
    generate()

# this was made by ezrashare21 :) github.com/ezrashare21/2Dedit

if mode == "open":
    load_file()

presskey_save = [False, False]

while True:
    screen.fill(white)
    keydown = None
    pressed_shift = False
    pressed_alt = False
    
    #caption
    if load_get() != ui_list: extra = "*"
    else: extra = ""
    
    pygame.display.set_caption("2DEdit " + file + extra)
    
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            
            #width
            if press_shift:
                if event.key == K_RIGHT: press_right = True
                if event.key == K_LEFT: press_left = True
                if event.key == K_DOWN: press_down = True
                if event.key == K_UP: press_up = True
            else:
                if event.key == K_RIGHT:
                    edit_grid = get_grid()
                    width += 1
                    n = -1
                    for x in edit_grid:
                        n += 1
                        edit_grid[n].append(" ")
                    set_grid(edit_grid)
                    generate()
                if event.key == K_LEFT:
                    if width > 3:
                        edit_grid = get_grid()
                        width -= 1
                        n = -1
                        for x in edit_grid:
                            n += 1
                            edit_grid[n].pop()
                        set_grid(edit_grid)
                        generate()
                
                #height
                if event.key == K_DOWN:
                    edit_grid = get_grid()
                    height += 1
                    edit = len(edit_grid)
                    edit_grid.append([])
                    for n in range(width):
                        edit_grid[edit].append(" ")
                    set_grid(edit_grid)
                    generate()
                
                if event.key == K_UP:
                    if height > 3:
                        edit_grid = get_grid()
                        height -= 1
                        edit_grid.pop()
                        set_grid(edit_grid)
                        generate()
            #change char and save and stuff
            if event.key == K_LSHIFT or event.key == K_RSHIFT: press_shift = True
            if event.key == K_LALT or event.key == K_RALT: press_alt = True
            
            if event.key == K_LCTRL: presskey_save[0] = True
            if event.key == K_s: presskey_save[1] = True
            
            if event.key == K_BACKSPACE:
                grid[index(pointerx,pointery)] = " "
                generate()
            keys = list("poiuytrewqlkjhgfdsamnbvcxz/.,';\\][=-0987654321`")
            n = -1
            for key in keys:
                n += 1
                if event.key == pygame.key.key_code(key):
                    keydown = key
                    keynum = n
        if event.type == KEYUP:
            if event.key == K_LSHIFT or event.key == K_RSHIFT: press_shift = False
            if event.key == K_LALT or event.key == K_RALT: press_alt = False
            
            if event.key == K_RIGHT: press_right = False
            if event.key == K_LEFT: press_left = False
            if event.key == K_DOWN: press_down = False
            if event.key == K_UP: press_up = False
            
            if event.key == K_LCTRL: presskey_save[0] = False
            if event.key == K_s: presskey_save[1] = False
        #end of events
    
    if presskey_save[0] and keydown == "s":
        keydown = None
    
    if presskey_save[0] and presskey_save[1]:
        save_file()
    
    pressed_alt = press_alt
    pressed_shift = press_shift
    
    if pressed_shift and keydown != None:
        keys = list("POIUYTREWQLKJHGFDSAMNBVCXZ?><\":|}{+_)(*&^%$#@!~")
        keydown = keys[keynum]
    if pressed_alt and keydown != None:
        keys = list("--------^------->v<-----------------------------")
        keydown = keys[keynum]
    
    #data
    speed = 3
    if press_right: scrollsx += speed
    if press_left: scrollsx -= speed
    if press_down: scrollsy += speed
    if press_up: scrollsy -= speed
    
    scrollx -= scrollsx
    scrolly -= scrollsy
    
    scrollsx = scrollsx * 0.8
    scrollsy = scrollsy * 0.8
    
    #mouse
    
    charwidth = 36
    charheight = 36
    
    mousepos = pygame.mouse.get_pos()
    
    mousepos = list(mousepos)
    
    mousepos[0] -= scrollx
    mousepos[1] -= scrolly
    
    oldx = pointerx
    oldy = pointery
    
    pointerx = round((mousepos[0]-20)/(charwidth/2))
    pointery = round((mousepos[1]-20)/(charheight/2))
    
    try:
        var = grid[index(pointerx,pointery)]
        if pointerx > width-1:
            deferror()
        elif pointerx < 0:
            deferror()
        elif index(pointerx,pointery) < 0:
            deferror()
    except:
        pointerx = oldx
        pointery = oldy
    
    if keydown != None:
        grid[index(pointerx,pointery)] = keydown
        generate()
    
    #render
    
    number = -1
    for item in ui_list:
        number += 1
        number1 = -1
        for char in item:
            number1 += 1
            if number == pointery and number1 == pointerx:
                back = green
            else:
                back = red
            pygame.draw.rect(screen, back, (10+(number1*charwidth/2)+scrollx,(10+(number*charheight/2))+scrolly,charwidth/2,charheight/2))
            renderText(char,(10+(number1*(charwidth/2))+scrollx,(8+(number*(charheight/2)))+scrolly),black)
    
    pygame.display.update()
    pygame.time.Clock().tick(30)