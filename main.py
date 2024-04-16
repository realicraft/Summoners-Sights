import sys, os, random, math, pygame, json
import pygame.surface, pygame.color, pygame.rect, pygame.image, pygame.font, pygame.time, pygame.display, pygame.draw, pygame.event, pygame.key, pygame.transform # mostly for syntax highlighting
import tkinter.filedialog, tkinter # only for the open/save file dialogue
pygame.init()

SIZE = WIDTH, HEIGHT = 640, 480
SIZER = WIDTHR, HEIGHTR = 320, 240

# define colors
BLACK =   pygame.Color(0x00, 0x00, 0x00)
RED =     pygame.Color(0xff, 0x00, 0x00)
ORANGE =  pygame.Color(0xff, 0x7f, 0x00)
YELLOW =  pygame.Color(0xff, 0xff, 0x00)
GREEN =   pygame.Color(0x00, 0xff, 0x00)
CYAN =    pygame.Color(0x00, 0xff, 0xff)
BLUE =    pygame.Color(0x00, 0x00, 0xff)
PURPLE =  pygame.Color(0x7f, 0x00, 0xff)
MAGENTA = pygame.Color(0xff, 0x00, 0xff)
WHITE =   pygame.Color(0xff, 0xff, 0xff)
GRAY =    pygame.Color(0x7f, 0x7f, 0x7f)
BGCOLOR = pygame.Color(0xe6, 0xf2, 0xff)
OVERBG  = pygame.Color(0x2f, 0x2f, 0x2f)

DRED =    pygame.Color(0x7f, 0x00, 0x00)

BGSEL   = pygame.Color(0xe6, 0xe6, 0xcf) # yeah i copied some boilerplate from harvester.
PLOTBR  = pygame.Color(0x66, 0x33, 0x00) # what're you gonna do about it
PLOTWW  = pygame.Color(0x7f, 0x3f, 0x00)
PLOTNW  = pygame.Color(0xcc, 0x99, 0x66)

TBOUTER = pygame.Color(0x5f, 0x5f, 0x5f)
TBINNER = pygame.Color(0xaf, 0xaf, 0xaf)

TRANSPARENT = pygame.Color(0x00, 0x00, 0x00, 0x00)

# define the framerate and values based on it
FRAMERATE = 60
FRAMERATE8 = int(FRAMERATE*0.8)
FRAMERATE15 = FRAMERATE*15
FRAMERATE30 = FRAMERATE*30
currentFrame = 0

def loadFromPath(path: str, file: str) -> pygame.surface.Surface:
    # https://stackoverflow.com/a/54926684
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return pygame.image.load(os.path.join(base_path, path, file))

def getSummonImageList(folder: str) -> list[pygame.surface.Surface]:
    return [
        loadFromPath("assets/summons/"+folder, "unaligned.png"),
        loadFromPath("assets/summons/"+folder, "fire.png"),
        loadFromPath("assets/summons/"+folder, "plant.png"),
        loadFromPath("assets/summons/"+folder, "water.png"),
        loadFromPath("assets/summons/"+folder, "electric.png"),
        loadFromPath("assets/summons/"+folder, "ice.png"),
        loadFromPath("assets/summons/"+folder, "ground.png"),
    ]
def getItemImage(item: str, folder: str=None) -> pygame.surface.Surface:
    if (folder is not None):
        return loadFromPath("assets/items/"+folder, item+".png")
    else:
        return loadFromPath("assets/items", item+".png")

SUMMONLIST = [ #[name, difficulty, exp curve*, [hp, atk, def, spd]**, [images]]
    # * a value of 10 means that the summon needs 10 exp to "reach" lvl 1, 10^(6/5) to reach lvl 2, 10^(7/5) to reach lvl 3, 10^(8/5) to reach lvl 4, 10^(9/5) to reach level 5, etc.
    # ** at level 10
    ["Slime", 3, 10, [40, 12, 7, 8], getSummonImageList("slime")], # 0
]

