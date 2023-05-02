import math as m
import pygame as pg


class Rectangle:
    def __init__(self, x=0, y=0, w=0, h=0, color=''):
        self.x = x  # Position X
        self.y = y  # Position Y
        self.w = w  # Width
        self.h = h  # Height
        self.color = color

    def draw(self, screen):
        pg.draw.rect(screen, self.color,
                     (self.x, self.y, self.w, self.h), 2)


class Button(Rectangle):
    def __init__(self, x=0, y=0, w=0, h=0, color=''):
        Rectangle.__init__(self, x, y, w, h, color)

    def isMouseOn(self):
        if self.x <= pg.mouse.get_pos()[0] <= (self.x + self.w) and self.y <= pg.mouse.get_pos()[1] <= (self.y + self.h):
            return True
        else:
            False

    def takeaction(self, output, value):
        if self.isMouseOn():
            if pg.mouse.get_pressed()[0]:
                pg.draw.rect(screen, ACTIVE, (self.x,
                                              self.y, self.w, self.h), 5)
                for i in range(len(output)):
                    output[i] = value[i]
            else:
                pg.draw.rect(screen, ACTIVE, (self.x,
                                              self.y, self.w, self.h), 2)
        else:
            pg.draw.rect(screen, black, (self.x,
                                         self.y, self.w, self.h), 2)
        return output

    def takeaction_toggle(self, output, mouse_trig, press, mouse_output, Auto_Manual_text_toggle):
        if self.isMouseOn():
            mouse_trig, press, mouse_output = mouse_logic(
                mouse_trig, press, mouse_output)
            if mouse_output:
                pg.draw.rect(screen, ACTIVE, (self.x,
                                              self.y, self.w, self.h), 5)
                Auto_Manual_text_toggle = True
                output = True
            else:
                pg.draw.rect(screen, ACTIVE, (self.x,
                                              self.y, self.w, self.h), 2)
                Auto_Manual_text_toggle = False
                output = False
        else:
            pg.draw.rect(screen, black, (self.x,
                                         self.y, self.w, self.h), 2)
        return output, mouse_trig, press, mouse_output, Auto_Manual_text_toggle


class TextBox:
    def __init__(self, col, text=''):
        # self.rect = pg.Rect(x, y, w, h)
        self.color = col
        self.text = text
        self.txt_surface = FONT.render(text, True, self.color)

    def draw(self, Screen):
        # Blit the text.
        Screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y))


