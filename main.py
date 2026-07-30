#main.py# This file is run by default when a Pico is powered on.  You can edit it to make the Pico do all kinds of fun and useful things.
#You can add comments to Python files by typing the "pound" or "hashtag" symbol followed by your text
"""Multi-line
comments
look
like
this.
With the three double quotation marks on both ends"""

#Imports
# Imports are how we tell Python which other tools and code we want to use.
import ntpTime
from time import sleep, localtime
from machine import I2C, Pin, PWM, Timer
from collections import OrderedDict

# The following imports are all defined by files present in the same directory as main.py.  You can explore how those parts work to get a deeper understanding.
from icon import Animate, Icon, Toolbar, Button, Event
from buzzer_music import music
from random import random
import framebuf
import songs
from buzz import buzzer
from saved_games import *

#Constants
# Constants are values that do not change.  Conventionally all caps
CANVAS_HEIGHT = 64
CANVAS_WIDTH = 128
SPRITE_SIZE = 16
SPRITE_X_LIMIT = CANVAS_WIDTH-SPRITE_SIZE
LETTER_WIDTH = 8 #"[Chars are] 8x8 pixels [changing not supported]" ~micropython framebuf docs
BANNER_SLEEP = 0.75
SPACER = 2


# Globals
# The following code is said to share "scope" with these global variables.
#May be set by saved file, if not, initialize
that_legal_tender = 500 if that_legal_tender is None else int(that_legal_tender)
health = 3 if health is None else int(health)
happiness = 3 if happiness is None else int(happiness)
energy = 3 if energy is None else int(energy)
inventory = [] if inventory is None else inventory
wifi_pass ='Nice Try'
volume = 1000 #of 2512



# Pin mappings & hardware config
# Buttons
button_a = Button(7, Pin.PULL_UP)
button_b = Button(11, Pin.PULL_UP)
button_x = Button(15, Pin.PULL_UP)

#Piezo buzzer
buzzer_pin = Pin(19)

#OLED        DOUBLE CHECK YOUR GND AND VCC CONNECTIONS!  They differ by manufacturer and may not match pictures in materials.
sda = Pin(16)
scl = Pin(17)

#OLED hardware options
supported_screens = ['ssd1306', 'sh1106']  #TODO: Untested with sh1106, but may be useful to others as a starting point for further development.
screen_used = supported_screens[0]         #HEADS UP!  You will need to change this to "screen_used = supported_screens[1]" if you are using the sh1106


# I2C is a communication protocol that allows devices to transfer info using just two wires, plus shared power connections.
# In this project, I2C allows the Pico to send images and commands to the display and bring our pet to life!

#Connect to the OLED screen
i2c = I2C(id = 0, scl = scl, sda = sda, freq = 400000) #i2c port 0 => id=0

if screen_used == supported_screens[0]:  # Create the right kind of oled display so our commands work correctly on each.
    from ssd1306 import SSD1306_I2C
    oled = SSD1306_I2C(width=CANVAS_WIDTH, height=CANVAS_HEIGHT, i2c=i2c)
elif screen_used == supported_screens[1]:
    from sh1106 import SH1106_I2C
    oled = SH1106_I2C(width=CANVAS_WIDTH, height=CANVAS_HEIGHT, i2c=i2c)
else:
    raise Exception('Unrecognized screen configured in main.py')



DEBUG  = True #Shows debug messages on the Serial Monitor

#TODO: Continue in-depth comments below
#TODO: Additional code clean up passes

oled.init_display()
oled.rotate(True)

logo = Animate(x=0, y=0, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, filename='assets/beeAndPuppycat', animation_type='loop')

logo.splash(oled, sleep_time=0)

#Set hunger and bathroom timers and callbacks
def goPotty(var):
    baby.set = False
    go_potty.loop(no = 1)
    go_potty.set = True
    clear()

def getHungry(var):
    global health, happiness, energy
    health-=1
    happiness-=1
    energy-=1