ITEMLIST = [ #[name, description, image, buy price, sell price*, {attributes}]
    # * 0 means unsellable
    ["Fire Shard", "A shard of Fire energy. It's used in the process of aligning a summon to Fire.", getItemImage("fire_shard", "shards"), 50, 40, {"shard": 1}], # 0
    ["Plant Shard", "A shard of Plant energy. It's used in the process of aligning a summon to Plant.", getItemImage("plant_shard", "shards"), 50, 40, {"shard": 2}], # 1
    ["Water Shard", "A shard of Water energy. It's used in the process of aligning a summon to Water.", getItemImage("water_shard", "shards"), 50, 40, {"shard": 3}], # 2
    ["Electric Shard", "A shard of Electric energy. It's used in the process of aligning a summon to Electric.", getItemImage("electric_shard", "shards"), 50, 40, {"shard": 4}], # 3
    ["Ice Shard", "A shard of Ice energy. It's used in the process of aligning a summon to Ice.", getItemImage("ice_shard", "shards"), 50, 40, {"shard": 5}], # 4
    ["Ground Shard", "A shard of Ground energy. It's used in the process of aligning a summon to Ground.", getItemImage("ground_shard", "shards"), 50, 40, {"shard": 6}], # 5
    ["Gear", "A small gear.", getItemImage("gear"), 0, 20, {}], # 6
    ["Parchment", "A sheet of old parchment.", getItemImage("parchment"), 0, 12, {}], # 7
    ["Red Crystal", "A stick of red crystal.", getItemImage("red_crystal", "crystals"), 0, 15, {}], # 8
    ["Orange Crystal", "A stick of orange crystal.", getItemImage("orange_crystal", "crystals"), 0, 15, {}], # 9
    ["Yellow Crystal", "A stick of yellow crystal.", getItemImage("yellow_crystal", "crystals"), 0, 15, {}], # 10
    ["Green Crystal", "A stick of green crystal.", getItemImage("green_crystal", "crystals"), 0, 15, {}], # 11
    ["Cyan Crystal", "A stick of cyan crystal.", getItemImage("cyan_crystal", "crystals"), 0, 15, {}], # 12
    ["Blue Crystal", "A stick of blue crystal.", getItemImage("blue_crystal", "crystals"), 0, 15, {}], # 13
    ["Purple Crystal", "A stick of purple crystal.", getItemImage("purple_crystal", "crystals"), 0, 15, {}], # 14
    ["White Crystal", "A stick of white crystal.", getItemImage("white_crystal", "crystals"), 0, 15, {}], # 15
    ["Pebble", "A small pebble.", getItemImage("pebble"), 0, 5, {}], # 16
    ["Blank Scroll", "A blank scroll. It can be attuned to a Summon over time.", getItemImage("blank_scroll", "scrolls"), 20, 15, {"scroll": 0}], # 17
    ["Partially Attuned Scroll", "A scroll that's in the process of being attuned to a %1.", getItemImage("partial_scroll", "scrolls"), 0, 0, {"scroll": 1}], # 18
    ["Attuned Scroll", "A scroll that's been attuned to a %1.", getItemImage("attuned_scroll", "scrolls"), 0, 0, {"scroll": 2}], # 19
    ["Twig", "A small twig.", getItemImage("twig"), 0, 5, {}], # 20
    ["Empty Bottle", "A bottle made of glass. Stuff can be put inside it.", getItemImage("empty_bottle", "bottles"), 10, 8, {"bottle": 0}], # 21
    ["Bottle of Water", "A bottle filled with water.", getItemImage("water_bottle", "bottles"), 0, 12, {"bottle": 1, "consume": 4}], # 22
    ["Bottle of Mud", "A bottle filled with mud.", getItemImage("mud_bottle", "bottles"), 0, 0, {"bottle": 1}], # 23
    ["Strawberry", "A small strawberry. A Summon that eats this will restore up to 5 HP.", getItemImage("strawberry"), 0, 3, {"consume": 5}], # 24
    ["Blueberry", "A small blueberry. A Summon that eats this will restore up to 4 HP.", getItemImage("blueberry"), 0, 3, {"consume": 4}], # 25
    ["Iron Nugget", "A small nugget of iron.", getItemImage("iron_nugget"), 0, 25, {}], # 26
    ["Gold Nugget", "A small nugget of gold.", getItemImage("gold_nugget"), 0, 40, {}], # 27
    ["Shard of Glass", "A small shard of glass.", getItemImage("glass_shard"), 0, 0, {}], # 28
    ["Red Flower", "A small, red flower.", getItemImage("red_flower"), 0, 2, {}], # 29
    ["Blue Flower", "A small, blue flower.", getItemImage("blue_flower"), 0, 2, {}], # 30
    ["Strip of Bark", "A strip of tree bark.", getItemImage("bark"), 0, 0, {}], # 31
]

