"""
This moduel does the drawing for all of the HSI features
draw_init() initializes pygame and opens the screen
rose_x(hdg) given a heading, returns the x-coordinate for the center of a graphic



"""

import sys
import pygame
import math
from datetime import datetime, time

global screen
size = display_width, display_height, = 480, 320

global DISPLAY_MID
global ROSE_TOP
global SMALL_FONT_SIZE
global SMALL_FONT_SPACING

global ROSE_MAX_ANGLE
global ROSE_WIDTH
global ROSE_HEIGHT
global ROSE_LEFT
global ROSE_DEG_WIDTH
global ROSE_COLOR
global DCT_COLOR
global DCT_WIDTH
global DCT_TOP
global DCT_MID
global DCT_BOT
global BUG_COLOR
global BUG_BOT
global BUG_TOP
global BUG_WIDTH
global GND_TRK_COLOR
global GND_TRK_TOP
global GND_TRK_BOT
global GND_TRK_WIDTH
global CRS_COLOR
global CRS_TOP
global CRS_WIDTH
global CRS_BOT
global CDI_COLOR
global CDI_NEEDLE_COLOR
global CDI_Y
global CDI_MAJ_RADIUS
global CDI_MIN_RADIUS
global CDI_SPACING


DISPLAY_MID = int(display_width/2)
ROSE_TOP = int(.5*display_height)       # DEFINES MOST DIMENSIONS
SMALL_FONT_SIZE = 30
SMALL_FONT_SPACING = 20

ROSE_MAX_ANGLE = 60
ROSE_WIDTH = int(.8*display_width)      # 80% of screen width
ROSE_HEIGHT = int(.3*display_height)    # 30% of screen height
ROSE_LEFT = int(.1*display_width)       # 10% right offset (center the 80%)
ROSE_DEG_WIDTH = ROSE_WIDTH/ROSE_MAX_ANGLE
ROSE_COLOR = (255,255,255)              # I think that's white
DCT_COLOR = (255,127,0)
DCT_WIDTH = 6                           # actually half width of diamond
DCT_TOP = ROSE_TOP - 4
DCT_MID = DCT_TOP + 6
DCT_BOT = DCT_TOP + 12
BUG_COLOR=(191,191,191)
BUG_BOT = ROSE_TOP
BUG_TOP = ROSE_TOP - 10
BUG_WIDTH = 18
GND_TRK_COLOR = (255,0,127)
GND_TRK_TOP = ROSE_TOP -10
GND_TRK_BOT = GND_TRK_TOP + 8
GND_TRK_WIDTH = 8
CRS_COLOR = DCT_COLOR                   # DCT and CDI color should match CRS color
CRS_TOP = ROSE_TOP + 5
CRS_WIDTH = 10
CRS_BOT = CRS_TOP + 25
CDI_COLOR = (255,255,255)
CDI_NEEDLE_COLOR = CRS_COLOR            # CDI color should match CRS color
CDI_Y = int(.8*display_height)          # 80% of the way down
CDI_MAJ_RADIUS = 10
CDI_MIN_RADIUS = 5
CDI_SPACING = int(.05*display_width)

pygame.init()
global screen
global MH_font
MH_font= pygame.font.Font('freesansbold.ttf',60) # need to make sure height is correct
global SmallFont
SmallFont= pygame.font.Font('freesansbold.ttf',SMALL_FONT_SIZE) # need to make sure height is correct
screen = pygame.display.set_mode(size,pygame.FULLSCREEN)


def rose_x(hdg, angle):
    delta = angle - hdg
    if delta > 180: delta -= 360
    if delta < -180: delta += 360
    if delta > ROSE_MAX_ANGLE/2 + 5: delta = ROSE_MAX_ANGLE/2 + 2
    if - delta > ROSE_MAX_ANGLE/2 + 5: delta = - (ROSE_MAX_ANGLE/2 + 2)
    return(int(DISPLAY_MID + delta*ROSE_DEG_WIDTH))

def draw_init(): # this thing just to get screen defined here
    pygame.init()
    screen = pygame.display.set_mode(size,pygame.FULLSCREEN)
    return(screen)

def draw_blank_screen():
    screen.fill((0,0,0))

def draw_ETA(ETA,HSI_mode):  # using the time tuple
    if HSI_mode == "ground":
        ETA_string = datetime.utcnow().strftime("%H:%M")+"z"
    else:
        ETA_string = "ETA " +ETA.strftime("%H:%M")+"Z"
    ETA_surface = SmallFont.render(ETA_string, True, ROSE_COLOR)
    ETA_rect = ETA_surface.get_rect()
    ETA_rect.right = display_width-SMALL_FONT_SPACING
    ETA_rect.top = SMALL_FONT_SPACING
    screen.blit(ETA_surface,ETA_rect)