class InputBox:

    def __init__(self, x, y, w, h, text='', type='', l=100, location=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = black
        self.text = text
        self.return_text = ''
        self.type = type
        self.len = l
        self.location = location
        self.txt_surface = FONT.render(text, True, self.color)
        self.active = False
        self.enter_switch = 0

    def return_location(self, location, location_cooldown):
        if self.active == True:
            location = self.location
            location_cooldown = 0
        elif self.active == False:
            location = location
            location_cooldown = 1
        return location, location_cooldown

    def handle_event(self, event):

        if event.type == pg.MOUSEBUTTONDOWN:  # ทำการเช็คว่ามีการคลิก Mouse หรือไม่
            # ทำการเช็คว่าตำแหน่งของ Mouse อยู่บน InputBox นี้หรือไม่
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.return_text = self.text
                self.active = False
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    self.return_text = self.text
                    self.active = False
                elif event.key == pg.K_KP_ENTER:
                    self.return_text = self.text
                    self.active = False
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    if self.type == 'str':
                        self.text += event.unicode
                    elif self.type == 'int':
                        if event.unicode.isnumeric():
                            if len(self.text) < self.len and self.text != '0':
                                self.text += event.unicode
                        else:
                            self.text = self.text
                # Re-render the text.
                self.txt_surface = FONT.render(self.text, True, black)
        self.color = ACTIVE if self.active else black  # เปลี่ยนสีของ InputBox

    def update(self):
        # Resize the box if the text is too long.
        width = max(self.rect.w, self.txt_surface.get_width()+10)
        self.rect.w = width

    def draw(self, Screen):
        # Blit the text.
        Screen.blit(self.txt_surface, (self.rect.x+5, self.rect.y))
        # Blit the rect.
        pg.draw.rect(Screen, self.color, self.rect, 2)

    def inputbox_return(self, output, multiplier=1):
        if self.return_text != '':
            output = int(self.text)/multiplier
            self.return_text = ''
            self.enter_switch = 0
        if self.return_text == '':
            if self.active:
                self.enter_switch = 1
            else:
                self.enter_switch = 0
        return output

    def notify_user(self, text, px, py):
        if self.enter_switch == 1:
            screen.blit(TextBox(red, text).txt_surface, (px, py))


# Squash Object------------------------------------------------------------------------------
class Ball:
    def __init__(self, pos_x, pos_y, u, size, color, curr_x_distance, curr_y_distance):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.u = u
        self.size = size
        self.color = color
        self.curr_x_distance = curr_x_distance
        self.curr_y_distance = curr_y_distance
        self.lx = []
        self.ly = []

    def update_position(self, t):
        self.pos_x = ini_sx+(ux*(t/1000*speed_multiplier))*scale_multiplier
        self.pos_y = (ini_sy-h*scale_multiplier)-(uy*(t/1000*speed_multiplier) +
                                                  (-a*(t/1000*speed_multiplier)**2)/2)*scale_multiplier
        self.curr_x_distance = str(ux*t/1000)[:5]
        self.curr_y_distance = str(h+(uy*(t/1000)-0.5*(a*((t/1000)**2))))[:5]

    def dots_track(self, t, speed_multiplier):
        # Re-fill the background with coordinates from list
        for i, j in zip(range(len(self.lx)), range(len(self.ly))):
            pg.draw.circle(screen, black, (self.lx[i], self.ly[i]), 2)
        # Frequency of dots in the path tracer
        if (t*speed_multiplier % 80 == 0):
            self.lx.append(int(squash.pos_x))
            self.ly.append(int(squash.pos_y))

    def reset(self, pos_x, pos_y,  curr_x_distance, curr_y_distance):
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.curr_x_distance = curr_x_distance
        self.curr_y_distance = curr_y_distance
        self.lx = []
        self.ly = []

    def draw(self, screen, scale_multiplier):
        pg.draw.circle(screen, self.color, (self.pos_x,
                                            self.pos_y), self.size*scale_multiplier)

# Simulation Object-------------------------------------------------------------------------------------


class Simulation():

    def __init__(self, t, last_t, pos_y_max):
        self.t = t
        self.last_t = last_t
        self.pos_y_max = pos_y_max

    def initiate_sim(self, wall_logic_gate, toggle_start):
        if self.pos_y_max > squash.pos_y:
            self.pos_y_max = squash.pos_y
        # toggleable simulation
        if toggle_start == 1:
            # dotted tracing#---------------------------------------------------------------------------------------------------#
            squash.dots_track(self.t, speed_multiplier)
            # position vector#---------------------------------------------------------------------------------------------------#
            squash.draw(screen, scale_multiplier)
            if (squash.pos_y <= ini_sy-0.35*scale_multiplier):  # run simulation
                if ((ini_sx+(1+s2)*scale_multiplier <= squash.pos_x <= (ini_sx+(1+s2)*scale_multiplier)+0.03*scale_multiplier) and (ini_sy+5-wall*scale_multiplier <= squash.pos_y <= (ini_sy+5-wall*scale_multiplier)+wall*scale_multiplier)):
                    wall_logic_gate = 1
                if wall_logic_gate == 1:
                    self.last_t = self.t
                    self.t = 0
                else:
                    squash.update_position(self.t)
                    self.t += 1
            else:  # reset simulation
                self.last_t = self.t
                self.t = 0
            pg.draw.rect(screen, red, (0, sim.pos_y_max, win_x-400, 2))
        elif toggle_start == 0:
            self.pos_y_max = 900
            squash.reset(ini_sx-5+(0.015*scale_multiplier), ini_sy -
                         (h*scale_multiplier), squash.curr_x_distance, squash.curr_y_distance)
            squash.draw(screen, scale_multiplier)

    def reset_sim(self, wall_logic_gate, toggle_reset, toggle_start):
        if toggle_reset == 1:
            squash.reset(ini_sx, ini_sy-h*scale_multiplier, 0, h)
            self.t = 0
            toggle_reset = 0
            toggle_start = 0
            wall_logic_gate = 0
        return wall_logic_gate, toggle_reset, toggle_start

# Calculate functions----------------------------------------------------------------------------------


def calculate(s1, s2, h, deg, M, k):
    u = m.sqrt((4.9*(s1+s2+2)**2)/((h-0.35+m.tan(m.radians(deg))
                                    * (s1+s2+2))*m.cos(m.radians(deg))**2))
    # print("u =", str(u)[:5])
    x = (19.6*M*m.sin(m.radians(deg)) +
         m.sqrt((19.6*M*m.sin(m.radians(deg))**2+4*k*1000*M*(u**2))))/(2*k*1000)
    # print("x =", str(x)[:5])
    H = m.tan(m.radians(deg))*(s1+1)-4.9 * \
        ((s1+1)/(u*m.cos(m.radians(deg))))**2+h
    # print("H =", str(H)[:5])
    ux = u*m.cos(m.radians(deg))
    uy = u*m.sin(m.radians(deg))
    return u, x, H, ux, uy


def ping_location(x, y, ct_G, ct_B):
    pg.draw.circle(screen, (255, 51+ct_G, 51+ct_B),
                   (x, y), ct_G/500*scale_multiplier)
    if ct_G+51 < 255:
        ct_G += 1
    else:
        ct_G = ct_G
    if ct_B+51 < 204:
        ct_B += (204/255)
    else:
        ct_B = ct_B
    return ct_G, ct_B


def activate_ping(location, ct_G, ct_B):
    if location == '':
        ct_G, ct_B = 0, 0
    if location == 'degree':
        ct_G, ct_B = ping_location(
            ini_sx, ini_sy-h*scale_multiplier, ct_G, ct_B)
    if location == 's2':
        ct_G, ct_B = ping_location(
            ini_sx, ini_sy-h*scale_multiplier, ct_G, ct_B)
    if location == 's1':
        ct_G, ct_B = ping_location(
            ini_sx+(2+s2)*scale_multiplier,
            ini_sy-0.5*h*scale_multiplier, ct_G, ct_B)
    if location == 'wall':
        ct_G, ct_B = ping_location(
            ini_sx+(1+s2)*scale_multiplier, ini_sy+5-0.5*wall*scale_multiplier, ct_G, ct_B)
    return location, ct_G, ct_B

# set field function--------------------------------------------------------------------------


def draw_field(location, location_time, location_cooldown):
    pg.draw.rect(screen, black, (0, ini_sy+5, win_x-400, 2))  # floor
    pg.draw.rect(screen, black, (ini_sx-5, ini_sy+5-h*scale_multiplier,
                 0.03*scale_multiplier, h*scale_multiplier))  # shooter
    pg.draw.rect(screen, black, (ini_sx+(1+s2)*scale_multiplier,
                 ini_sy+5-wall*scale_multiplier, 0.03*scale_multiplier, wall*scale_multiplier))  # wall
    pg.draw.rect(screen, light_blue, ((ini_sx+(2+s2)*scale_multiplier),
                 ini_sy+3, 0.433*scale_multiplier, 4))
    pg.draw.rect(screen, dark_blue, ((ini_sx+(2+s1+s2)*scale_multiplier)-(0.065*scale_multiplier),
                 ini_sy+5-0.35*scale_multiplier, 0.13*scale_multiplier, 0.35*scale_multiplier))
    pg.draw.rect(screen, light_blue, ((ini_sx+(-0.8+s2)*scale_multiplier),
                 ini_sy+3, 0.8*scale_multiplier, 4))
    pg.draw.rect(screen, bg_color, (win_x-400, 0, 400, win_y))
    pg.draw.rect(screen, black, (win_x-400, 0, 2, win_y))  # divider
    # alternative mode
    if location == 'degree':
        pg.draw.line(screen, red, (ini_sx-1, ini_sy-h*scale_multiplier),
                     (ini_sx+int((0.5*scale_multiplier) * m.cos(m.radians(deg))), ini_sy-h*scale_multiplier-int((0.5*scale_multiplier)*m.sin(m.radians(deg)))), 2)
        pg.draw.line(screen, red, (ini_sx-1, ini_sy-h*scale_multiplier),
                     (ini_sx+0.5*scale_multiplier, ini_sy-h*scale_multiplier), 2)
        pg.draw.arc(screen, red, (ini_sx-0.15*scale_multiplier, ini_sy-(h+0.15)*scale_multiplier,
                    0.3*scale_multiplier, 0.3*scale_multiplier), 0, m.radians(deg), 2)
    if location == 's1':
        pg.draw.line(screen, red, (ini_sx+(2+s2)*scale_multiplier,
                                   ini_sy), (ini_sx+(2+s2)*scale_multiplier, ini_sy-(0.34+0.05)*scale_multiplier), 2)
        pg.draw.line(screen, red, (ini_sx+(2+s1+s2)*scale_multiplier,
                                   ini_sy-0.34*scale_multiplier), (ini_sx+(2+s1+s2)*scale_multiplier, ini_sy-(0.34+0.05)*scale_multiplier), 2)
        pg.draw.line(screen, red, (ini_sx+(2+s2)*scale_multiplier, ini_sy-(0.34+0.025)*scale_multiplier),
                     (ini_sx+(2+s1+s2)*scale_multiplier, ini_sy-(0.34+0.025)*scale_multiplier), 2)
    if location == 's2':
        pg.draw.line(screen, red, (ini_sx-1, ini_sy-(h+0.05) *
                                   scale_multiplier), (ini_sx-1, ini_sy-(h+0.1)*scale_multiplier), 2)
        pg.draw.line(screen, red, (ini_sx-1+s2*scale_multiplier, ini_sy),
                     (ini_sx-1+s2*scale_multiplier, ini_sy-(h+0.1)*scale_multiplier), 2)
        pg.draw.line(screen, red, (ini_sx-1, ini_sy-(h+0.1-0.025)*scale_multiplier),
                     (ini_sx+s2*scale_multiplier, ini_sy-(h+0.1-0.025)*scale_multiplier), 2)
    if location == 'wall':
        pg.draw.line(screen, red, (ini_sx+(1+s2+0.1)*scale_multiplier,
                                   ini_sy+5-wall*scale_multiplier), (ini_sx+(1+s2+0.1)*scale_multiplier,
                                                                     ini_sy+5), 2)
        pg.draw.line(screen, red, (ini_sx+(1+s2+0.05)*scale_multiplier,
                                   ini_sy+5-wall*scale_multiplier), (ini_sx+(1+s2+0.125)*scale_multiplier,
                                                                     ini_sy+5-wall*scale_multiplier), 2)
        pg.draw.line(screen, red, (ini_sx+(1+s2+0.05)*scale_multiplier,
                                   ini_sy+5), (ini_sx+(1+s2+0.125)*scale_multiplier,
                                               ini_sy+5), 2)
    # visual guidelines delay
    if location_cooldown == 1:
        location_time += 1
    else:
        location_time = 0

    if location_time >= 1000:
        location = ''

    return location, location_time, location_cooldown


# get speed_multiplier functions------------------------------------------------------------------------
def find_speed_multiplier(x_speed_switches):
    x_speed_switches = x_01.takeaction(
        x_speed_switches, [1, 0, 0, 0, 0])
    x_speed_switches = x_02.takeaction(
        x_speed_switches, [0, 1, 0, 0, 0])
    x_speed_switches = x_05.takeaction(
        x_speed_switches, [0, 0, 1, 0, 0])
    x_speed_switches = x_08.takeaction(
        x_speed_switches, [0, 0, 0, 1, 0])
    x_speed_switches = x_1.takeaction(
        x_speed_switches, [0, 0, 0, 0, 1])

    # speed button adjustment
    if x_speed_switches[0] == 1:  # x_01_switch
        pg.draw.rect(screen, ACTIVE, (x_01.x,
                                      x_01.y, x_01.w, x_01.h), 5)
        speed_multiplier = 0.1
    elif x_speed_switches[1] == 1:  # x_02_switch
        pg.draw.rect(screen, ACTIVE, (x_02.x,
                                      x_02.y, x_02.w, x_02.h), 5)
        speed_multiplier = 0.2
    elif x_speed_switches[2] == 1:  # x_05_switch
        pg.draw.rect(screen, ACTIVE, (x_05.x,
                                      x_05.y, x_05.w, x_05.h), 5)
        speed_multiplier = 0.5
    elif x_speed_switches[3] == 1:  # x_08_switch
        pg.draw.rect(screen, ACTIVE, (x_08.x,
                                      x_08.y, x_08.w, x_08.h), 5)
        speed_multiplier = 0.8
    elif x_speed_switches[4] == 1:  # x_1_switch
        pg.draw.rect(screen, ACTIVE, (x_1.x,
                                      x_1.y, x_1.w, x_1.h), 5)
        speed_multiplier = 1
    return speed_multiplier, x_speed_switches

# update text function---------------------------------------------------------------------------------


def update_textboxs():
    screen.blit(TextBox(black,
                'Launch degree =          °').txt_surface, (20, 555))
    screen.blit(TextBox(black,
                'S1 =              (mm)').txt_surface, (230, 555))
    screen.blit(TextBox(black,
                'S2 =              (mm)').txt_surface, (400, 555))
    screen.blit(TextBox(black,
                'Wall Height =              (cm)').txt_surface, (570, 555))
    screen.blit(TextBox(black,
                '0.1').txt_surface, (909, 423))
    screen.blit(TextBox(black,
                '0.2').txt_surface, (948, 423))
    screen.blit(TextBox(black,
                '0.5').txt_surface, (987, 423))
    screen.blit(TextBox(black,
                '0.8').txt_surface, (1027, 423))
    screen.blit(TextBox(black,
                '1').txt_surface, (1075, 423))
    screen.blit(TextBox(dark_blue,
                'INITIATE').txt_surface, (969, 474))
    screen.blit(TextBox(red,
                'RESET').txt_surface, (978, 524))
    screen.blit(TextBox(black,
                'Speed Multiplier').txt_surface, (935, 395))
    screen.blit(TextBox(black,
                'Scale : {sp}'.format(sp=scale_multiplier)).txt_surface, (820, 300))
    screen.blit(TextBox(mystic_green,
                "Initial Velocity = {u} m/s".format(u=str(u)[:5])).txt_surface, (820, 25))
    screen.blit(TextBox(mystic_green,
                "Spring deformation = {x} m".format(x=str(x)[:5])).txt_surface, (820, 75))
    screen.blit(TextBox(mystic_green,
                "Height over wall while passing  = {H} m".format(H=str(H-wall)[:5])).txt_surface, (820, 125))
    screen.blit(TextBox(black,
                "X displacement from start : {x_pos} m".format(x_pos=squash.curr_x_distance)).txt_surface, (5, 5))
    screen.blit(TextBox(black,
                "Y displacement from ground : {y_pos} m".format(y_pos=squash.curr_y_distance)).txt_surface, (5, 30))
    if Auto_Manual_text_toggle:
        screen.blit(TextBox(mystic_green, 'Auto').txt_surface, (1093, 300))
    if not Auto_Manual_text_toggle:
        screen.blit(TextBox(black, 'Manual').txt_surface, (1080, 300))


def mouse_logic(mouse_trig, press, mouse_output):
    mouse_release = True if pg.mouse.get_pressed()[0] == False else False
    if mouse_release:  # if mouse button is released
        mouse_trig[0] = True
    if not mouse_release:  # if mouse button is pressed
        mouse_trig[1] = True
    # trigger only if mouse button already pressed and releasde at least once
    if mouse_trig == [True, True]:
        press.append('pressed')
        # trigger only when mouse button pressed but not when release
        mouse_trig = [False, False]
    if len(press) == 2:
        # output = True
        mouse_output = not mouse_output
        press = []
    return mouse_trig, press, mouse_output


def recommend_adjustment(toggle_recc, scale_multiplier):
    if toggle_recc == True:
        while (2+s2+s1)*scale_multiplier < 690:
            scale_multiplier += 1
            if (2+s2+s1)*scale_multiplier >= 690:
                break
    if toggle_recc == True:
        while (2+s2+s1)*scale_multiplier > 700:
            scale_multiplier -= 1
            if (2+s2+s1)*scale_multiplier <= 700:
                break
    # toggle_recc = 0
    return toggle_recc, scale_multiplier


# logic#---------------------------------------------------------------------------------------------------#
scale_multiplier = 300  # to manually fit the screen
speed_multiplier = 1  # to manually control time as see fit
toggle_start = 0
toggle_reset = 0
toggle_recc = False
mouse_output = False
mouse_trig = [False, False]
Auto_Manual_text_toggle = False  # Manual
press = []
x_01_switch = 0
x_02_switch = 0
x_05_switch = 0
x_08_switch = 0
x_1_switch = 1
wall_logic_gate = 0
location_cooldown = 0
location = ''
x_speed_switches = [x_01_switch, x_02_switch,
                    x_05_switch, x_08_switch, x_1_switch]
# Scientific variables#---------------------------------------------------------------------------------------------------#
M = 0.23  # net weight of ball and platform
k = 0.88  # spring constant
deg = 60  # degree
s1 = 0.303  # at target
s2 = 0  # at shooter
wall = 1  # wall's height
h = 0.433  # shooter's height
a = 9.81  # earth's gravitational acceleration

u, x, H, ux, uy = calculate(s1, s2, h, deg, M, k)


ini_sx = 50  # initial floor position on X-axis
ini_sy = 530  # initial floor position on Y-axis
pos_x = ini_sx
pos_y = ini_sy-h*scale_multiplier  # initial ball position
pos_y_max = pos_y
curr_x_distance = 0
curr_y_distance = h
last_t = 0
location_time = 0
ct_G = 0
ct_B = 0
t = 0  # initial time
# Color code#---------------------------------------------------------------------------------------------------#
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 51, 51)
blue = (153, 153, 255)
light_blue = (153, 204, 255)
dark_blue = (0, 0, 153)
mystic_green = (29, 120, 116)
bg_color = (255, 255, 204)
ACTIVE = (192, 192, 192)