ALIGNLIST = [ #[name, image]
    ["Unaligned", loadFromPath("assets/ui/aligns/", "unaligned.png")], # 0
    ["Fire", loadFromPath("assets/ui/aligns/", "fire.png")], # 1
    ["Plant", loadFromPath("assets/ui/aligns/", "plant.png")], # 2
    ["Water", loadFromPath("assets/ui/aligns/", "water.png")], # 3
    ["Electric", loadFromPath("assets/ui/aligns/", "electric.png")], # 4
    ["Ice", loadFromPath("assets/ui/aligns/", "ice.png")], # 5
    ["Ground", loadFromPath("assets/ui/aligns/", "ground.png")], # 6
]

TILELIST = [ # [icon, collide?]
    [loadFromPath("assets/tiles/", "grass.png"), False], # 0
    [loadFromPath("assets/tiles/", "path_h.png"), False], # 1
    [loadFromPath("assets/tiles/", "path_v.png"), False], # 2
    [loadFromPath("assets/tiles/", "path_rd.png"), False], # 3
    [loadFromPath("assets/tiles/", "path_ld.png"), False], # 4
    [loadFromPath("assets/tiles/", "path_ru.png"), False], # 5
    [loadFromPath("assets/tiles/", "path_lu.png"), False], # 6
    [loadFromPath("assets/tiles/", "path_vl.png"), False], # 7
    [loadFromPath("assets/tiles/", "path_vr.png"), False], # 8
    [loadFromPath("assets/tiles/", "path_hu.png"), False], # 9
    [loadFromPath("assets/tiles/", "path_hd.png"), False], # 10
    [loadFromPath("assets/tiles/", "path_all.png"), False], # 11
    [loadFromPath("assets/tiles/", "shrub_ul.png"), True], # 12
    [loadFromPath("assets/tiles/", "shrub_u.png"), True], # 13
    [loadFromPath("assets/tiles/", "shrub_ur.png"), True], # 14
    [loadFromPath("assets/tiles/", "shrub_l.png"), True], # 15
    [loadFromPath("assets/tiles/", "shrub.png"), True], # 16
    [loadFromPath("assets/tiles/", "shrub_r.png"), True], # 17
    [loadFromPath("assets/tiles/", "shrub_dl.png"), True], # 18
    [loadFromPath("assets/tiles/", "shrub_d.png"), True], # 19
    [loadFromPath("assets/tiles/", "shrub_dr.png"), True], # 20
    [loadFromPath("assets/tiles/", "path_el.png"), False], # 21
    [loadFromPath("assets/tiles/", "path_er.png"), False], # 22
    [loadFromPath("assets/tiles/", "path_eu.png"), False], # 23
    [loadFromPath("assets/tiles/", "path_ed.png"), False], # 24
]

MAPLIST = [ # [name, [width, height], [spawn], [[tile, ...], ...], [exits* - l u r d]]
    # * -1 represents no exit
    [ # 0 - debug map
        "Debug",
        [8, 8],
        [1, 1],
        [
            [ 0,  0,  3,  1,  1,  1,  4,  0],
            [ 0,  0,  2, 12, 13, 14,  2,  0],
            [ 0,  0,  2, 15, 16, 17,  2,  0],
            [ 0,  0,  2, 18, 19, 20,  2,  0],
            [ 0, 23,  5,  1, 10,  1,  6,  0],
            [ 0,  2,  0,  0,  2,  0,  0,  0],
            [21,  9,  1,  1, 11, 22,  0,  0],
            [ 0,  0,  0,  0, 24,  0,  0,  0],
        ],
        [0, 0, 0, -1]
    ], # 0 - debug map
]