oneHour = 60*60*1000
potty_timer = Timer(mode=Timer.PERIODIC, period=oneHour, callback=goPotty)
hunger_timer = Timer(mode=Timer.PERIODIC, period=oneHour, callback=getHungry)

#Create Icons
Icons = OrderedDict([
    ('pretty_patrick', Icon('assets/pretty_patrick.pbm', name = 'pretty_patrick')),
    ('race_track', Icon('assets/race_track.pbm', name = 'race_track')),
    ('food', Icon('assets/big_meat.pbm', name = 'food')),
    ('book', Icon('assets/book.pbm', name='book')),
    ('heart_plus', Icon('assets/heart.pbm', name = 'heart_plus')),
    ('lightbulb', Icon('assets/lightbulb.pbm', name = 'lightbulb')),
    ('game', Icon('assets/star.pbm', name = 'game')),
    ('firstaid', Icon('assets/firstaid.pbm', name = 'firstaid')),
    ('toilet', Icon('assets/toilet.pbm', name = 'toilet')),
    ('heart', Icon('assets/heart.pbm', name = 'heart')),
    ('toast_icon', Icon('assets/toast.pbm', name = 'toast_icon')),
    ('bee_icon', Icon('assets/bee.pbm', name = 'bee_icon')),
    ('crab', Icon('assets/crab.pbm', name ='crab'))
])

icon_count = len(Icons)
star = Icon('assets/star.pbm', name = 'star')

def clear():
    """ Clear the screen """
    oled.fill_rect(0,0,CANVAS_WIDTH,CANVAS_HEIGHT,0)

def build_toolbar():
    toolbar = Toolbar()
    toolbar.spacer = SPACER
    for item in Icons:
        #if item != 'star': #Star added for use in dark heart game, not a selectable icon
        toolbar.additem(Icons[item])
    return toolbar        
        
tb = build_toolbar()
krabs =           Animate(x=0, y=0, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, filename='assets/puppyCatEat', animation_type='loop')
bee =             Animate(x=0, y=0, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, filename='assets/beeFull', animation_type='loop')
puppycat =        Animate(x=0, y=0, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, filename='assets/puppycatFull', animation_type='loop')
toast =           Animate(x=0, y=0, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, filename='assets/toastFull', animation_type='loop')
starBunny =       Animate(x=0, y=0, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, filename='assets/beeFull', animation_type='loop') #TODO: change beeFull to bunnyStar image
narb =            Animate(x=0, y=0, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, filename='assets/narb', animation_type='loop')
puppyCatEat =     Animate(x=0, y=0, width=CANVAS_WIDTH, height=CANVAS_HEIGHT, filename='assets/puppyCatEat', animation_type='loop') #TODO: forgetting to add loop in init will cause animations to run without end, throw error
eat =             Animate(x=48, y=SPRITE_SIZE, width=48, height=48, filename = 'assets/eat')
baby =            Animate(x=48, y=SPRITE_SIZE, width=48, height=48, filename = 'assets/puppy_bounce', animation_type='bounce')
babyzzz =         Animate(x=48, y=SPRITE_SIZE, width=48, height=48, filename = 'assets/puppy_cat_zzz', animation_type='loop')
go_potty =        Animate(x=64, y=SPRITE_SIZE, width=48, height=48, filename = 'assets/puppy_cat_potty', animation_type='bounce')
poopy =           Animate(x=96, y=48, width=SPRITE_SIZE, height=SPRITE_SIZE, filename='assets/poop')
death =           Animate(x=40, y=SPRITE_SIZE, width=SPRITE_SIZE, height=SPRITE_SIZE, filename='assets/skull', animation_type='bounce')
dark_heart =      Animate(x=40, y=0, width=48, height=64, filename='assets/dark_heart', animation_type='loop')

