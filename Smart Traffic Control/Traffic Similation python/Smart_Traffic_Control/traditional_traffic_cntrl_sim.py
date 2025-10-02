
import threading
import os
import pygame
import math
import time
import sys
import random
import numpy 

# from Detect_Vehicles 
# Detect_Vehicles will provide the number of Vehicles on the basis of which the following algorithm will decide the Green signal timing of respective road 

#default minimum and maximum values of signal
default_Min =8
default_Max = 80

# Default red,yellow,green signal time values 
default_red_time = 150   
default_yellow_time = 5
default_green_time = 30

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
Simulation_Time = 800
crnt_green = 0   # shows which signal is green currently
nxt_green = (crnt_green+1)%no_of_signal
crnt_yellow = 0   # shows whether yellow signal is currently on or off , this helps to synchronize next green with it

# Average vehicle time to pass the intersection as per their vehicle class
avg_truck_time = 1.75
avg_rickshaw_time = 1.75
avg_car_time = 1.25
avg_bike_time = 0.75
avg_bus_time = 1.75
avg_ambulancea_time = 2


# Red signal time at which vehilcles will be detected at a next signal
detection_time = 5

# Avg speeds of each Vehicles using dictionary
speed = {'Car':2.25, 'Bus':1.8, 'Truck':1.8, 'Rickshaw':2, 'Bike':2.5, 'Ambulance':2.5}  

# Vehicle= start point coordinates for each direction using dictionary
x = {'right':[0,0,0], 'down':[755,727,697], 'left':[1400,1400,1400], 'up':[595,627,660]}    
y = {'right':[318,355,385], 'down':[0,0,0], 'left':[480,458,425], 'up':[800,800,800]}

Vehicles_Direction_Wise = {'right': {0:[], 1:[], 2:[], 'crossed':0}, 'down': {0:[], 1:[], 2:[], 'crossed':0}, 'left': {0:[], 1:[], 2:[], 'crossed':0}, 'up': {0:[], 1:[], 2:[], 'crossed':0}}
Vehicle_Type = {0:'Car', 1:'Bus', 3:'Rickshaw', 2:'Truck', 4:'Bike', 5:'Ambulance'}
Direction_No = {0:'right', 1:'down', 2:'left', 3:'up'}

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
gap1 = 15    # stopping gap , i.e ~ when signal is red 
gap2 = 15   # moving gap, i.e ~ when vehicles are moving 

pygame.init()
simulation = pygame.sprite.Group()

class Traffic_Signl:
    def __init__(self, red, yellow, green, min, max):
        self.green = green
        self.yellow = yellow
        self.red = red
        self.min= min
        self.max= max
        self.signalText = "30"
        self.totalGreenTime = 0
        