PLAYERSPRITELIST = [ # down, right, up, left
    [loadFromPath("assets/player/", "down1.png"), loadFromPath("assets/player/", "down2.png"), loadFromPath("assets/player/", "down3.png")],
    [loadFromPath("assets/player/", "right1.png"), loadFromPath("assets/player/", "right2.png"), loadFromPath("assets/player/", "right3.png")],
    [loadFromPath("assets/player/", "up1.png"), loadFromPath("assets/player/", "up2.png"), loadFromPath("assets/player/", "up3.png")],
    [loadFromPath("assets/player/", "left1.png"), loadFromPath("assets/player/", "left2.png"), loadFromPath("assets/player/", "left3.png")]
]

MAINFONT24 = pygame.font.SysFont("Arial", 48)
MAINFONT16 = pygame.font.SysFont("Arial", 32)
MAINFONT12 = pygame.font.SysFont("Arial", 24)
MAINFONT10 = pygame.font.SysFont("Arial", 20)
MAINFONT8 = pygame.font.SysFont("Arial", 16)
MAINFONT6 = pygame.font.SysFont("Arial", 12)

# the summons that you have
summons = [ #[id*, element, level, exp, current hp, [stat multis**]]
    # * an id of -1 means the slot is empty
    # ** a value from 0.9 to 1.1 that is multiplied with the stat to add randomness
]

# the summons in your storages
storageSummons = [ # same as summons, split into four pages of fourty
    [],[],[],[]
]

# your items
bag = [ # [id, nbt, count]
]

SCREEN = pygame.display.set_mode(SIZE)
screenr = pygame.surface.Surface(SIZER)

pygame.display.set_caption("Summoner's Sights")
#pygame.display.set_icon(CROPLIST[1][5][0])

clock = pygame.time.Clock()

textbox = pygame.Rect(40, 348, 560, 92)
textnextimg = loadFromPath("assets/ui", "dialogue_next.png")

menubox = pygame.Rect(520, 20, 100, 120)

money = 0

state = "T" # T for title, O for overworld, B for battle, M for menu

menuType = "N" # N for none, P for party, B for bag, S for save
menuOpen = False # is the pop up menu open?
menuSelection = 0 # 0 for party, 1 for boxes, 2 for save, 3 for quit

titleOption = "T" # T for title, F for continue, S for settings, C for credits
titleSelection = 0 # 0 for continue, 1 for settings, 2 for credits, 3 for quit

textbox_queue = [] # queue of textboxes
textbox_visible = False
textbox_planned = "" # final text to display in the textbox
textbox_current = "" # current text in the textbox
textbox_wait = 0 # frames to wait until adding more text
TEXTBOX_WAIT_TIMES = {",": 10, ".": 20, "?": 20, "!": 20, ":": 15, ";": 5, "\n": 3} # characters not in this list default to 1