pg.init()
pg.display.set_caption("G03_Simulation")
FONT = pg.font.SysFont("impact", 20)
win_x = 1200
win_y = 600
screen = pg.display.set_mode((win_x, win_y))
running = True

# Buttons
Initiate = Button(900, 470, 200, 32, black)
Reset = Button(900, 520, 200, 32, black)
recommend = Button(1050, 298, 125, 32, black)
x_01 = Button(900, 420, 40, 32, black)
x_02 = Button(940, 420, 40, 32, black)
x_05 = Button(980, 420, 40, 32, black)
x_08 = Button(1020, 420, 40, 32, black)
x_1 = Button(1060, 420, 40, 32, black)
x_buttons = [x_01, x_02, x_05, x_08, x_1]

# Input boxes
input_box1 = InputBox(160, 555, 32, 32, '60', 'int', 2, 'degree')
input_box2 = InputBox(270, 555, 42, 32, '303', 'int', 3, 's1')
input_box3 = InputBox(440, 555, 42, 32, '0', 'int', 3, 's2')
input_box4 = InputBox(680, 555, 42, 32, '100', 'int', 3, 'wall')
input_boxes = [input_box1, input_box2, input_box3, input_box4]

# Squash
squash = Ball(pos_x, pos_y, u, 0.03, black, curr_x_distance, curr_y_distance)