class Vehicle(pygame.sprite.Sprite):
    def __init__(self, lane, vehicle_class, direction_no, direction, will_turn):
        pygame.sprite.Sprite.__init__(self)
        #creating image of vehicles using sprite and initializing all the parameters of vehicle class
        self.lane = lane
        self.direction = direction
        self.will_turn = will_turn
        self.turned = 0
        self.rotateAngle = 0
        self.crossed = 0
        self.vehicle_class = vehicle_class
        self.speed = speed[vehicle_class]
        self.direction_no = direction_no
        self.x = x[direction][lane]
        self.y = y[direction][lane]
        Vehicles_Direction_Wise[direction][lane].append(self)
        self.Index = len(Vehicles_Direction_Wise[direction][lane]) - 1
        
        # path is set as "images/"+direction+"/+vehicle_class"+".png" in this direction will change(right,left,up,down) and vehicle_class will change (Car,Bike,Truck,Bus,Ambulance,Rickshaw) and images will be selected respectively
        path = "images/" + direction + "/" + vehicle_class + ".png"
        self.orgnl_img = pygame.image.load(path)
        self.crnt_img = pygame.image.load(path)

    
        if(direction=='right'):
            if(len(Vehicles_Direction_Wise[direction][lane])>1 and Vehicles_Direction_Wise[direction][lane][self.Index-1].crossed==0):    # this if checks that if more than 1 vehicle in the respective lane of vehicle before it has crossed stop line
                self.stop = Vehicles_Direction_Wise[direction][lane][self.Index-1].stop - Vehicles_Direction_Wise[direction][lane][self.Index-1].crnt_img.get_rect().width - gap1         # setting stop coordinate as: stop coordinate of next vehicle - width of next vehicle - gap
            else:
                self.stop = Default_Stops[direction] # in else part we kept the stop coordinate as default stop coordinate value declared for that particular direction
            # So Now setting new starting and stopping coordinate
            temp = self.crnt_img.get_rect().width + gap1    
            x[direction][lane] -= temp
            stops[direction][lane] -= temp
        elif(direction=='down'):
            if(len(Vehicles_Direction_Wise[direction][lane])>1 and Vehicles_Direction_Wise[direction][lane][self.Index-1].crossed==0):  # same as right
                self.stop = Vehicles_Direction_Wise[direction][lane][self.Index-1].stop - Vehicles_Direction_Wise[direction][lane][self.Index-1].crnt_img.get_rect().height - gap1      # setting stop coordinate as: stop coordinate of next vehicle - width of next vehicle - gap
            else:
                self.stop = Default_Stops[direction]
            temp = self.crnt_img.get_rect().height + gap1
            y[direction][lane] -= temp
            stops[direction][lane] -= temp
        elif(direction=='left'):
            if(len(Vehicles_Direction_Wise[direction][lane])>1 and Vehicles_Direction_Wise[direction][lane][self.Index-1].crossed==0):  # same as rigt
                self.stop = Vehicles_Direction_Wise[direction][lane][self.Index-1].stop + Vehicles_Direction_Wise[direction][lane][self.Index-1].crnt_img.get_rect().width + gap1       # setting stop coordinate as: stop coordinate of next vehicle - width of next vehicle - gap
            else:
                self.stop = Default_Stops[direction]
            temp = self.crnt_img.get_rect().width + gap1
            x[direction][lane] += temp
            stops[direction][lane] += temp
        elif(direction=='up'):
            if(len(Vehicles_Direction_Wise[direction][lane])>1 and Vehicles_Direction_Wise[direction][lane][self.Index-1].crossed==0):  # same as right
                self.stop = Vehicles_Direction_Wise[direction][lane][self.Index-1].stop + Vehicles_Direction_Wise[direction][lane][self.Index-1].crnt_img.get_rect().height + gap1       # setting stop coordinate as: stop coordinate of next vehicle - width of next vehicle - gap
            else:
                self.stop = Default_Stops[direction]
            temp = self.crnt_img.get_rect().height + gap1
            y[direction][lane] += temp
            stops[direction][lane] += temp
        simulation.add(self)

    def render(self, screen):
        screen.blit(self.crnt_img, (self.x, self.y))

    def move_vehicles(self):
        if(self.direction=='right'):
            if(self.crossed==0 and self.x+self.crnt_img.get_rect().width>Stop_Lines[self.direction]):   # if the image has crossed stop line now
                self.crossed = 1
                Vehicles_Direction_Wise[self.direction]['crossed'] += 1
            if(self.will_turn==1):
                if(self.crossed==0 or self.x+self.crnt_img.get_rect().width<mid[self.direction]['x']):
                    if((self.x+self.crnt_img.get_rect().width<=self.stop or (crnt_green==0 and crnt_yellow==0) or self.crossed==1) and (self.Index==0 or self.x+self.crnt_img.get_rect().width<(Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].x - gap2) or Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].turned==1)):                
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
                        if(self.Index==0 or self.y+self.crnt_img.get_rect().height<(Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].y - gap2) or self.x+self.crnt_img.get_rect().width<(Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].x - gap2)):
                            self.y += self.speed
            else: 
                if((self.x+self.crnt_img.get_rect().width<=self.stop or self.crossed == 1 or (crnt_green==0 and crnt_yellow==0)) and (self.Index==0 or self.x+self.crnt_img.get_rect().width<(Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].x - gap2) or (Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].turned==1))):                
                # (if the image has not reached its stop coordinate or has crossed stop line or has green signal) and (it is either the first vehicle in that lane or it is has enough gap to the next vehicle in that lane)
                    self.x += self.speed  # move_vehicles the vehicle
        elif(self.direction=='left'):
            if(self.crossed==0 and self.x<Stop_Lines[self.direction]):
                self.crossed = 1
                Vehicles_Direction_Wise[self.direction]['crossed'] += 1
            if(self.will_turn==1):
                if(self.crossed==0 or self.x>mid[self.direction]['x']):
                    if((self.x>=self.stop or (crnt_green==2 and crnt_yellow==0) or self.crossed==1) and (self.Index==0 or self.x>(Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].x + Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].crnt_img.get_rect().width + gap2) or Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].turned==1)):                
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
                        if(self.Index==0 or self.y>(Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].y + Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].crnt_img.get_rect().height +  gap2) or self.x>(Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].x + gap2)):
                            self.y -= self.speed
            else: 
                if((self.x>=self.stop or self.crossed == 1 or (crnt_green==2 and crnt_yellow==0)) and (self.Index==0 or self.x>(Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].x + Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].crnt_img.get_rect().width + gap2) or (Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].turned==1))):                
                # if the image has not reached its stop coordinate or has crossed stop line or has green signal and it is either the first vehicle in that lane or it is has enough gap to the next vehicle in that lane
                    self.x -= self.speed  # move the vehicle    
        elif(self.direction=='down'):
            if(self.crossed==0 and self.y+self.crnt_img.get_rect().height>Stop_Lines[self.direction]):
                self.crossed = 1
                Vehicles_Direction_Wise[self.direction]['crossed'] += 1
            if(self.will_turn==1):
                if(self.crossed==0 or self.y+self.crnt_img.get_rect().height<mid[self.direction]['y']):
                    if((self.y+self.crnt_img.get_rect().height<=self.stop or (crnt_green==1 and crnt_yellow==0) or self.crossed==1) and (self.Index==0 or self.y+self.crnt_img.get_rect().height<(Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].y - gap2) or Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].turned==1)):                
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
                        if(self.Index==0 or self.x>(Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].x + Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].crnt_img.get_rect().width + gap2) or self.y<(Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].y - gap2)):
                            self.x -= self.speed
            else: 
                if((self.y+self.crnt_img.get_rect().height<=self.stop or self.crossed == 1 or (crnt_green==1 and crnt_yellow==0)) and (self.Index==0 or self.y+self.crnt_img.get_rect().height<(Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].y - gap2) or (Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].turned==1))):                
                    self.y += self.speed
            
           
        elif(self.direction=='up'):
            if(self.crossed==0 and self.y<Stop_Lines[self.direction]):
                self.crossed = 1
                Vehicles_Direction_Wise[self.direction]['crossed'] += 1
            if(self.will_turn==1):
                if(self.crossed==0 or self.y>mid[self.direction]['y']):
                    if((self.y>=self.stop or (crnt_green==3 and crnt_yellow==0) or self.crossed == 1) and (self.Index==0 or self.y>(Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].y + Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].crnt_img.get_rect().height +  gap2) or Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].turned==1)):
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
                        if(self.Index==0 or self.x<(Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].x - Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].crnt_img.get_rect().width - gap2) or self.y>(Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].y + gap2)):
                            self.x += self.speed
            else: 
                if((self.y>=self.stop or self.crossed == 1 or (crnt_green==3 and crnt_yellow==0)) and (self.Index==0 or self.y>(Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].y + Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].crnt_img.get_rect().height + gap2) or (Vehicles_Direction_Wise[self.direction][self.lane][self.Index-1].turned==1))):                
                    self.y -= self.speed

   
