import threading
import os
import pygame
import math
import time
import sys
import random
import numpy 
import asyncio

# from Detect_Vehicles 
# Detect_Vehicles will provide the number of Vehicles on the basis of which the following algorithm will decide the Green signal timing of respective road 

#default minimum and maximum values of signal
default_Min = 8
default_Max = 80

# Default Red,Yllow,Grn signal time values 
default_red_time = 150   
default_yellow_time = 5
default_green_time = 10

# Number of Vehicles at Traffic Signal and no of lanes 
no_of_lanes = 2
cnt_of_bikes = 0
cnt_of_bus =0
cnt_of_rickshaws = 0
cnt_of_ambulance = 0
cnt_of_cars = 0
cnt_of_trucks = 0


Signals = []
Elapsed_time = 0
no_of_signal = 4
Simulation_Time = 1000  
crnt_green = 0   # shows which signal is Grn currently
nxt_green = (crnt_green+1)%no_of_signal
crnt_yellow = 0   # shows whether Yllow signal is currently on or off , this helps to synchronize next Grn with it

# Average vehicle time to pass the intersection as per their vehicle class
avg_truck_time = 1.5
avg_rickshaw_time = 1.5
avg_car_time = 1.1
avg_bike_time = 0.6
avg_bus_time = 1.5
avg_ambulancea_time = 1.5


# Red signal time at which vehilcles will be detected at a next signal
detection_time = 5

# Avg speeds of each Vehicles using dictionary
speed = {'Car':1.2, 'Bus':0.9, 'Truck':0.8, 'Rickshaw':1.3, 'Bike':1.3, 'Ambulance':1.4}  

# Vehicle= start point coordinates for each Dirctn using dictionary
x = {'right':[0,0,0], 'down':[755,727,697], 'left':[1400,1400,1400], 'up':[595,627,660]}    
y = {'right':[318,355,385], 'down':[0,0,0], 'left':[480,458,425], 'up':[800,800,800]}

Vehicls_Dirctn_Wise = {'right': {0:[], 1:[], 2:[], 'crossed':0}, 'down': {0:[], 1:[], 2:[], 'crossed':0}, 'left': {0:[], 1:[], 2:[], 'crossed':0}, 'up': {0:[], 1:[], 2:[], 'crossed':0}}
Vehicle_Typ = {0:'Car', 1:'Bus', 3:'Rickshaw', 2:'Truck', 4:'Bike', 5:'Ambulance'}
Dirctn_No = {0:'right', 1:'down', 2:'left', 3:'up'}

# STOP Line Coordinates at Intersections
Default_Stops = {'right': 530, 'down': 270, 'left': 870, 'up': 575}
Stop_Lines = {'right': 560, 'down': 290, 'left': 860, 'up': 565}
stops = {'right': [530,520,530], 'down': [270,270,270], 'left': [870,870,870], 'up': [575,575,575]}

mid = {'right': {'x':705, 'y':445}, 'down': {'x':695, 'y':450}, 'left': {'x':695, 'y':425}, 'up': {'x':695, 'y':400}}
rotation_ang = 3

# Coordinates of signal image, timer, and vehicle count
signl_coords = [(530,200),(830,200),(830,570),(530,570)]
signl_timer_coords = [(530,180),(830,180),(830,550),(530,550)]
vehicle_cnt_coords = [(480,210),(880,210),(880,550),(480,550)]
vehicle_cnt_txt = ["0", "0", "0", "0"]

# Gap between Vehicles
gap1 = 15    # stopping gap , i.e ~ when signal is Red 
gap2 = 15   # moving gap, i.e ~ when vehicles are moving 

pygame.init()
simulation = pygame.sprite.Group()