def showTextXY(oled, message='', x=110, y=0, width=CANVAS_WIDTH, height=8, center=None, color=1):
    fbuf = framebuf.FrameBuffer(bytearray(width*height), width, height, framebuf.MONO_HLSB)
    if color == 0:
        fbuf.fill(1)
    fbuf.text(message, 0, 0, color)
    if center:
        msgWidth = len(message) * LETTER_WIDTH
        if msgWidth > CANVAS_WIDTH:
            raise Exception('Message overflow')
        x = int((width - msgWidth) / 2)
    oled.blit(fbuf, x, y)

def protoInputDrawLoop(oled):
    """Use callbacks to abstract input draw loop"""
    while True:
        if button_a.is_pressed:
            pass
        if button_b.is_pressed:
            pass
        if button_x.is_pressed:
            pass
        if button_a.is_held and button_b.is_held and button_x.is_held:
            clear()
            return
        
        oled.show()
        sleep(0.05)
        clear()

def pretty_patrick(oled):
    water = Icon('assets/water.pbm', name = 'water', width=SPRITE_SIZE, height=SPRITE_SIZE)
    fire = Icon('assets/fire.pbm', name = 'fire', width=SPRITE_SIZE, height=SPRITE_SIZE)
    air = Icon('assets/air.pbm', name = 'air', width=SPRITE_SIZE, height=SPRITE_SIZE)
    pan_width = 55
    pan_height = 23
    pan = Icon('assets/pan.pbm', name ='pan', x=42, y=33, width=pan_width, height=pan_height)
    chicken = Icon('assets/chicken.pbm', name ='chicken', x=54, y=8, width=16, height=11)
    chicken2 = Icon('assets/chicken2.pbm', name ='chicken2', x=54, y=8, width=16, height=11)
    egg_bg = Icon('assets/egg_bg.pbm', name='egg_bg', width=8, height=11)
    egg_fg = Icon('assets/egg_fg.pbm', name='egg_fg', width=8, height=11)
    egg_max_height = 32
    egg_min_height = 28
    egg_1_dir = -1
    egg_1_y = egg_max_height
    egg_2_dir = 1
    egg_2_y = egg_min_height
    egg_3_dir = -1
    egg_3_y = egg_max_height-2
    water_in = False
    fire_on = False
    eggs_in = False
    
    fire_under_width = 45
    fire_under = Animate(x=38, y=47, width=fire_under_width, height=14, filename='assets/fire_under', animation_type='loop')
    fire_under.load()
    fire_under.loop(no=-1)
    fire_under.speed='slow'
    
    steam = Animate(x=0, y=0, width = CANVAS_WIDTH - SPRITE_SIZE, height=37, filename='assets/steam', animation_type='loop')
    steam.load()
    steam.loop(no=-1)
    steam.speed='slow'
    
    #TODO: implement vertical toolbar for water, fire, air icons, and cycle via inverting image
    while True:
        if button_a.is_pressed:
            water_in = not water_in
            pass
        if button_b.is_pressed:
            fire_on = not fire_on
            pass
        if button_x.is_pressed:
            eggs_in = not eggs_in
            pass
        if button_a.is_held and button_b.is_held and button_x.is_held:
            clear()
            return
        
        egg_1_y += egg_1_dir
        egg_2_y += egg_2_dir
        egg_3_y += egg_3_dir
        
        if egg_1_y >= egg_max_height or egg_1_y <= egg_min_height:
            egg_1_dir *= -1
        if egg_2_y >= egg_max_height or egg_2_y <= egg_min_height:
            egg_2_dir *= -1
        if egg_3_y >= egg_max_height or egg_3_y <= egg_min_height:
            egg_3_dir *= -1
        
            
        #gap of 4 between each on right side
        water.show(oled, CANVAS_WIDTH - SPRITE_SIZE, 4)
        fire.show(oled, CANVAS_WIDTH - SPRITE_SIZE, 24)
        air.show(oled, CANVAS_WIDTH - SPRITE_SIZE, 44)
        pan.show(oled)
        if water_in and not fire_on:
            chicken.show(oled)
        if water_in and fire_on:
            steam.animate(oled)
            chicken2.show(oled)
        if eggs_in:
            egg_bg.show(oled, 45, egg_1_y, key=1) #key = 1 ignores black in the source image
            egg_fg.show(oled, 45, egg_1_y, key=0)
            egg_bg.show(oled, 55, egg_2_y, key=1) #key = 1 ignores black in the source image
            egg_fg.show(oled, 55, egg_2_y, key=0)
            egg_bg.show(oled, 65, egg_3_y, key=1) #key = 1 ignores black in the source image
            egg_fg.show(oled, 65, egg_3_y, key=0)
        if fire_on:
            fire_under.animate(oled)
        oled.show()
        sleep(0.05)
        clear()
    
    