KEY_TO_CHAR_UNSHIFTED = {pygame.K_a: "a", pygame.K_b: "b", pygame.K_c: "c", pygame.K_d: "d", pygame.K_e: "e", pygame.K_f: "f", 
                         pygame.K_g: "g", pygame.K_h: "h", pygame.K_i: "i", pygame.K_j: "j", pygame.K_k: "k", pygame.K_l: "l", 
                         pygame.K_m: "m", pygame.K_n: "n", pygame.K_o: "o", pygame.K_p: "p", pygame.K_q: "q", pygame.K_r: "r", 
                         pygame.K_s: "s", pygame.K_t: "t", pygame.K_u: "u", pygame.K_v: "v", pygame.K_w: "w", pygame.K_x: "x", 
                         pygame.K_y: "y", pygame.K_z: "z", pygame.K_0: "0", pygame.K_1: "1", pygame.K_2: "2", pygame.K_3: "3", 
                         pygame.K_4: "4", pygame.K_5: "5", pygame.K_6: "6", pygame.K_7: "7", pygame.K_8: "8", pygame.K_9: "9", 
                         pygame.K_BACKQUOTE: "`", pygame.K_MINUS: "-", pygame.K_EQUALS: "=", pygame.K_LEFTBRACKET: "[", pygame.K_RIGHTBRACKET: "]", pygame.K_BACKSLASH: "\\", 
                         pygame.K_SEMICOLON: ";", pygame.K_QUOTE: "'", pygame.K_COMMA: ",", pygame.K_PERIOD: ".", pygame.K_SLASH: "/",
}
KEY_TO_CHAR_SHIFTED = {pygame.K_a: "A", pygame.K_b: "B", pygame.K_c: "C", pygame.K_d: "D", pygame.K_e: "E", pygame.K_f: "F", 
                       pygame.K_g: "G", pygame.K_h: "H", pygame.K_i: "I", pygame.K_j: "J", pygame.K_k: "K", pygame.K_l: "L", 
                       pygame.K_m: "M", pygame.K_n: "N", pygame.K_o: "O", pygame.K_p: "P", pygame.K_q: "Q", pygame.K_r: "R", 
                       pygame.K_s: "S", pygame.K_t: "T", pygame.K_u: "U", pygame.K_v: "V", pygame.K_w: "W", pygame.K_x: "X",                        
                       pygame.K_y: "Y", pygame.K_z: "Z", pygame.K_0: ")", pygame.K_1: "!", pygame.K_2: "@", pygame.K_3: "#", 
                       pygame.K_4: "$", pygame.K_5: "%", pygame.K_6: "^", pygame.K_7: "&", pygame.K_8: "*", pygame.K_9: "(", 
                       pygame.K_BACKQUOTE: "~", pygame.K_MINUS: "_", pygame.K_EQUALS: "+", pygame.K_LEFTBRACKET: "{", pygame.K_RIGHTBRACKET: "}", pygame.K_BACKSLASH: "|", 
                       pygame.K_SEMICOLON: ":", pygame.K_QUOTE: "\"", pygame.K_COMMA: "<", pygame.K_PERIOD: ">", pygame.K_SLASH: "?",
}

currentMap = -1 # current map id; set to -1 on the title screen
currentPos = [0, 0] # current position in map (tile)
direction = 0 # 0 is down, 1 is right, 2 is up, 3 is left
moving = False

# is (x, y) within (x1, y1, x2, y2)?
def isPosWithin(pos: tuple[int, int], bounds: tuple[int, int, int, int]) -> bool:
    return ((pos[0] >= bounds[0]) and (pos[0] <= bounds[2])) and ((pos[1] >= bounds[1]) and (pos[1] <= bounds[3]))

def initData() -> None:
    global summons, storageSummons, bag, money, currentMap, currentPos
    # initialize summons
    summons = []
    summons.append([0, 0, 1, 0, 4, [1, 1, 1, 1]]) # you start with a Lv. 1 Slime
    for i in range(4):
        summons.append([-1, 0, 1, 0, 1, [1, 1, 1, 1]])
    # initialize storage summons
    for i in range(4):
        storageSummons[i] = []
        for j in range(40):
            storageSummons[i].append([-1, 0, 1, 0, 1, [1, 1, 1, 1]])
    # initialize bag
    bag = []
    # initialize money
    money = 0
    # initialze map
    currentMap = 1
    # initialize position
    currentPos = [0, 0]
    

# save game, returning if the file was saved
def saveGame() -> bool:
    out = {}
    out["game"] = "Summoner's Sights"
    out["version"] = "LD55"
    out["summons"] = summons
    out["storageSummons"] = storageSummons
    out["bag"] = bag
    out["money"] = money
    out["currentMap"] = currentMap
    out["currentPos"] = currentPos
    root = tkinter.Tk() # https://stackoverflow.com/a/1407700
    root.withdraw()
    filename = tkinter.filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON", "*.json")], initialdir=os.path.join("saves"))
    root.destroy()
    if filename != "":
        with open(filename, "w") as file:
            file.write(json.dumps(out))
        return True
    else: return False

# load game, returning if the file was loaded
def loadGame() -> bool:
    global summons, storageSummons, bag, money, currentMap, currentPos
    root = tkinter.Tk() # https://stackoverflow.com/a/1407700
    root.withdraw()
    filename = tkinter.filedialog.askopenfilename(defaultextension=".json", filetypes=[("JSON", "*.json")], initialdir=os.path.join("saves"))
    root.destroy()
    if filename != "":
        with open(filename, "r") as file:
            save = json.loads(file.read())
            summons = save["summons"]
            storageSummons = save["storageSummons"]
            bag = save["bag"]
            money = save["money"]
            currentMap = save["currentMap"]
            currentPos = save["currentPos"]
        return True
    else: return False

