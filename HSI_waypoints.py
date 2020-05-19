import math
from HSI_math import *
from HSI_draw import *

# Load navaid database -- store in dictionary named navaid_list -- complete
def load_navaid_list():
    navaid_list = {}
    with open('NAV.txt','r') as nav_data:
        for line in nav_data:
            if line[:4]=="NAV1":
                name = line[4:7]
                navaid_type = line[20:29]
    #           Get latitude, make negative if south
                if line[395] == 'N':
                    lat_deg = float(line[385:395])/3600.0
                elif line[395] == 'S':
                    lat_deg = float(line[385:395])/-3600.0
                else:
                    print("Latitude error on line: ",line)
                    return(navaid_list)
    #   	    Get longitude, make negative if west
                if line[420] == 'W':
                    lon_deg = float(line[410:419])/-3600.0
                elif line[420] == 'E':
                    lon_deg = float(line[410:419])/3600.0
                else:
                    print("longitude error on line: ",line)
                    return(navaid_list)
    #           declination stored as 2 digit plus direction right now Mag + East var = True 
                declination = line[481:484]
                navaid_list[name]=Location(name,math.radians(lat_deg),math.radians(lon_deg),declination)
    return(navaid_list)
            
# Load fix database -- store in dictionary named fix_list 
def load_fix_list():
    fix_list = {}
    with open('FIX.txt','r') as nav_data:
        for line in nav_data:
            if line[:4]=="FIX1":
                name = line[4:9]
                fix_type = line[213:231]
                
    #           Get latitude, make negative if south
                if line[78] == 'N':
                    lat_deg = dms_to_deg((line[66:68]),(line[69:71]),(line[72:78]))
                elif line[78] == 'S':
                    lat_deg = -1.0*dms_to_deg((line[66:68]),(line[69:71]),(line[72:78]))
                else:
                    print("Latitude error on line: ",line)
                    return(fix_list)
    #           Get Longitude, make negative if west
                if line[93] == 'W':
                    lon_deg = -1.0*dms_to_deg((line[80:83]),(line[84:86]),(line[87:93]))
    #                print(name, (line[80:83]),(line[84:86]),(line[87:93]))
                elif line[93] == 'E':
                    lon_deg = dms_to_deg((line[80:83]),(line[84:86]),(line[87:93]))
                else:
                    print("longitude error on line: ",line)
                    return(fix_list)
                fix_list[name]=Location(name,math.radians(lat_deg),math.radians(lon_deg),"")
    return(fix_list)      


# Load airport database -- store in dictionary named apt_list 
def load_apt_list():
    apt_list = {}
    with open('APT.txt','r') as nav_data:
        for line in nav_data:
            if line[:3]=="APT":
                name = line[27:31]
                apt_type = line[14:27]
                ICAO_name = line[1210:1214]
               
    #           Get latitude, make negative if south
                if line[549] == 'N':
                    lat_deg = float(line[538:549])/3600.0
                elif line[549] == 'S':
                    lat_deg = float(line[538:549])/-3600.0
                else:
                    print("Latitude error on line: ",line)
                    return(apt_list)

    #   	    Get longitude, make negative if west
                if line[576] == 'W':
                    lon_deg = float(line[565:576])/-3600.0
                elif line[576] == 'E':
                    lon_deg = float(line[565:576])/3600.0
                else:
                    print("Longitude error line: ",line)
                    return(apt_list)
    #           declination stored as 2 digit plus direction right now Mag + East var = True 
                declination = line[586:589]

    #           Use ICAO name if exists
                if ICAO_name[1]!=" ":
                    apt_list[ICAO_name]=Location(ICAO_name,math.radians(lat_deg),math.radians(lon_deg),declination)           
    #           Use 4 leter name if exists
                if name[-1] != " ":
                    apt_list[name]=Location(name,math.radians(lat_deg),math.radians(lon_deg),declination)        
                else: # store 3 letter names
                    apt_list[name[0:3]]=Location(name[0:3],math.radians(lat_deg),math.radians(lon_deg),declination)        
    return(apt_list)

def fp_from_file(filename = "FLIGHTPLAN.txt"):
    with open(filename,'r') as fp_file:
        fp_string = fp_file.readline()

        if fp_string[:1] != "#":
            print("Opened file",filename)
        else:
            fp_string = fp_file.readline()

    if fp_string[-1] == "\n": fp_string = fp_string[:-1]
    fp_string = fp_string.replace('\t',' ').replace(',',' ')

    return(fp_string)