class Traffic_Signl:
    def __init__(self, Red, Yllow, Grn, min, max):
        self.Grn = Grn
        self.Yllow = Yllow
        self.Red = Red
        self.min= min
        self.max= max
        self.signalText = "30"
        self.totalGreenTime = 0
        
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicle_class, Dirctn_no, Dirctn, will_turn):
        pygame.sprite.Sprite.__init__(self)
        #creating image of vehicles using sprite and initializing all the parameters of vehicle class
        self.lane = lane
        self.Dirctn = Dirctn
        self.will_turn = will_turn
        self.turned = 0
        self.rotateAngle = 0
        self.crossed = 0
        self.vehicle_class = vehicle_class
        self.speed = speed[vehicle_class]
        self.Dirctn_no = Dirctn_no
        self.x = x[Dirctn][lane]
        self.y = y[Dirctn][lane]
        Vehicls_Dirctn_Wise[Dirctn][lane].append(self)
        self.Index = len(Vehicls_Dirctn_Wise[Dirctn][lane]) - 1
        
        # path is set as "images/"+Dirctn+"/+vehicle_class"+".png" in this Dirctn will change(right,left,up,down) and vehicle_class will change (Car,Bike,Truck,Bus,Ambulance,Rickshaw) and images will be selected respectively
        path = "images/" + Dirctn + "/" + vehicle_class + ".png"
        self.orgnl_img = pygame.image.load(path)
        self.crnt_img = pygame.image.load(path)

    
        if(Dirctn=='right'):
            if(Vehicls_Dirctn_Wise[Dirctn][lane][self.Index-1].crossed==0 and len(Vehicls_Dirctn_Wise[Dirctn][lane])>1):    # this if checks that if more than 1 vehicle in the respective lane of vehicle before it has crossed stop line
                self.stop = Vehicls_Dirctn_Wise[Dirctn][lane][self.Index-1].stop - Vehicls_Dirctn_Wise[Dirctn][lane][self.Index-1].crnt_img.get_rect().width - gap1         # setting stop coordinate as: stop coordinate of next vehicle - width of next vehicle - gap
            else:
                self.stop = Default_Stops[Dirctn] # in else part we kept the stop coordinate as default stop coordinate value declared for that particular Dirctn
            # So Now setting new starting and stopping coordinate
            temp = self.crnt_img.get_rect().width + gap1    
            x[Dirctn][lane] -= temp
            stops[Dirctn][lane] -= temp
        elif(Dirctn=='down'):
            if(len(Vehicls_Dirctn_Wise[Dirctn][lane])>1 and Vehicls_Dirctn_Wise[Dirctn][lane][self.Index-1].crossed==0):  # same as right
                self.stop = Vehicls_Dirctn_Wise[Dirctn][lane][self.Index-1].stop - Vehicls_Dirctn_Wise[Dirctn][lane][self.Index-1].crnt_img.get_rect().height - gap1      # setting stop coordinate as: stop coordinate of next vehicle - width of next vehicle - gap
            else:
                self.stop = Default_Stops[Dirctn]
            temp = self.crnt_img.get_rect().height + gap1
            y[Dirctn][lane] -= temp
            stops[Dirctn][lane] -= temp
        elif(Dirctn=='left'):
            if(len(Vehicls_Dirctn_Wise[Dirctn][lane])>1 and Vehicls_Dirctn_Wise[Dirctn][lane][self.Index-1].crossed==0):  # same as rigt
                self.stop = Vehicls_Dirctn_Wise[Dirctn][lane][self.Index-1].stop + Vehicls_Dirctn_Wise[Dirctn][lane][self.Index-1].crnt_img.get_rect().width + gap1       # setting stop coordinate as: stop coordinate of next vehicle - width of next vehicle - gap
            else:
                self.stop = Default_Stops[Dirctn]
            temp = self.crnt_img.get_rect().width + gap1
            x[Dirctn][lane] += temp
            stops[Dirctn][lane] += temp
        elif(Dirctn=='up'):
            if(len(Vehicls_Dirctn_Wise[Dirctn][lane])>1 and Vehicls_Dirctn_Wise[Dirctn][lane][self.Index-1].crossed==0):  # same as right
                self.stop = Vehicls_Dirctn_Wise[Dirctn][lane][self.Index-1].stop + Vehicls_Dirctn_Wise[Dirctn][lane][self.Index-1].crnt_img.get_rect().height + gap1       # setting stop coordinate as: stop coordinate of next vehicle - width of next vehicle - gap
            else:
                self.stop = Default_Stops[Dirctn]
            temp = self.crnt_img.get_rect().height + gap1
            y[Dirctn][lane] += temp
            stops[Dirctn][lane] += temp
        simulation.add(self)

    def render(self, screen):
        screen.blit(self.crnt_img, (self.x, self.y))

    def move_vehicles(self):
        if(self.Dirctn=='right'):
            if(self.crossed==0 and self.x+self.crnt_img.get_rect().width>Stop_Lines[self.Dirctn]):   # if the image has crossed stop line now
                self.crossed = 1
                Vehicls_Dirctn_Wise[self.Dirctn]['crossed'] += 1
            if(self.will_turn==1):
                if(self.crossed==0 or self.x+self.crnt_img.get_rect().width<mid[self.Dirctn]['x']):
                    if((self.x+self.crnt_img.get_rect().width<=self.stop or (crnt_green==0 and crnt_yellow==0) or self.crossed==1) and (self.Index==0 or self.x+self.crnt_img.get_rect().width<(Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].x - gap2) or Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].turned==1)):                
                        self.x += self.speed
                else:   
                    if(self.turned==0):
                        self.rotateAngle += rotation_ang
                        self.crnt_img = pygame.transform.rotate(self.orgnl_img, -self.rotateAngle)
                        self.x += 2
                        self.y += 1.8
                        if(self.rotateAngle==90):
                            self.turned = 1
                    else:
                        if(self.Index==0 or self.y+self.crnt_img.get_rect().height<(Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].y - gap2) or self.x+self.crnt_img.get_rect().width<(Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].x - gap2)):
                            self.y += self.speed
            else: 
                if((self.x+self.crnt_img.get_rect().width<=self.stop or self.crossed == 1 or (crnt_green==0 and crnt_yellow==0)) and (self.Index==0 or self.x+self.crnt_img.get_rect().width<(Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].x - gap2) or (Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].turned==1))):                
                # (if the image has not reached its stop coordinate or has crossed stop line or has Grn signal) and (it is either the first vehicle in that lane or it is has enough gap to the next vehicle in that lane)
                    self.x += self.speed  # move_vehicles the vehicle
        elif(self.Dirctn=='left'):
            if(self.crossed==0 and self.x<Stop_Lines[self.Dirctn]):
                self.crossed = 1
                Vehicls_Dirctn_Wise[self.Dirctn]['crossed'] += 1
            if(self.will_turn==1):
                if(self.crossed==0 or self.x>mid[self.Dirctn]['x']):
                    if((self.x>=self.stop or (crnt_green==2 and crnt_yellow==0) or self.crossed==1) and (self.Index==0 or self.x>(Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].x + Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].crnt_img.get_rect().width + gap2) or Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].turned==1)):                
                        self.x -= self.speed
                else: 
                    if(self.turned==0):
                        self.rotateAngle += rotation_ang
                        self.crnt_img = pygame.transform.rotate(self.orgnl_img, -self.rotateAngle)
                        self.x -= 1.8
                        self.y -= 2.5
                        if(self.rotateAngle==90):
                            self.turned = 1
                    else:
                        if(self.Index==0 or self.y>(Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].y + Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].crnt_img.get_rect().height +  gap2) or self.x>(Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].x + gap2)):
                            self.y -= self.speed
            else: 
                if((self.x>=self.stop or self.crossed == 1 or (crnt_green==2 and crnt_yellow==0)) and (self.Index==0 or self.x>(Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].x + Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].crnt_img.get_rect().width + gap2) or (Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].turned==1))):                
                # if the image has not reached its stop coordinate or has crossed stop line or has Grn signal and it is either the first vehicle in that lane or it is has enough gap to the next vehicle in that lane
                    self.x -= self.speed  # move the vehicle    
        elif(self.Dirctn=='down'):
            if(self.crossed==0 and self.y+self.crnt_img.get_rect().height>Stop_Lines[self.Dirctn]):
                self.crossed = 1
                Vehicls_Dirctn_Wise[self.Dirctn]['crossed'] += 1
            if(self.will_turn==1):
                if(self.crossed==0 or self.y+self.crnt_img.get_rect().height<mid[self.Dirctn]['y']):
                    if((self.y+self.crnt_img.get_rect().height<=self.stop or (crnt_green==1 and crnt_yellow==0) or self.crossed==1) and (self.Index==0 or self.y+self.crnt_img.get_rect().height<(Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].y - gap2) or Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].turned==1)):                
                        self.y += self.speed
                else:   
                    if(self.turned==0):
                        self.rotateAngle += rotation_ang
                        self.crnt_img = pygame.transform.rotate(self.orgnl_img, -self.rotateAngle)
                        self.x -= 2.5
                        self.y += 2
                        if(self.rotateAngle==90):
                            self.turned = 1
                    else:
                        if(self.Index==0 or self.x>(Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].x + Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].crnt_img.get_rect().width + gap2) or self.y<(Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].y - gap2)):
                            self.x -= self.speed
            else: 
                if((self.y+self.crnt_img.get_rect().height<=self.stop or self.crossed == 1 or (crnt_green==1 and crnt_yellow==0)) and (self.Index==0 or self.y+self.crnt_img.get_rect().height<(Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].y - gap2) or (Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].turned==1))):                
                    self.y += self.speed
            
           
        elif(self.Dirctn=='up'):
            if(self.crossed==0 and self.y<Stop_Lines[self.Dirctn]):
                self.crossed = 1
                Vehicls_Dirctn_Wise[self.Dirctn]['crossed'] += 1
            if(self.will_turn==1):
                if(self.crossed==0 or self.y>mid[self.Dirctn]['y']):
                    if((self.y>=self.stop or (crnt_green==3 and crnt_yellow==0) or self.crossed == 1) and (self.Index==0 or self.y>(Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].y + Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].crnt_img.get_rect().height +  gap2) or Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].turned==1)):
                        self.y -= self.speed
                else:   
                    if(self.turned==0):
                        self.rotateAngle += rotation_ang
                        self.crnt_img = pygame.transform.rotate(self.orgnl_img, -self.rotateAngle)
                        self.x += 1
                        self.y -= 1
                        if(self.rotateAngle==90):
                            self.turned = 1
                    else:
                        if(self.Index==0 or self.x<(Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].x - Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].crnt_img.get_rect().width - gap2) or self.y>(Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].y + gap2)):
                            self.x += self.speed
            else: 
                if((self.y>=self.stop or self.crossed == 1 or (crnt_green==3 and crnt_yellow==0)) and (self.Index==0 or self.y>(Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].y + Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].crnt_img.get_rect().height + gap2) or (Vehicls_Dirctn_Wise[self.Dirctn][self.lane][self.Index-1].turned==1))):                
                    self.y -= self.speed

   