def draw_distance(dtg):
    if dtg < 100:
        dist_string = "{:.1f}".format(dtg)
    else:
        dist_string = "{:.0f}".format(dtg)
    dist_surface = SmallFont.render(dist_string + " NM", True, ROSE_COLOR)
    dist_rect = dist_surface.get_rect()
    dist_rect.left = SMALL_FONT_SPACING
    dist_rect.top = SMALL_FONT_SPACING
    screen.blit(dist_surface,dist_rect)

def draw_steering_mode(from_name, to_name, dct_course,HSI_mode):
    #print(from_name, to_name,dct_course, HSI_mode)
    if HSI_mode in ("dct" ,"dct bug"):
        mode_surface = SmallFont.render("{:03.0f}".format(dct_course)+" to "+to_name, True, ROSE_COLOR)
    elif HSI_mode == "ground":
        mode_surface = SmallFont.render("Ground", True, ROSE_COLOR)
    else:
        mode_surface = SmallFont.render("to " + to_name, True, ROSE_COLOR)
    mode_rect = mode_surface.get_rect()
    mode_rect.right = display_width-SMALL_FONT_SPACING
    mode_rect.top = SMALL_FONT_SIZE+SMALL_FONT_SPACING
    screen.blit(mode_surface,mode_rect)


def draw_compass_rose(hdg):

    pygame.draw.line(screen,ROSE_COLOR,(ROSE_LEFT,ROSE_TOP),(ROSE_LEFT+ROSE_WIDTH,ROSE_TOP))

    for tick in (-25,-20,-15,-10,-5,0,5,10,15,20,25,30):
        tick_dir = hdg - hdg%5 + tick
        tick_x = rose_x(hdg, tick_dir)
        if tick_dir%30 == 0:
            pygame.draw.line(screen,ROSE_COLOR,(tick_x,ROSE_TOP),(tick_x,ROSE_TOP+30))
            tick_txt = str(int(tick_dir/10))
            if tick_dir == 0 or tick_dir == 360: tick_txt="N"
            if tick_dir == 90: tick_txt="E"
            if tick_dir == 180: tick_txt="S"
            if tick_dir == 270: tick_txt="W"
            card_surface = SmallFont.render(tick_txt, True, ROSE_COLOR)
            card_rect = card_surface.get_rect()
            card_rect.centerx = tick_x
            card_rect.top = ROSE_TOP + 35
            screen.blit(card_surface,card_rect)
        else:
            pygame.draw.line(screen,ROSE_COLOR,(tick_x,ROSE_TOP),(tick_x,ROSE_TOP+20-tick_dir%10))

def draw_MH_num(hdg):
    MH_surface = MH_font.render("{:03.0f}".format(round(hdg,0)), True, ROSE_COLOR)
    MH_rect = MH_surface.get_rect()
    MH_rect.centerx = int(display_width/2)
    MH_rect.bottom = ROSE_TOP - 5
    screen.blit(MH_surface,MH_rect)

def draw_HDG_bug(hdg, bug):
    x = rose_x(hdg, bug)
    pygame.draw.polygon(screen,BUG_COLOR,
                      ((x-2,BUG_BOT),(x-BUG_WIDTH,BUG_BOT),(x-BUG_WIDTH,BUG_TOP),(x-BUG_WIDTH/2,BUG_TOP))
                      ,0)
    pygame.draw.polygon(screen,BUG_COLOR,
                      ((x+2,BUG_BOT),(x+BUG_WIDTH,BUG_BOT),(x+BUG_WIDTH,BUG_TOP),(x+BUG_WIDTH/2,BUG_TOP))
                      ,0)


def draw_lubber_line():
    pygame.draw.line(screen,ROSE_COLOR,(display_width/2,ROSE_TOP),(display_width/2,ROSE_TOP-8),3)

    pygame.draw.polygon(screen,ROSE_COLOR,
                      ((display_width/2,ROSE_TOP-2),(display_width/2+GND_TRK_WIDTH,GND_TRK_TOP-2),(display_width/2-GND_TRK_WIDTH,GND_TRK_TOP-2))
                      )


def draw_direct_diamond(hdg,hdg_to):
    x = rose_x(hdg, hdg_to)
    pygame.draw.lines(screen,DCT_COLOR,True,
                      ((x,DCT_BOT),(x+DCT_WIDTH,DCT_MID),(x,DCT_TOP),(x-DCT_WIDTH,DCT_MID))
                      ,3)

def draw_FP_course(hdg,FP_course):
    x = rose_x(hdg, FP_course)
    pygame.draw.lines(screen,CRS_COLOR,False,
                      ((x-CRS_WIDTH,CRS_TOP+CRS_WIDTH),(x,CRS_TOP),(x+CRS_WIDTH,CRS_TOP+CRS_WIDTH))
                      ,1)
    pygame.draw.line(screen,CRS_COLOR,(x,CRS_TOP),(x,CRS_BOT),3)

def draw_gnd_track(hdg,gnd_track):
    x = rose_x(hdg, gnd_track)
    pygame.draw.lines(screen,GND_TRK_COLOR,True,
                      ((x,GND_TRK_BOT),(x+GND_TRK_WIDTH,GND_TRK_TOP),(x-GND_TRK_WIDTH,GND_TRK_TOP))
                      ,3)

