#custom libraries used
from HSI_math import *
from HSI_draw import *
from HSI_waypoints import *

#system libraries used
import math
import sys
import pygame
from datetime import time, timedelta
import serial
import threading

class Flightplan:
    def __init__(self,wpnames): # eats a list of waypoint names on invocation, else defaults to KFLY to KMLE
        global ground_speed
        wpnames = wpnames.split(" ")
        self.wp_list={}
        if len(wpnames)<2:
            print("inadequate points in flight plan")
            wpnames = "KFLY","KMLE"
            print(type(wpnames))
        wpnum = 1                           # #1 is the first waypoint. Not zero. 
        for point in wpnames:
            wp_to_add = waypoint_by_name(point)
            if wp_to_add == False:
                print("Failed to find waypoint "+point)
            else:
                self.add_waypoint(wpnum,wp_to_add)
                wpnum += 1
        self.fromwpnum = 1
        self.towpnum = 2
        self.heading_to = math.degrees(Location.heading_to(self.wp_list[1],self.wp_list[2]))
        if self.heading_to < 0: self.heading_to +=360
        if 3 in self.wp_list:
            self.heading_out = math.degrees(Location.heading_to(self.wp_list[2], self.wp_list[3]))
            self.lead_distance = lead_turn(ground_speed, self.heading_to, self.heading_out)
        else:
            self.heading_out = self.heading_to
            self.lead_distance = 0

    def __repr__(self):
        return_string = "\n"
        for wpnum in self.wp_list:
            return_string = return_string + str(wpnum) + " " + self.wp_list[wpnum].name + "\n"
        return_string = return_string + "Steering to " + self.wp_list[self.towpnum].name +"\n"
        return(return_string)

    def to_wp(self):
        return(self.wp_list[self.towpnum])

    def from_wp(self):
        return(self.wp_list[self.fromwpnum])


    def update_lead_distance(self,groundspeed):
        lead_distance = lead_turn(groundspeed, heading_to, heading_out)
        if lead_distance < .1: lead_distance = .1 # big enough for fp to sequence at 1 Hz

    def add_waypoint(self,wp_number,name):
        self.wp_list[wp_number] = name

    def next_wp(self):
        global ground_speed
        print("next_wp started")
        if self.towpnum  +1 in self.wp_list:
            self.fromwpnum = self.towpnum
            self.towpnum = self.towpnum + 1
            self.heading_to = self.heading_out
            if self.towpnum + 1 in self.wp_list:
                self.heading_out = math.radians(self.wp_list[self.towpnum].heading_to(self.wp_list[self.towpnum+1]))
                if self.heading_out < 0: self.heading_out += 360
                self.lead_distance = lead_turn(ground_speed,self.heading_to, self.heading_out)
                print("next_wp: sequenced to ",self.wp_list[self.towpnum].name)
            else:
                self.heading_out = self.heading_to
                self.lead_distance = 0
                print("next_wp: sequenced advanced to last leg")
        else:
            print("next_wp: last waypoint reached, sequence failed")

    def prev_wp(self):
        global ground_speed
        if self.fromwpnum - 1 in self.wp_list:
            self.towpnum = self.fromwpnum
            self.fromwpnum = self.fromwpnum - 1
            self.heading_to = self.heading_out
            if self.towpnum + 1 in self.wp_list:
                self.heading_out = math.degrees(self.wp_list[self.towpnum].heading_to(self.wp_list[self.towpnum +1]))
                self.lead_distance = lead_turn(ground_speed,self.heading_to, self.heading_out)
                print("next_wp: sequenced to ",self.wp_list[self.towpnum].name)
        else:
            print("prev_wp: first waypoint reached, sequence failed")

    def new_fp(self, wpnames): # This has not been fixed -- reference class def
        global groundspeed
        wp_list={}
        if not isinstance(wpnames,tuple):
            print("new flight plan is not a list of points")
            return(False)
        if len(wpnames)<2:
            print("inadequate points in flight plan")
            return(False)
        wpnum = 1                           #1 is the first waypoint. Not zero. 
        for point in wpnames:
            wp_to_add = waypoint_by_name(point)
            if wp_to_add == False:
                print("Failed to find waypoint "+point)
                return(False)
            wp_list.add_waypoint(wpnum,wp_to_add)
            wpnum += 1
        fromwpnum = 1
        towpnum = 2
        heading_to = heading_to(wp_list[1].wp_list[2])
        if 3 in wp_list:
            heading_out = heading_to(wp_list[2].wp_list[3])
            lead_distance = lead_turn(groundspeed, heading_to, heading_out)
        else:
            heading_out = heading_to
            lead_distance = 0
        return(True)