# textbox functions
def drawTextbox() -> None:
    global textbox_current, textbox_planned, textbox_wait, textbox_visible, currentFrame
    draw_arrow = False
    if (textbox_wait > 0):
        textbox_wait -= 1
    else:
        if (len(textbox_current) < len(textbox_planned)):
            next_char = textbox_planned[len(textbox_current)]
            textbox_current += next_char
            if (next_char in TEXTBOX_WAIT_TIMES):
                textbox_wait = TEXTBOX_WAIT_TIMES[next_char]
            else:
                textbox_wait = 1
        else:
            draw_arrow = True
    pygame.draw.rect(SCREEN, TBINNER, textbox)
    pygame.draw.rect(SCREEN, TBOUTER, textbox, 4)
    lines = textbox_current.split("\n")
    for line in range(len(lines)):
        SCREEN.blit(MAINFONT8.render(lines[line], True, BLACK), (46, 354+(20*line)))
        if draw_arrow:
            SCREEN.blit(textnextimg, (581+(int(currentFrame/15)%3), 420))
def nextTextbox() -> bool: # returns if there's still a textbox onscreen
    global textbox_current, textbox_planned, textbox_wait, textbox_visible
    textbox_queue.pop(0)
    out = True
    if len(textbox_queue) > 0:
        textbox_planned = textbox_queue[0] # if there's a textbox in the queue, use it
        out = True
    else: # otherwise, hide the textbox
        textbox_planned = ""
        textbox_visible = False
        out = False
    textbox_current = ""
    textbox_wait = 0
    return out
def queueTextboxes(queue: list[str]) -> None:
    global textbox_queue, textbox_visible, textbox_planned
    if (len(queue) > 0):
        if (len(textbox_queue) == 0):
            textbox_planned = queue[0]
        textbox_queue.extend(queue)
        textbox_visible = True

# draw menu
def drawMenu() -> None:
    pygame.draw.rect(SCREEN, WHITE, menubox)
    pygame.draw.rect(SCREEN, BLACK, menubox, 4)
    SCREEN.blit(MAINFONT10.render("Party", True, DRED), (538, 30))
    SCREEN.blit(MAINFONT10.render("Boxes", True, DRED), (538, 55))
    SCREEN.blit(MAINFONT10.render("Save", True, BLACK), (538, 80))
    SCREEN.blit(MAINFONT10.render("Quit", True, BLACK), (538, 105))
    if debug: SCREEN.blit(MAINFONT6.render("Options in red are not available.", True, WHITE, BLACK), (460, 0))
    SCREEN.blit(textnextimg, (524, 34+(25*menuSelection)))

# function to render the map to a Surface
def renderMap() -> pygame.surface.Surface:
    global currentMap, MAPLIST
    out = pygame.surface.Surface((16*(MAPLIST[currentMap][1][0]), 16*(MAPLIST[currentMap][1][1])))
    for r in range(MAPLIST[currentMap][1][0]):
        for c in range(MAPLIST[currentMap][1][1]):
            out.blit(TILELIST[MAPLIST[currentMap][3][c][r]][0], ((16*r), (16*c)))
    return out

def changeMap(mapID: int) -> None:
    global currentMap, currentPos
    currentMap = mapID
    currentPos[0] = 8 + (MAPLIST[currentMap][2][0]*16)
    currentPos[1] = 8 + (MAPLIST[currentMap][2][1]*16)

# functions to draw the money counter
#def drawMoney():
#    screenr.blit(coinimg, (4,4))
#def drawMoneyText():
#    SCREEN.blit(MAINFONT16.render(str(money), True, BLACK, BGCOLOR), (48, 8))

# function to draw the framerate
def drawFR() -> None:
    SCREEN.blit(MAINFONT10.render(str(int(clock.get_fps())), True, BLACK), (4, 456))


initData() # initialize data before starting the event loop