def race_track(oled):
    global that_legal_tender, star, dark_heart_event
    clear()
#     speed = 15
#     xpos = CANVAS_WIDTH + SPRITE_SIZE # Traveling to the right, things move to the left
#     ypos = 0
#     width = SPRITE_SIZE
#     height = SPRITE_SIZE
#     fbuf = framebuf.FrameBuffer(bytearray(width*height), width, height, framebuf.MONO_HLSB)
#     fbuf.rect(0,0,8,8,1,True)
    star_field = Icon('assets/star_field.pbm', name = 'star_field', width = 128, height = 64)
    star_field_2 = Icon('assets/star_field.pbm', name = 'star_field_2', width = 128, height = 64, x=128)
    bg_wht = Icon('assets/race_track_bg_wht.pbm', name = 'bg_wht', width = 128, height = 64)
    bg_2_wht = Icon('assets/race_track_bg_wht.pbm', name = 'bg_2_wht', width = 128, height = 64)
    bg_blk = Icon('assets/race_track_bg_blk.pbm', name = 'bg_blk', width = 128, height = 64)
    bg_2_blk = Icon('assets/race_track_bg_blk.pbm', name = 'bg_2_blk', width = 128, height = 64)
    bee_width = 30
    bee_cycle_wht = Icon('assets/bee_cycle_wht.pbm', name = 'bee_cycle_wht', width = bee_width, height = 27)
    bee_cycle_blk = Icon('assets/bee_cycle_blk.pbm', name = 'bee_cycle_blk', width = bee_width, height = 27)
    poop = Icon('assets/poop01.pbm', name = 'poop', width = SPRITE_SIZE, height = SPRITE_SIZE)
    speed = -2
    pos = 0
    bg_speed = -8
    bg_pos = 0
    bg_pos2 = 128
    stripe_speed = 10
    stripe_pos = 0
    stripe_spacing = 6
    bee_x_pos = 49
    bee_lanes = [22, 36]
    star_lanes = [33, 47] # 11 off from bee lanes to account for different size in sprites
    lane_index = 0
    choice = int(random()*1.9)
    star_index = choice
    poop_index = int(not choice)
    score = 0
    star.x = CANVAS_WIDTH
    win_bonus = 400
    
    while True:
        if score >= 20:
            dark_heart_event.message = 'Winner!'
            dark_heart_event.popup(oled, sleep_time = 1)
            for x in range(3):
                dark_heart_event.message = '$ + '+str(win_bonus)+'!'
                dark_heart_event.popup(oled, sleep_time = 0.75)
                dark_heart_event.message = ''
                dark_heart_event.popup(oled, sleep_time = 0.25)
            that_legal_tender += win_bonus
            clear()
            return
        if button_a.is_pressed:
            bee_x_pos -= 10
            if bee_x_pos < 0:
                bee_x_pos = 0
        if button_b.is_pressed:
            lane_index = int(not lane_index)
        if button_x.is_pressed:
            bee_x_pos += 10
            if bee_x_pos + bee_width > CANVAS_WIDTH:
                bee_x_pos = CANVAS_WIDTH - bee
        if button_a.is_held and button_b.is_held and button_x.is_held:
            clear()
            #TODO: unload icons
            return
