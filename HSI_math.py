import math

def dms_to_deg(deg, mins,sec):
    return float(deg) + float(mins)/60.0 + float(sec)/3600.0

# Check and see if there's an implicit assumption of positive degrees here.
def deg_to_dm(deg):
    if deg < 0:
        neg = True
        deg = -deg
    else:
        neg = False
    deg_out = deg//1.0
    deg = deg - deg_out
    min_out = deg*60
    if neg:
        deg = -deg
    return(deg_out,min_out)

def lead_turn(groundspeed, inbound_course, outbound_course):
    if groundspeed < 180:
        turn_radius = groundspeed**2/5.25062423083/6076 # 11.26 * tan(25 deg)
    else:
        turn_radius = groundspeed/62.8318530718 # 3 deg/sec = 3 min turn ... 20*pi()
    hdg_change = outbound_course - inbound_course
    if hdg_change < 0: hdg_change += 360
    if hdg_change > 360: hdg_change -= 360
    if abs(hdg_change)> 90: hdg_change = 90
    return(turn_radius*math.sin(math.radians(abs(hdg_change))))
    

class Location:
    # Radius of earth in Nautical Miles
    RADIUS = 3440.065
    
    def __init__(self, name, lat, lon, mag_var):
        self.lat = lat
        self.lon = lon
        self.name = name
        self.mag_var = mag_var
     
    def angular_distance_to(self, dest):
        delta_lat = dest.lat - self.lat
        delta_lon = dest.lon - self.lon

        a = math.sin(delta_lat/2)* math.sin(delta_lat/2) + math.cos(self.lat) * math.cos(dest.lat) * math.sin(delta_lon/2) * math.sin(delta_lon/2)
        c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))
        return (c)

    def distance_to(self, dest):
        delta_lat = dest.lat - self.lat
        delta_lon = dest.lon - self.lon
        a = math.sin(delta_lat/2)*math.sin(delta_lat/2) + math.cos(self.lat) * math.cos(dest.lat) * math.sin(delta_lon/2)*math.sin(delta_lon/2)
        c = 2 * math.atan2(math.sqrt(a),math.sqrt(1-a))
        return (Location.RADIUS*c)

    def heading_to(self, dest): #Need to make sure this returns posive values, round to 0 - 359 degrees
        delta_lon = dest.lon - self.lon
        y = math.sin(delta_lon)*math.cos(dest.lat)
        x = math.cos(self.lat)*math.sin(dest.lat) - math.sin(self.lat)*math.cos(dest.lat)*math.cos(delta_lon)
        return math.atan2(y,x)


#    def crosstrack_error(self, start, dest):
#This is from spherical trigenometry, and isn't working
#        dist_start_self = Location.angular_distance_to(self,start) #angular distance
#        heading_start_self = start.heading_to(self)
#        heading_start_end = start.heading_to(dest)
#        xte_angle = math.asin(math.sin(dist_start_self)*math.sin(heading_start_self-heading_start_end))
#       print(dist_start_self * Location.RADIUS)
#        return(xte_angle*Location.RADIUS)

    def crosstrack_error(self, start, dest):
        dist_start_self = Location.angular_distance_to(self, start)
        heading_start_self = start.heading_to(self)
        heading_start_end = start.heading_to(dest)
        xte = math.asin(math.sin(dist_start_self)*math.sin(heading_start_self-heading_start_end))
        return(xte*Location.RADIUS)




    def __repr__(self):
        return(self.name + " at " + str(math.degrees(self.lat)) + " lat and " + str(math.degrees(self.lon)) + " lon, mag var " + self.mag_var)

def load_points():
    zeros = Location("zeros",0,0,"")
    p90E = Location("90E",0,math.pi/2,"")
    p90W = Location("90W",0,-math.pi/2,"")
    p30N = Location("30N",math.pi/3,0,"")
    p30N90W = Location("30N90W",math.pi/3,-math.pi/2,"")
    pole = Location("pole",math.pi/2,0,"")
    p1n = Location("1N",math.radians(1),math.pi/6,"")
    print("available points zeros, p90E,p90W,p30N, p30N90W, pole")

if __name__ == "__main__":
    print("HSI_math contains routines to support the HeadsUp HSI display")