# This section stays in the main module so we don't pass waypoint databases to the lookup

def waypoint_by_name(wpt_name):
    if len(wpt_name)==2:
        if wpt_name+" " in navaid_list:
            return(navaid_list[wpt_name])
        else:
            return(False)
    if len(wpt_name)==3: # For 3 digit locations, look for navaid first
        if wpt_name in navaid_list:
            return(navaid_list[wpt_name])
        elif wpt_name in apt_list:
            return(apt_list[wpt_name])
        else:
            return(False)
    elif len(wpt_name)== 5:
        if wpt_name in fix_list:
            return(fix_list[wpt_name])
        else:
            return(False)
    elif len(wpt_name) == 4:
        if wpt_name in apt_list:
            return(apt_list[wpt_name])
        elif (wpt_name[0]=="K" or wpt_name[0]=="P") and (wpt_name[-3:] in apt_list):
            result = apt_list[wpt_name[-3:]]
            result.name = wpt_name
            return(result)
        else:
            return(False)
    else:
        return(False)

def nearest_navaid(self):
    distance = 3 #unreasonably larger number, in radians
    for navaid in navaid_list:
        diamond_range = abs(self.lon - navaid_list[navaid].lon)+abs(math.sin(self.lon)*(self.lat-navaid_list[navaid].lat))
#        print (navaid, diamond_range)
        if diamond_range < distance:
            distance = diamond_range
            nearest = navaid
            print("  "+navaid)
    return(nearest)

"""
This is just a graphics demo, but I'll build the real time loop inside this demo
"""

def main_graphics_loop():
    global position
    global direct_wp
    global ground_track
    global ground_speed
    global HSI_mode

    # some initial values
    runticks = 0 # used to sequence flight plan
    bug = 0
    dct_course = 0 # so it doesn't get passed before assigned
    clock = pygame.time.Clock()

    print("Screen in main_graphics_demo() is, ",screen)
    while 1:
        # Handle keystrokes
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.display.quit()
                    return()
                if event.key == pygame.K_w: #  W and E to change heading
                    if HSI_mode == "fp": fp.prev_wp()
                    if HSI_mode in ("ground","fp bug","dct bug"): bug -= 1
                    if HSI_mode == "dct": dct_course -= 1
                    if dct_course < 0: dct_course +=360
                    if bug < 0 : bug +=360

                if event.key == pygame.K_e:
                    if HSI_mode == "fp": fp.next_wp()
                    if HSI_mode in ("ground","fp bug","dct bug"): bug += 1
                    if HSI_mode == "dct": dct_course += 1
                    if dct_course > 360: dct_course -=360
                    if HSI_mode == "dct bug": bug += 1
                    if bug > 360: bug -= 360

                if event.key == pygame.K_m: # M to cycle through modes (switch push on the final object)
                    if HSI_mode == "fp":
                        new_mode = "fp bug"
                        bug = hdg
                    elif HSI_mode == "fp bug":
                        new_mode = "dct"
                        direct_wp = position
                        dct_course = round(math.degrees(position.heading_to(fp.to_wp()))) # dct to to_wp
                        if dct_course < 0: dct_course += 360
                    elif HSI_mode == "dct":
                        new_mode = "dct bug"
                        bug = hdg
                    elif HSI_mode == "dct bug":
                        new_mode = "fp"
                    else:
                        new_mode = "fp" # debugging to fp, reality stay in "ground"
                        print("bad mode shift from ",HSI_mode)
                    HSI_mode = new_mode
                    print(HSI_mode)

        # variable assignments help debugging
        dtg = position.distance_to(fp.to_wp())
        if ground_speed > 0:
            ETA = datetime.utcnow() + timedelta(seconds = dtg/ground_speed * 3600)
        else:
            ETA = datetime.utcnow()
        hdg = ground_track  # this is a hack until the compass works
        if HSI_mode in ("dct","dct bug"): # set_course is to display the arrow
            set_course = dct_course
        else:
            set_course = fp.heading_to
        xte = position.crosstrack_error(fp.from_wp(), fp.to_wp())
        print(xte)
        # one second update loop is in this section (because I don't 
        # want to deal with atomicity in third thread)
        runticks += 1
        if runticks % 20 == 0 :
            if dtg < fp.lead_distance: fp.next_wp() # check for sequencing
            #print(HSI_mode,dct_course, fp.to_wp())

        # now draw this update to the screen
        draw_blank_screen()
        draw_ETA(ETA,HSI_mode)
        draw_distance(dtg)      # pass DTG in NM
        draw_steering_mode(fp.from_wp().name,fp.to_wp().name,set_course,HSI_mode)    # pass text, third is  mode (true_false)
        draw_compass_rose(hdg)
        draw_MH_num(hdg)
        if HSI_mode in ("fp bug","dct bug","ground"):
            draw_HDG_bug(hdg,bug)
        draw_lubber_line()
        draw_direct_diamond(hdg,math.degrees(position.heading_to(fp.to_wp())))
        draw_FP_course(hdg, set_course)
        draw_gnd_track(hdg,ground_track) # also called the drift indicator 
        draw_gnd_speed(ground_speed)
        draw_z_time()
        if HSI_mode in ("ground","fp","fp bug"):
            draw_CDI_scale("enroute")
            draw_CDI_needle(position.crosstrack_error(fp.from_wp(), fp.to_wp()),"enroute")
        else:
            draw_CDI_scale("direct")
            draw_CDI_needle(dct_course - fp.heading_to,"direct")

        pygame.display.flip()
        msElapsed = clock.tick(20) # sets framerate at 20 fps