debug = True # if True, allow debug options
# EVENT LOOP #
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # mouse click
            pass
        elif event.type == pygame.KEYDOWN:
            # key press
            if (event.key == pygame.K_m):
                if (debug):
                    money += 50
            elif (event.key == pygame.K_q):
                if (debug):
                    if (pygame.key.get_mods() & pygame.KMOD_SHIFT): # if shift held...
                        sys.exit() # ...exit immediately
                    else:
                        state = "T"
            elif (event.key == pygame.K_s):
                if (debug):
                    saveGame()
            elif (event.key == pygame.K_t):
                if (debug):
                    queueTextboxes(["Debug string.\nLine 2.\nCharacter tests: abc, abc. abc? abc! abc: abc;\nLine 4.", "Textbox 2.\nPress Enter to advance."])
            elif (event.key == pygame.K_RETURN):
                if (textbox_visible) and (len(textbox_current) == len(textbox_planned)): # if there's a textbox onscreen, and it's finished, advance it
                    nextTextbox()
                if state == "T":
                    if titleOption == "T":
                        if titleSelection == 3: # quit
                            sys.exit()
                        else:
                            titleOption = ["F", "S", "C"][titleSelection]
                            titleSelection = 0
                    elif titleOption == "F":
                        if titleSelection == 0: # new game
                            initData()
                            titleSelection = 0
                            titleOption = "T"
                            state = "O"
                            changeMap(0)
                        elif titleSelection == 1: # load file
                            if (loadGame()): # ask to load a file; false is returned if canceled
                                titleSelection = 0
                                titleOption = "T"
                                state = "O"
                                changeMap(currentMap)
                        elif titleSelection == 2: # back
                            titleSelection = 0
                            titleOption = "T"
                    elif titleOption == "S":
                        titleOption = "T"
                    elif titleOption == "C":
                        titleOption = "T"
                elif state == "O":
                    if menuOpen:
                        if menuSelection == 0:
                            pass
                        elif menuSelection == 1:
                            pass
                        elif menuSelection == 2:
                            saveGame()
                            menuOpen = False
                            menuSelection = 1
                        elif menuSelection == 3:
                            state = "T"
                            menuOpen = False
                            menuSelection = 1
            elif (event.key == pygame.K_UP):
                if state == "T":
                    if titleOption == "T":
                        if titleSelection > 0: titleSelection -= 1
                    elif titleOption == "F":
                        if titleSelection > 0: titleSelection -= 1
                elif state == "O":
                    if menuOpen:
                        if menuSelection > 0: menuSelection -= 1
            elif (event.key == pygame.K_LEFT):
                pass
            elif (event.key == pygame.K_DOWN):
                if state == "T":
                    if titleOption == "T":
                        if titleSelection < 3: titleSelection += 1
                    elif titleOption == "F":
                        if titleSelection < 2: titleSelection += 1
                elif state == "O":
                    if menuOpen:
                        if menuSelection < 3: menuSelection += 1
            elif (event.key == pygame.K_RIGHT):
                pass
            elif (event.key == pygame.K_ESCAPE):
                if state == "O":
                    menuOpen = not menuOpen
    
    # https://stackoverflow.com/a/64611463
    keys = pygame.key.get_pressed()
    moving = False
    if keys[pygame.K_LEFT]:
        if (state == "O") and (not textbox_visible) and (not menuOpen):
            direction = 3
            moving = True
            if (currentFrame % 3 != 2):
                currentPos[0] -= 1
    if keys[pygame.K_UP]:
        if (state == "O") and (not textbox_visible) and (not menuOpen):
            direction = 2
            moving = True
            if (currentFrame % 3 != 2):
                currentPos[1] -= 1
    if keys[pygame.K_RIGHT]:
        if (state == "O") and (not textbox_visible) and (not menuOpen):
            direction = 1
            moving = True
            if (currentFrame % 3 != 2):
                currentPos[0] += 1
    if keys[pygame.K_DOWN]:
        if (state == "O") and (not textbox_visible) and (not menuOpen):
            direction = 0
            moving = True
            if (currentFrame % 3 != 2):
                currentPos[1] += 1
    # wrap positions within [-512, 1024]
    if (currentPos[0] < -512): currentPos[0] += 1536
    if (currentPos[0] > 1024): currentPos[0] -= 1536
    if (currentPos[1] < -512): currentPos[1] += 1536
    if (currentPos[1] > 1024): currentPos[1] -= 1536

    clock.tick(FRAMERATE)
    currentFrame += 1
    if state == "O":
        screenr.fill(OVERBG)
    else:
        screenr.fill(BGCOLOR)
    # pre upscale
    if state == "T":
        if titleOption == "T":
            screenr.blit(textnextimg, (84, 96+(titleSelection*25)))
        elif titleOption == "F":
            screenr.blit(textnextimg, (84, 96+(titleSelection*25)))
        elif titleOption == "S":
            screenr.blit(textnextimg, (84, 146))
        elif titleOption == "C":
            screenr.blit(textnextimg, (84, 171))
    elif state == "O":
        mapSurf = renderMap()
        screenr.blit(mapSurf, (160-(currentPos[0]), 120-(currentPos[1])))
        screenr.blit(PLAYERSPRITELIST[direction][(int(currentFrame/12)%3) if moving else 0], (152, 112))
    elif state == "B":
        pass
    elif state == "M":
        pass
    # upscale
    SCREEN.blit(pygame.transform.scale(screenr, SCREEN.get_rect().size), (0, 0))
    # post upscale
    if state == "T":
        SCREEN.blit(MAINFONT24.render("Summoner's Sights", True, BLACK), (320-(MAINFONT24.size("Summoner's Sights")[0])/2, 20))
        if titleOption == "T":
            SCREEN.blit(MAINFONT16.render("Continue", True, BLACK), (200, 190))
            SCREEN.blit(MAINFONT16.render("Settings", True, BLACK), (200, 240))
            SCREEN.blit(MAINFONT16.render("Credits", True, BLACK), (200, 290))
            SCREEN.blit(MAINFONT16.render("Quit", True, BLACK), (200, 340))
        elif titleOption == "F":
            SCREEN.blit(MAINFONT16.render("New Game", True, BLACK), (200, 190))
            SCREEN.blit(MAINFONT16.render("Load File", True, BLACK), (200, 240))
            SCREEN.blit(MAINFONT16.render("Back", True, BLACK), (200, 290))
        elif titleOption == "S":
            SCREEN.blit(MAINFONT12.render("Settings.", True, BLACK), (200, 190))
            SCREEN.blit(MAINFONT16.render("Back", True, BLACK), (200, 290))
        elif titleOption == "C":
            SCREEN.blit(MAINFONT12.render("Everything: realicraft", True, BLACK), (200, 190))
            SCREEN.blit(MAINFONT12.render("Written in PyGame 2.0.1", True, BLACK), (200, 225))
            SCREEN.blit(MAINFONT12.render("Sprites made with PikoPixel", True, BLACK), (200, 260))
            SCREEN.blit(MAINFONT16.render("Back", True, BLACK), (200, 340))
    elif state == "O":
        if (debug):
            SCREEN.blit(MAINFONT6.render("Press Q to quit. (Hold shift to exit.)", True, WHITE, BLACK), (0, 0))
            SCREEN.blit(MAINFONT6.render("Press S to save.", True, WHITE, BLACK), (0, 15))
            SCREEN.blit(MAINFONT6.render("Press T to spawn a textbox.", True, WHITE, BLACK), (0, 30))
            SCREEN.blit(MAINFONT6.render("Press M to give yourself money.", True, WHITE, BLACK), (0, 45))
            SCREEN.blit(MAINFONT6.render("Open the menu with ESC.", True, WHITE, BLACK), (0, 60))
            SCREEN.blit(MAINFONT6.render(f"Position: ({currentPos[0]}, {currentPos[1]})", True, WHITE, BLACK), (0, 425))
            SCREEN.blit(MAINFONT6.render(f"Money: {money}", True, WHITE, BLACK), (0, 440))
    elif state == "B":
        pass
    elif state == "M":
        pass

    # textbox
    if textbox_visible: drawTextbox()

    # menu popup
    if menuOpen: drawMenu()

    if (debug): drawFR()
    pygame.display.flip()