#         xpos -= speed
#         if xpos < -1 * width:
#             xpos = CANVAS_WIDTH + SPRITE_SIZE
#             ypos = int(random() * (CANVAS_HEIGHT - SPRITE_SIZE))
        pos += speed
        if pos < -128:
            pos = 0
        bg_pos += bg_speed
        if bg_pos <= -136:
            bg_pos = 128
        bg_pos2 += bg_speed
        if bg_pos2 <= -136:
            bg_pos2 = 128
        stripe_pos -= stripe_speed
        if stripe_pos <= -128:
            stripe_pos = 0
            
        #check for colissions between beeCycle and other actors
        #ideally more like
        #bee.checkCollisions([actors_list])
        if star.x < bee_x_pos + bee_width and star.x + SPRITE_SIZE > bee_x_pos and lane_index == star_index:
            buzz.success()
            score+=1
            choice = int(random()*1.9)
            star_index = choice
            star.x = CANVAS_WIDTH
            poop_index = int(not choice)
        # Spawn in opposing rows
        if star.x <= -SPRITE_SIZE:
            choice = int(random()*1.9)
            star_index = choice
            star.x = CANVAS_WIDTH
            poop_index = int(not choice)
        
        star.x -= stripe_speed


        
        star_field.show(oled, pos)
        star_field_2.show(oled, pos+128)
        bg_wht.show(oled, bg_pos, 0, key=0)
        bg_blk.show(oled, bg_pos, 0, key=1) #split images into blk and white portions to achieve a lazy transparency effect
        bg_2_wht.show(oled, bg_pos2, 0, key=0)
        bg_2_blk.show(oled, bg_pos2, 0, key=1)
        
        oled.fill_rect(0,42,CANVAS_WIDTH,22,0)
        for i in range(43):
            oled.hline(stripe_pos+stripe_spacing*i,56,4,1)
        star.show(oled, star.x, star_lanes[star_index])
        bee_cycle_blk.show(oled, bee_x_pos, bee_lanes[lane_index], key=1) # Bulk of shape is black, so start by putting down the silloutte
        bee_cycle_wht.show(oled, bee_x_pos, bee_lanes[lane_index], key=0)
        showTextXY(oled, str(score))
        oled.show()
        sleep(0.05)
        clear()

def menu(options):
    """Present, allow scroll and selection of items"""

    selected = 0
    while True:
        if button_a.is_pressed:
            buzz.a()
            selected+=1
            if selected > 7:
                selected = 0
        if button_x.is_pressed:
            buzz.x()
            clear()
            return
        if button_b.is_pressed:
            buzz.b()
            if len(options) != 0:
                options.remove(options[selected])
        clear()
        for i in range(min(8,len(options))):
            colr = 1
            if i == selected:
                colr = 0
            showTextXY(oled, str(options[i]), y=i*8, x=0, color = colr)
        oled.show()
        sleep(0.05)

def prompt(): #TODO: pass this an existing string to load into entry
    """Allow text and numeric entries"""
    cursor = True
    entry = [' '] * 16
    symbols = ' ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789!?'
    entry_i = 0
    symbols_i = 0
    while True:
        if button_b.is_held: # Holding b allows exit, disables indep a and x behavior
            buzz.b()
            if button_a.is_held and button_x.is_held:
                buzz.x()
                clear()
                return ''.join(entry)
            else:
                entry_i+=1
                if entry_i >= len(entry):
                    entry_i = 0   
        elif button_a.is_pressed:
            buzz.a()
            symbols_i-=1;
            if symbols_i < 0:
                symbols_i = len(symbols)-1
            entry[entry_i] = symbols[symbols_i]        
        elif button_x.is_pressed:
            buzz.x()
            symbols_i+=1;
            if symbols_i >= len(symbols):
                symbols_i = 0
            entry[entry_i] = symbols[symbols_i]
            
            
        clear()
        showTextXY(oled, 'Enter text below:', y = 24, x =0)
        showTextXY(oled, ''.join(entry).rstrip(), y=34, x=0)
        if cursor: #lazy toggle cursor
            oled.hline(LETTER_WIDTH*entry_i, 43, LETTER_WIDTH, 1)
            cursor = False
        else:
            cursor = True
        oled.show()
        sleep(0.05)
    