def repeat():
    global crnt_green, crnt_yellow, nxt_green
    while(Signals[crnt_green].green>0):   # while the timer of current green signal is not zero
        prnt_status()
        update_val()
        if(Signals[(crnt_green+1)%(no_of_signal)].red==detection_time):    # set time of next green signal 
            thread = threading.Thread(name="detection",target=set_time, args=())
            thread.daemon = True
            thread.start()
           
        time.sleep(1)
    crnt_yellow = 1   # set yellow signal as 'on'
    vehicle_cnt_txt[crnt_green] = "0"
    # reset stop coordinates of lanes and Vehicles
    for i in range(0,3):
        stops[Direction_No[crnt_green]][i] = Default_Stops[Direction_No[crnt_green]]
        for vehicle in Vehicles_Direction_Wise[Direction_No[crnt_green]][i]:
            vehicle.stop = Default_Stops[Direction_No[crnt_green]]
    while(Signals[crnt_green].yellow>0):  # while the timer of current yellow signal is not zero
        prnt_status()
        update_val()
        time.sleep(1)
    crnt_yellow = 0   # set yellow signal as 'off'
    
    # reset all signal times of current signal to theirdefault times
    Signals[crnt_green].green = default_green_time
    Signals[crnt_green].yellow = default_yellow_time
    Signals[crnt_green].red = default_red_time
       
    crnt_green = nxt_green # set next signal as green signal
    nxt_green = (crnt_green+1)%no_of_signal    # set next green signal
    Signals[nxt_green].red = Signals[crnt_green].yellow+Signals[crnt_green].green    # set the red time of next to next signal as (yellow time + green time) of next signal
    repeat()     
    
    