"""
This codee is the GPS thread.
Halfassed effort has been made to make sure that this is
all thread safe. However, no verification has been done.
Assumption is that nothing other than heading can change fast
inside a second, so if other modueles read inside the parse
function, getting a slightly erred position isn't a big deal.
"""

def read_from_port(gps):
    connected = True
    message =" "
    while connected:
        try:
            reading = gps.readline().decode("ascii")
        except:
            print("GPS serial port died")
            return()
        if len(reading)>0 and reading[0] == "$": #sometimes don't get the whole message. This sends the last line to the parser, not the current one
           parse_GPS(message)
           message = reading
        else:
            message = message + reading
    gps.close()

def parse_GPS(reading):

    global position
    global ground_track
    global ground_speed
    global HSI_mode

    words = reading.split(',')
    if reading[3:6]=="GLL": print(words[6],end="")

    if reading[3:6] =="GLL":
        words = reading.split(",")
        lat = dms_to_deg(float(words[1][0:2]),float(words[1][2:]),0)
        if words[2] == "S":
            lat = -lat
        lon = dms_to_deg(float(words[3][0:3]),float(words[1][3:]),0)
        if words[4] == "W":
            lon = -lon

        position.lat = math.radians(lat)
        position.lon = math.radians(lon)
#        print("position",position.lat, position.lon)

    if reading[3:6] =="VTG":
        words = reading.split(",")
#        print("ground track",words[1])
        if words[1]=="":
            ground_track = 0
        else:
            ground_track = float(words[1])
        if words[5] == "":
            ground_speed = 0.0
        else:
            ground_speed = float(words[5])
        if HSI_mode == "ground" and  ground_speed > 30:
            HSI_mode = "fp bug"
            print ("Mode change from gound to FP")
#        print(".", end = "")
#        sys.stdout.flush()

"""
This is where the code starts to run
"""

HSI_mode = "ground"
ground_speed = 0.1 # dummy variable to make the flight plan load
position = Location("position",0,0,"") # force position to be a type Location

# setup serial and threads
print("Connecting to GPS")
connected = True
port = '/dev/ttyACM0'
baud = 9600

try:
    gps = serial.Serial(port, baud, timeout = 0)
    gps_thread = threading.Thread(target=read_from_port, args=(gps,))
    gps_thread.daemon = True        # want the GPS thread to die when it's done. 
    gps_thread.start()
except:
    connected = False
    print("GPS Comm port failed to open")

# load navaids
navaid_list = load_navaid_list()
print("Navaids: ",len(navaid_list))
fix_list = load_fix_list()
print("Fixes:   ",len(fix_list))
apt_list = load_apt_list()
print("Airport: ",len(apt_list))


# load flight plan from file
if len(sys.argv)==2:
    print("Flightplan opening " + str(sys.argv[1]))
    fp = Flightplan(fp_from_file(sys.argv[1]))
else:
    fp = Flightplan(fp_from_file())
print(fp) # this is delayed so that the flightplan can use the lists above

# initialize variables if in demo mode

if connected == False:
    print("setting demo mode")
    position = Location("position",math.radians(39.0917),math.radians(-104.8728),"") # Monument, CO
    ground_track = 90
    HSI_mode = "fp"

# start the graphics loop
screen = draw_init()
main_graphics_loop()

print("main thread is exiting")
gps.close()