class ShopItem:
    def __init__(self, name, cost, icon):
        self.name = name
        self.cost = cost
        self.icon = icon

def shop():
    global that_legal_tender
    items=[]
    item_count = 3
    shop_inventory = [
        ShopItem('Cheese', 10, star),
        ShopItem('Red Chews', 25, Icons['toast_icon']),
        ShopItem('Mcwv. Egg Pouch', 50, star),
        ShopItem('Towel', 200, Icons['toast_icon']),
        ShopItem('Chips', 150, Icons['food'])]
    while len(items) < 3:
        index = int(random() * len(shop_inventory))
        if shop_inventory[index] not in items:
            items.append(shop_inventory[index])
    i = 0
    while True:       
        if button_a.is_pressed:
            buzz.a()
            i+=1
            if(i == item_count):
                i = 0
        if button_x.is_pressed:
            buzz.x()
            save_game()
            return
        if button_b.is_pressed:
            buzz.b()
            if that_legal_tender >= items[i].cost:
                that_legal_tender-=items[i].cost
                inventory.append(items[i].name)
        clear()
        showTextXY(oled, str(that_legal_tender), center = True)
        items[i].icon.show(oled, x=int((SPRITE_X_LIMIT)/2), y = 12)
        showTextXY(oled, str(items[i].name), y = 34, center = True)
        showTextXY(oled, str(items[i].cost), y = 48, center = True)
        oled.show()
        sleep(0.05)

def darkHeartGame():
    """Separate animation and input cycle"""
    global that_legal_tender, star
    score = 0
    clear()
    heart = Icons['heart']
    x_pos = int((SPRITE_X_LIMIT)/2)
    heart.y = CANVAS_HEIGHT-SPRITE_SIZE
    star_y = 0
    star_speed = 4
    speed = 18
    win_bonus = 400
    star_field = Icon('assets/star_field.pbm', name = 'star_field', width = 128, height = 64)
    star_field_2 = Icon('assets/star_field.pbm', name = 'star_field_2', width = 128, height = 64)
    star_field_speed = 1
    star_field_y_pos = 0
    while True:
        if score >= 20:
            dark_heart_event.message = 'Winner!'
            dark_heart_event.popup(oled, sleep_time = 1)
            for x in range(3):
                dark_heart_event.message = '$ + '+str(win_bonus)+'!'
                dark_heart_event.popup(oled, sleep_time = 0.75)
                dark_heart_event.message = ''
                dark_heart_event.popup(oled, sleep_time = 0.25)
            that_legal_tender += win_bonus
            clear()
            return
        if button_a.is_pressed:
            buzz.a()
            x_pos-=speed
            if x_pos < 0:
                x_pos = 0
        if button_x.is_pressed:
            buzz.x()
            x_pos+=speed
            if x_pos > SPRITE_X_LIMIT:
                x_pos = SPRITE_X_LIMIT
        if button_b.is_pressed:
            buzz.b()
            krabs.load()
            woeIsMeSong = music(songs.woeIsMe, looping = False, pin = buzzer_pin, tempo = 1, duty=volume)
            krabs.loop(no = 4)
            while woeIsMeSong.tick():
                if not krabs.done:
                    krabs.animate(oled)
                    oled.show()
                sleep(0.02)
            clear()
            that_legal_tender += min((score * score), 400)
            return
        heart.x = x_pos
        
        star.y+=round(star_speed)
        star_field_y_pos += star_field_speed
        if star_field_y_pos >=63:
           star_field_y_pos = 0 
        if(star.y > 32):
            if(abs(heart.x-star.x) < SPRITE_SIZE):
                buzz.success()
                score+=1
                star_speed+=0.125
                star.x = int(random() * SPRITE_X_LIMIT)
                star.y = -SPRITE_SIZE
        if(star.y > 64):
            star.y = -SPRITE_SIZE
            star.x+=SPRITE_SIZE
            if star.x > SPRITE_X_LIMIT:
                star.x = 0
        
        
        star_field.show(oled, 0, star_field_y_pos)
        star_field_2.show(oled, 0, star_field_y_pos-64)
        star.show(oled)
        heart.show(oled)
        showTextXY(oled, str(score))
        oled.show()
        sleep(0.05)
        clear()