# Initialization of Traffic Signals 
def initialize_signals():
    traffic_s1 = Traffic_Signl(0, default_yellow_time, default_green_time, default_Min, default_Max)
    Signals.append(traffic_s1)
    traffic_s2 = Traffic_Signl(traffic_s1.red+traffic_s1.yellow+traffic_s1.green, default_yellow_time, default_green_time, default_Min, default_Max)
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
    os.system("detecting Vehicles "+Direction_No[(crnt_green+1)%no_of_signal])
    cnt_of_cars, cnt_of_bus, cnt_of_trucks, cnt_of_rickshaws, cnt_of_bikes = 0,0,0,0,0
    for j in range(len(Vehicles_Direction_Wise[Direction_No[nxt_green]][0])):
        vehicle = Vehicles_Direction_Wise[Direction_No[nxt_green]][0][j]
        if(vehicle.crossed==0):
            variable_class = vehicle.vehicle_class
            cnt_of_bikes += 1
    for i in range(1,3):
        for j in range(len(Vehicles_Direction_Wise[Direction_No[nxt_green]][i])):
            vehicle = Vehicles_Direction_Wise[Direction_No[nxt_green]][i][j]
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
                    
    
    #GREEN SIGNAL TIMING ALGORITHM : Timing for green signal is calculated by multiplying every number of every vehicle with its average time and if amulance or poice vehicle detected so they will hold twice the priority compared to other Vehicles
    greenTime = 30
    
    print('Green Signal Time: ',greenTime)
    if(greenTime<default_Min):
        greenTime = default_Min
    elif(greenTime>default_Max):
        greenTime = default_Max
    Signals[(crnt_green+1)%(no_of_signal)].green = greenTime


# Print the signal timings
def prnt_status():                                                                                           
	for i in range(0, no_of_signal):
		if(i==crnt_green):
			if(crnt_yellow==0):
				print("Green Signal",i+1,"-> R:",Signals[i].red," Y:",Signals[i].yellow," G:",Signals[i].green)
			else:
				print("Yellow Signal",i+1,"-> R:",Signals[i].red," Y:",Signals[i].yellow," G:",Signals[i].green)
		else:
			print("Red Signal",i+1,"-> R:",Signals[i].red," Y:",Signals[i].yellow," G:",Signals[i].green)
	print()

# Update values of the signal timers after every second 
def update_val():
    for i in range(0, no_of_signal):
        if(i==crnt_green):
            if(crnt_yellow==0):
                Signals[i].green-=1
                Signals[i].totalGreenTime+=1
            else:
                Signals[i].yellow-=1
        else:
            Signals[i].red-=1

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
        direction_no = 0
        Z = [400,800,900,1000]
        if(temp<Z[0]):
            direction_no = 0
        elif(temp<Z[1]):
            direction_no = 1
        elif(temp<Z[2]):
            direction_no = 2
        elif(temp<Z[3]):
            direction_no = 3
        Vehicle(lane_number, Vehicle_Type[vehicle_type], direction_no, Direction_No[direction_no], will_turn)
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
                print('Lane',i+1,':',Vehicles_Direction_Wise[Direction_No[i]]['crossed'])
                totalVehicles += Vehicles_Direction_Wise[Direction_No[i]]['crossed']
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
        # displaying Signal (i.e: green yellow or red)
        for i in range(0,no_of_signal):  
            if(i==crnt_green):
                if(crnt_yellow==1):
                    if(Signals[i].yellow==0):
                        Signals[i].signalText = "STOP"
                    else:
                        Signals[i].signalText = Signals[i].yellow
                    screen.blit(yellowSignal, signl_coords[i])
                else:
                    if(Signals[i].green==0):
                        Signals[i].signalText = "SLOW"
                    else:
                        Signals[i].signalText = Signals[i].green
                    screen.blit(greenSignal, signl_coords[i])
            else:
                if(Signals[i].red<=10):
                    if(Signals[i].red==0):
                        Signals[i].signalText = "GO"
                    else:
                        Signals[i].signalText = Signals[i].red
                else:
                    Signals[i].signalText = "---"
                screen.blit(redSignal, signl_coords[i])
        signalTexts = ["","","",""]

        # displaying signal timers and vehicle counts 
        for i in range(0,no_of_signal):  
            signalTexts[i] = font.render(str(Signals[i].signalText), True, white, black)
            screen.blit(signalTexts[i],signl_timer_coords[i]) 
            displayText = Vehicles_Direction_Wise[Direction_No[i]]['crossed']
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

  