def repeat():
    global crnt_green, crnt_yellow, nxt_green
    while(Signals[crnt_green].Grn>0):   # while the timer of current Grn signal is not zero
        prnt_status()
        update_val()
        if(Signals[(crnt_green+1)%(no_of_signal)].Red==detection_time):    # set time of next Grn signal 
            thread = threading.Thread(name="detection",target=set_time, args=())
            thread.daemon = True
            thread.start()
           
        time.sleep(1)
    crnt_yellow = 1   # set Yllow signal as 'on'
    vehicle_cnt_txt[crnt_green] = "0"
    # reset stop coordinates of lanes and Vehicles
    for i in range(0,3):
        stops[Dirctn_No[crnt_green]][i] = Default_Stops[Dirctn_No[crnt_green]]
        for vehicle in Vehicls_Dirctn_Wise[Dirctn_No[crnt_green]][i]:
            vehicle.stop = Default_Stops[Dirctn_No[crnt_green]]
    while(Signals[crnt_green].Yllow>0):  # while the timer of current Yllow signal is not zero
        prnt_status()
        update_val()
        time.sleep(1)
    crnt_yellow = 0   # set Yllow signal as 'off'
    
    # reset all signal times of current signal to theirdefault times
    Signals[crnt_green].Grn = default_green_time
    Signals[crnt_green].Yllow = default_yellow_time
    Signals[crnt_green].Red = default_red_time
       
    crnt_green = nxt_green # set next signal as Grn signal
    nxt_green = (crnt_green+1)%no_of_signal    # set next Grn signal
    Signals[nxt_green].Red = Signals[crnt_green].Yllow+Signals[crnt_green].Grn    # set the Red time of next to next signal as (Yllow time + Grn time) of next signal
    repeat()     
    
    