index = 0
tb.select(index, oled)
cancel = False
feeding_time = False
sleeping = False
death.set = False

# Set up Events
energy_increase =   Event(name = 'Increase Energy', sprite = Icons['heart'])
firstaid =          Event(name = 'First Aid', sprite = Icons['firstaid'])
toilet =            Event(name = 'Toilet', sprite = Icons['toilet'])
game_event =        Event(name = 'Game', sprite = Icons['game'])
dark_heart_event =  Event(name = 'Dark Heart', sprite = star)
sleep_time =        Event(name = 'sleep time', sprite = Icons['lightbulb'])
heart_status =      Event(name = 'Status', sprite = Icons['heart'])

baby.bounce() #initialize the baby animation as a bounce type
poopy.bounce() #initialize the poopy animation as a bounce type
puppyCatEat.loop(no = 4)
puppyCatEat.speed = 'slow'
krabs.loop(no = 4)
krabs.speed = 'slow'
death.loop(no = -1) #initialize the death animation as an endless loop type
death.speed = 'slow'
babyzzz.speed = 'very slow'
go_potty.loop(no = 1) #init the go_potty animation as a loop with one pass
dark_heart.loop(no = 2)
dark_heart.speed='slow'

go_potty.set = True #set the flag to show the potty animation
poopy.set = False #set the poopy as not visible
go_potty.load() #load the resources for go_potty

beeThemeSong = music(songs.beeTheme, looping = False, pin = buzzer_pin, tempo = 2, duty=volume) #default tempo=3=slow; tempo=2 is usually right
woeIsMeSong = music(songs.woeIsMe, looping = False, pin = buzzer_pin, tempo = 1, duty=volume)

buzz = buzzer(pin=buzzer_pin, duty=volume)


#Display the intro logo and play the startup song
logo.splash(oled, sleep_time=0)
while beeThemeSong.tick(): #Play song until finished
    sleep(0.04)
clear()