# Simulation
sim = Simulation(t, last_t, pos_y_max)
while (running):
    screen.fill((255, 255, 204))
    # alternative visual display
    location, ct_G, ct_B = activate_ping(location, ct_G, ct_B)
    location, location_time, location_cooldown = draw_field(
        location, location_time, location_cooldown)

    # inputtable variables
    deg = input_box1.inputbox_return(deg)
    s1 = input_box2.inputbox_return(s1, 1000)
    s2 = input_box3.inputbox_return(s2, 1000)
    wall = input_box4.inputbox_return(wall, 100)

    # Calculations
    u, x, H, ux, uy = calculate(s1, s2, h, deg, M, k)
    # simulation init#
    sim.initiate_sim(wall_logic_gate, toggle_start)
    # simulation reset#
    wall_logic_gate, toggle_reset, toggle_start = sim.reset_sim(
        wall_logic_gate, toggle_reset, toggle_start)

    # initiate button interaction
    Initiate.draw(screen)
    Reset.draw(screen)
    recommend.draw(screen)
    for button in x_buttons:
        button.draw(screen)

    # Buttons#
    [toggle_start] = Initiate.takeaction([toggle_start], [1])
    [toggle_reset] = Reset.takeaction([toggle_reset], [1])
    toggle_recc, mouse_trig, press, mouse_output, Auto_Manual_text_toggle = recommend.takeaction_toggle(
        toggle_recc, mouse_trig, press, mouse_output, Auto_Manual_text_toggle)

    # recommend button
    toggle_recc, scale_multiplier = recommend_adjustment(
        toggle_recc, scale_multiplier)

    # get speed_multiplier
    speed_multiplier, x_speed_switches = find_speed_multiplier(
        x_speed_switches)
    # Textboxes
    update_textboxs()

    # ทำการเรียก InputBox ทุกๆตัว โดยการ Loop เข้าไปยัง list ที่เราเก็บค่า InputBox ไว้
    location_cooldowns = []
    for box in input_boxes:
        location, location_cooldown = box.return_location(
            location, location_cooldown)
        location_cooldowns.append(location_cooldown)
        box.update()  # เรียกใช้ฟังก์ชัน update() ของ InputBox
        # เรียกใช้ฟังก์ชัน draw() ของ InputBox เพื่อทำการสร้างรูปบน Screen
        box.draw(screen)
    location_cooldown = min(location_cooldowns)

    pg.display.update()
    for event in pg.event.get():
        for box in input_boxes:
            box.handle_event(event)
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_KP_MINUS:
                if toggle_start == 0:
                    scale_multiplier -= 10
                toggle_reset = 1
            elif event.key == pg.K_KP_PLUS:
                if toggle_start == 0:
                    scale_multiplier += 10
                toggle_reset = 1
        if event.type == pg.QUIT:
            pg.quit()
            exit()
'''pg.draw.circle(screen, black, (ini_sx-5+(0.015*scale_multiplier),
                   ini_sy-(h*scale_multiplier)), 0.03*scale_multiplier)'''