# Initialization of Traffic Signals 
def initialize_signals():
    traffic_s1 = Traffic_Signl(0, default_yellow_time, default_green_time, default_Min, default_Max)
    Signals.append(traffic_s1)
    traffic_s2 = Traffic_Signl(traffic_s1.Red+traffic_s1.Yllow+traffic_s1.Grn, default_yellow_time, default_green_time, default_Min, default_Max)
    Signals.append(traffic_s2)
    traffic_s3 = Traffic_Signl(default_red_time, default_yellow_time, default_green_time, default_Min, default_Max)
    Signals.append(traffic_s3)
    traffic_s4 = Traffic_Signl(default_red_time, default_yellow_time, default_green_time, default_Min, default_Max)
    Signals.append(traffic_s4)
    repeat()

# Set time according to formula
def set_time():
    global cnt_of_cars, cnt_of_bikes, cnt_of_bus, cnt_of_trucks, cnt_of_rickshaws,cnt_of_ambulance, no_of_lanes
    global avg_car_time, avg_bus_time, avg_truck_time, avg_rickshaw_time, avg_bike_time, avg_ambulancea_time
    os.system("detecting Vehicles "+Dirctn_No[(crnt_green+1)%no_of_signal])
    cnt_of_cars, cnt_of_bus, cnt_of_trucks, cnt_of_rickshaws, cnt_of_bikes = 0,0,0,0,0
    for j in range(len(Vehicls_Dirctn_Wise[Dirctn_No[nxt_green]][0])):
        vehicle = Vehicls_Dirctn_Wise[Dirctn_No[nxt_green]][0][j]
        if(vehicle.crossed==0):
            variable_class = vehicle.vehicle_class
            cnt_of_bikes += 1
    for i in range(1,3):
        for j in range(len(Vehicls_Dirctn_Wise[Dirctn_No[nxt_green]][i])):
            vehicle = Vehicls_Dirctn_Wise[Dirctn_No[nxt_green]][i][j]
            if(vehicle.crossed==0):
                variable_class = vehicle.vehicle_class
                if(variable_class=='Car'):
                    cnt_of_cars += 1
                elif(variable_class=='Rickshaw'):
                    cnt_of_rickshaws += 1
                elif(variable_class=='Truck'):
                    cnt_of_trucks += 1
                elif(variable_class=='Bus'):
                    cnt_of_bus += 1
                elif(variable_class=='Ambulance'):
                    cnt_of_ambulance += 1 
                #for setting time the most important factor is the count of vehicles so just for this simulation purose we are counting the vehicles directly from it's respective class
                    
    
    #GREEN SIGNAL TIMING ALGORITHM : Timing for Grn signal is calculated by multiplying every number of every vehicle with its average time and if amulance or poice vehicle detected so they will hold twice the priority compared to other Vehicles
    greenTime = math.ceil(((cnt_of_cars*avg_car_time) + (cnt_of_rickshaws*avg_rickshaw_time) + (cnt_of_bus*avg_bus_time) + (cnt_of_trucks*avg_truck_time)+ (cnt_of_bikes*avg_bike_time) + (cnt_of_ambulance*avg_ambulancea_time*2))/(no_of_lanes+1))
    
    print('Green Signal Time: ',greenTime)
    if(greenTime<default_Min):
        greenTime = default_Min
    elif(greenTime>default_Max):
        greenTime = default_Max
    Signals[(crnt_green+1)%(no_of_signal)].Grn = greenTime