#main loop after everything else has been defined and established
while True:
    if not cancel:
        tb.unselect(index, oled)
    if button_a.is_pressed:
        buzz.a()
        index+=1
        if index == len(Icons):
            index = 0
        cancel = False
    if button_x.is_pressed:
        buzz.x()
        cancel = True
        index = -1
    if not cancel:
        tb.select(index, oled)
    if button_b.is_pressed:
        buzz.b()
        if index == -1: #TODO: find a better fix for this than checking index set after cancel
            time = localtime()
            hour = time[3]
            ampm='AM'
            if hour > 12:
                hour = time[3] - 12
                ampm = 'PM'
            dark_heart_event.message = '%s:%02d %s' %(hour, time[4], ampm)
            dark_heart_event.popup(oled, sleep_time = BANNER_SLEEP)
            clear()
        if tb.selected_item == 'food':
            feeding_time = True
            puppyCatEat.loop(no = 4)
            sleeping = False
            baby.unload()
        if tb.selected_item == 'book':
            menu(inventory)
        if tb.selected_item == 'heart_plus':
            result = prompt()
            wifi_pass = result
            connected = ntpTime.connect(wifi_pass)
            if connected:
                dark_heart_event.message = 'Connected'
                dark_heart_event.popup(oled)
            else:
                dark_heart_event.message = 'Ask me later'
                dark_heart_event.popup(oled)
            clear()
        if tb.selected_item == 'game':
            dark_heart_event.message = 'Fill my dark'
            dark_heart_event.popup(oled, sleep_time = BANNER_SLEEP)
            dark_heart_event.message = 'heart with'
            dark_heart_event.popup(oled, sleep_time = BANNER_SLEEP)
            dark_heart_event.message = 'stars'
            dark_heart_event.popup(oled, sleep_time = BANNER_SLEEP)
            dark_heart.load()
            dark_heart.loop(no = 2)
            clear()
            while not dark_heart.done:
                dark_heart.animate(oled)
                oled.show()
                sleep(0.04)
            dark_heart.unload()
            darkHeartGame()
        if tb.selected_item == 'toilet':
            toilet.message = 'Cleaning...'
            toilet.popup(oled)
            poopy.set = False
            baby.set = True
            happiness+=1
            clear()
            poopy.unload()
        if tb.selected_item == 'lightbulb':
            if not sleeping:
                sleeping = True
                babyzzz.load()
                sleep_time.message = 'Night Night'
                sleep_time.popup(oled)
                clear()
            else:
                sleeping = False
                babyzzz.unload()
        if tb.selected_item == 'firstaid':
            firstaid.message = 'Vitamins'
            firstaid.popup(oled)
            health+=1
            clear()
        if tb.selected_item == 'heart':
            narb.splash(oled, sleep_time = BANNER_SLEEP)
            game_event.message = 'yea yea yea'
            game_event.popup(oled, sleep_time = BANNER_SLEEP)
            game_event.message = 'you like the'
            game_event.popup(oled, sleep_time = BANNER_SLEEP)
            game_event.message = 'word yea huh'
            game_event.popup(oled, sleep_time = BANNER_SLEEP)
            shop()
            clear()
        if (tb.selected_item == 'toast_icon'):
            toast.splash(oled, sleep_time = 1)
            clear()
        if (tb.selected_item == 'bee_icon'):
            bee.splash(oled, sleep_time = 1)
            clear()
        if (tb.selected_item == 'crab'): 
            puppycat.splash(oled, sleep_time = 1)
            clear()
        if (tb.selected_item == 'race_track' and index >= 0): #TODO: find a better fix for this than checking index set after cancel
            race_track(oled)
            clear()
        if (tb.selected_item == 'pretty_patrick' and index >= 0): #TODO: find a better fix for this than checking index set after cancel
            pretty_patrick(oled)
            clear()
    if poopy.set:
        poopy.load()
        poopy.animate(oled)        
    if feeding_time:
        puppyCatEat.load()
        if not puppyCatEat.done:
            puppyCatEat.animate(oled)
        if feeding_time and puppyCatEat.done:
            feeding_time = False
            energy_increase.message = 'ENERGY + 1'
            energy_increase.popup(oled)
            energy+=1
            clear()
            puppyCatEat.unload()
            baby.load()
    else:
        if sleeping:
            babyzzz.animate(oled)
        else:
            if baby.set:
                baby.load()
                baby.animate(oled)
            if go_potty.set:
                go_potty.animate(oled)
            if go_potty.done:
                go_potty.set = False
                poopy.set = True
                baby.load()
                baby.bounce(no = -1)
                baby.set = True
    if (energy <= 1) and (happiness <= 1) and (health <= 1):
        death.set = True
    else:
        death.set = False
    if death.set:
        death.animate(oled)
    
    offset = 0
    if index > 6:
        offset = (6 - index) * (SPRITE_SIZE + SPACER)
    tb.show(oled, offset)
    oled.show()
    sleep(0.05)