def draw_gnd_speed(gs):
    gs_string = "gs "+"{:.0f}".format(gs)
    gs_surface = SmallFont.render(gs_string+" kts", True, ROSE_COLOR)
    gs_rect = gs_surface.get_rect()
    gs_rect.left = SMALL_FONT_SPACING
    gs_rect.top = SMALL_FONT_SIZE+SMALL_FONT_SPACING
    screen.blit(gs_surface,gs_rect)

def draw_z_time():
    pass

def draw_CDI_scale(mode):
    # this should draw the units of the scale
    scale_text = "err"
    if mode == "enroute": scale_text = "2NM"
    if mode == "terminal": scale_text = "1NM"
    if mode == "approach": scale_text = ".3 NM"
    if mode == "direct": scale_text = "5 deg"

    scale_surface = SmallFont.render(scale_text, True, CDI_COLOR)
    scale_rect = scale_surface.get_rect()
    scale_rect.left = DISPLAY_MID + 5 * CDI_SPACING
    scale_rect.centery = CDI_Y
    screen.blit(scale_surface,scale_rect)

#   This part should be replaced with a bitmap or pre-drawn thing.     
    pygame.draw.circle(screen,CDI_COLOR,(DISPLAY_MID,CDI_Y),CDI_MAJ_RADIUS,1)
    for dot in (5,-4,-3,-2,-1,1,2,3,4,5):
        pygame.draw.circle(screen,CDI_COLOR,(DISPLAY_MID - CDI_SPACING*dot,CDI_Y),CDI_MIN_RADIUS,1)

def draw_CDI_needle(xte,mode):
    if mode == "direct":
        xte_angle = xte / 5
    elif mode == "enroute":
        xte_angle = xte/2
    elif mode == "terminal":
        xte_angle = xte
    elif mode == "approach" :
        xte_angle = xte*5
    else:
        xte_angle = xte
        print("CDI MODE ERROR")
    if xte_angle > 1.1:
        pygame.draw.lines(screen,CRS_COLOR,False,
                          ((DISPLAY_MID-6*CDI_SPACING, CDI_Y - 12),(DISPLAY_MID-6*CDI_SPACING-12, CDI_Y),(DISPLAY_MID-6*CDI_SPACING, CDI_Y + 12)),3)
    elif xte_angle < -1.1:
        pygame.draw.lines(screen,CRS_COLOR,False,
                          ((DISPLAY_MID+5*CDI_SPACING-12, CDI_Y - 12),(DISPLAY_MID+5*CDI_SPACING, CDI_Y),(DISPLAY_MID+5*CDI_SPACING-12, CDI_Y + 12)),3)
    else:    
        CDI_x = DISPLAY_MID - xte_angle*5*CDI_SPACING
        pygame.draw.line(screen,CRS_COLOR,(CDI_x, CDI_Y - 12),(CDI_x, CDI_Y + 12),3)



"""
This below is a tool to test the graphics
"""


def graphics_demo():
    clock = pygame.time.Clock()
    # some initial values
    runticks = 0 # used to generate drift angel
    hdg = 321.1
    FP_course = 320
    hdg_to = 330
    bug = 305
    dtg = 11
    fromwp = "OVR"
    towp = "DANEE"
    gs = 132
    crosstrack_error = -3

    while 1:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w: #  W and E to change heading
                    hdg -=1
                    if hdg < 0: hdg +=360
                if event.key == pygame.K_e:
                    hdg += 1
                    if hdg >= 360: hdg -= 360
                if event.key == pygame.K_u: # U and I to change hdg_to
                    hdg_to -=1
                    if hdg_to < 0: hdg_to +=360
                if event.key == pygame.K_i:
                    hdg_to += 1
                    if hdg_to >= 360: hdg_to -= 360
        runticks += 1
        gnd_track = hdg + 7*math.sin(runticks/100)
        ETA = datetime.now() #datetime time object
        dtg = dtg - .001
        
        screen.fill((0,0,0))
        draw_ETA(ETA)
        draw_distance(dtg)      # pass DTG in NM
        draw_steering_mode(fromwp,towp,0,False)    # pass text, third is direct to mode (true_false)
        draw_compass_rose(hdg)
        draw_MH_num(hdg)
        draw_HDG_bug(hdg,bug)
        draw_lubber_line()
        draw_direct_diamond(hdg,hdg_to)
        draw_FP_course(hdg, FP_course)
        draw_gnd_track(hdg,gnd_track) # also called the drift indicator 
        draw_gnd_speed(gs)
        draw_z_time()
        draw_CDI_scale("enroute")
        draw_CDI_needle(0.4,"approach")
        
        pygame.display.flip()
        msElapsed = clock.tick(20)    


# Only run the graphics demo if this file is run by itself
if __name__ == "__main__":
    #screen = pygame.display.set_mode(size)
    graphics_demo()