# Print the signal timings
def prnt_status():                                                                                           
	for i in range(0, no_of_signal):
		if(i==crnt_green):
			if(crnt_yellow==0):
				print("Green Signal",i+1,"-> R:",Signals[i].Red," Y:",Signals[i].Yllow," G:",Signals[i].Grn)
			else:
				print("Yellow Signal",i+1,"-> R:",Signals[i].Red," Y:",Signals[i].Yllow," G:",Signals[i].Grn)
		else:
			print("Red Signal",i+1,"-> R:",Signals[i].Red," Y:",Signals[i].Yllow," G:",Signals[i].Grn)
	print()

# Update values of the signal timers after every second 
def update_val():
    for i in range(0, no_of_signal):
        if(i==crnt_green):
            if(crnt_yellow==0):
                Signals[i].Grn-=1
                Signals[i].totalGreenTime+=1
            else:
                Signals[i].Yllow-=1
        else:
            Signals[i].Red-=1

# Function for Generating Vehicles in the Simulation 
def gen_vehicles():
    counter = 0
    while(True):
        vehicle_type = random.randint(0,5)
        
        # if Ambulance is detected so on cmd "AMBULANCE DETECTED" will be printed and we've set a counter in this just for simulation purpose to control the generation of Ambulance so that not more than 2 Ambulance in simulation to depict a relastic scenario 
        if(vehicle_type == 5 and counter < 2):
            print("AMBULANCE DETECTED !!")
            counter += 1
            lane_number = random.randint(0,1)
            will_turn = 0
        elif(counter >= 2):
            vehicle_type = random.randint(0,4)
            
        if(vehicle_type==4):
            lane_number = 0
        else:
            lane_number = random.randint(0,1) + 1
        will_turn = 0
        if(lane_number==2):
            temp = random.randint(0,4)
            if(temp<=2):
                will_turn = 1
            elif(temp>2):
                will_turn = 0
        temp = random.randint(0,999)
        Dirctn_no = 0
        Z = [400,800,900,1000]
        if(temp<Z[0]):
            Dirctn_no = 0
        elif(temp<Z[1]):
            Dirctn_no = 1
        elif(temp<Z[2]):
            Dirctn_no = 2
        elif(temp<Z[3]):
            Dirctn_no = 3
        Vehicle(lane_number, Vehicle_Typ[vehicle_type], Dirctn_no, Dirctn_No[Dirctn_no], will_turn)
        time.sleep(0.75) #rest time till generation of next vehicle 

def sim_time():
    global Elapsed_time, Simulation_Time
    while(True):
        Elapsed_time += 1
        time.sleep(1)
        #Using Simulation_Time variable to control the simulation timing and whereas elapsed time keeps a track of how long the simulation is running 
        if(Elapsed_time==Simulation_Time):
            totalVehicles = 0
            print('Lane Wise Vehicle Counts :')
            for i in range(no_of_signal):
                print('Lane',i+1,':',Vehicls_Dirctn_Wise[Dirctn_No[i]]['crossed'])
                totalVehicles += Vehicls_Dirctn_Wise[Dirctn_No[i]]['crossed']
            print('Total Vehicles passed: ',totalVehicles)
            print('Total time passed: ',Elapsed_time)
            print('No. of Vehicles per unit time: ',(float(totalVehicles)/float(Elapsed_time)))
            os._exit(1)
    

class Main:
    thread4 = threading.Thread(name="simulation time",target=sim_time, args=()) 
    thread4.daemon = True
    thread4.start()

    thread2 = threading.Thread(name="initialization",target=initialize_signals, args=())    # initilizing
    thread2.daemon = True
    thread2.start()
    
    # Defining Screensize 
    HEIGHT = 800
    WIDTH = 1400
    screenSize = (WIDTH, HEIGHT)
    screen = pygame.display.set_mode(screenSize)
    pygame.display.set_caption("SMART TRAFFIC CONTROL SIMULATION")

    # Defining black and white colours 
    white = (255, 255, 255)
    black = (0, 0, 0)


    # signal images and font
    greenSignal = pygame.image.load('images/signals/green.png')
    yellowSignal = pygame.image.load('images/signals/yellow.png')
    redSignal = pygame.image.load('images/signals/red.png')
    font = pygame.font.Font(None, 30)

    # Setting background image i.e. Road Intersection Image
    background = pygame.image.load('images/Road_BG.png')


    thread3 = threading.Thread(name="generate vehicles",target=gen_vehicles, args=())    # Generating Vehicles here
    thread3.daemon = True
    thread3.start()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

        screen.blit(background,(0,0))   # display background 
        # displaying Signal (i.e: Grn Yllow or Red)
        for i in range(0,no_of_signal):  
            if(i==crnt_green):
                if(crnt_yellow==1):
                    if(Signals[i].Yllow==0):
                        Signals[i].signalText = "STOP"
                    else:
                        Signals[i].signalText = Signals[i].Yllow
                    screen.blit(yellowSignal, signl_coords[i])
                else:
                    if(Signals[i].Grn==0):
                        Signals[i].signalText = "SLOW"
                    else:
                        Signals[i].signalText = Signals[i].Grn
                    screen.blit(greenSignal, signl_coords[i])
            else:
                if(Signals[i].Red<=10):
                    if(Signals[i].Red==0):
                        Signals[i].signalText = "GO"
                    else:
                        Signals[i].signalText = Signals[i].Red
                else:
                    Signals[i].signalText = "---"
                screen.blit(redSignal, signl_coords[i])
        signalTexts = ["","","",""]

        # displaying signal timers and vehicle counts 
        for i in range(0,no_of_signal):  
            signalTexts[i] = font.render(str(Signals[i].signalText), True, white, black)
            screen.blit(signalTexts[i],signl_timer_coords[i]) 
            displayText = Vehicls_Dirctn_Wise[Dirctn_No[i]]['crossed']
            vehicle_cnt_txt[i] = font.render(str(displayText), True, black, white)
            screen.blit(vehicle_cnt_txt[i],vehicle_cnt_coords[i])

        timeElapsedText = font.render(("Time Elapsed: "+str(Elapsed_time)), True, black, white)
        screen.blit(timeElapsedText,(1100,50))

        # display Vehicles
        for vehicle in simulation:  
            screen.blit(vehicle.crnt_img, [vehicle.x, vehicle.y])
            vehicle.move_vehicles()
        pygame.display.update()

Main()

  
