import numpy as np
from matplotlib import pyplot as plt
from matplotlib import animation
from matplotlib.patches import Circle, Wedge, Polygon
from matplotlib.collections import PatchCollection
import math
from . import Anchor
from . import Bar

class Two_Bar(object):
    def __init__(self, drive1, drive2, bar1, bar2):
        self.resolution = 360
    
        self.drive1 = drive1
        self.drive2 = drive2
        self.bar1 = bar1
        self.bar2 = bar2
        
        self.set_speeds()
    
        if (drive1.distance_angle_from(drive2.x, drive2.y)[0] + drive1.r + drive2.r) >= (bar1.joint + bar2.length):
            raise NameError('Bars too short!')
        if ((drive1.distance_angle_from(drive2.x, drive2.y)[0] - drive1.r) + bar1.joint) < (bar2.length):
            raise NameError('Bars too long!')
        
        #identify speeds
        self.animationSpeed = self.lcm(drive1.speed, drive2.speed)
        
        
    def gcd(self, a, b): return math.gcd(a,b) if a and b else 0

    def lcm(self, a, b): return abs(a * b) / math.gcd(a,b) if a and b else 0

    def set_speeds(self):
    
        if self.drive1.speed == self.drive2.speed:
            #Equal (3, 3)
            self.totalFrames = self.resolution
        else:
            gcd = self.gcd(self.drive1.speed, self.drive2.speed)
            lcm = self.lcm(self.drive1.speed, self.drive2.speed)
            
            if gcd > 1:
                if gcd == self.drive1.speed:
                    #Equally divisible (3, 6)
                    self.totalFrames = int((self.drive2.speed / gcd)  * self.resolution)
                elif gcd == self.drive2.speed:
                    #Equally divisible (6, 3)
                    self.totalFrames = int((self.drive1.speed / gcd)  * self.resolution)
                else: 
                    #Common divisor (14, 21)
                    self.totalFrames = int(gcd  * self.resolution)
            else:
                #Coprimes (14, 15)
                self.totalFrames = int(self.drive1.speed * self.drive2.speed  * self.resolution)
                
        self.stepSize = self.totalFrames / self.resolution

    def sides_to_angle(self, A, B, C):
        #cosine law
        out = np.arccos((A * A + B * B - C * C)/(2.0 * A * B))
        return out
        
    def line_end(self, x, y, r, angle):
        x = x + np.cos(angle) * r
        y = y + np.sin(angle) * r
        return x, y
        
    def end_path(self, i):        
        #drive 1
        angle1 = i * self.drive1.speed
        drive1X, drive1Y = self.drive1.base_point(angle1)
        
        #drive 2
        angle2 = i * self.drive2.speed
        drive2X, drive2Y = self.drive2.base_point(angle2)
        
        driveLengthR, driveAngle = self.drive1.base_point_distance(angle1, angle2, self.drive2)
        
        angle = self.sides_to_angle(self.bar1.joint, driveLengthR, self.bar2.length)
        
        barEnd = self.line_end(drive1X, drive1Y, self.bar1.length, angle + driveAngle)
        
        return barEnd

    def define_speed(self):
        if drive1.speed == 0:
            animate['frames'] = 360 / np.abs(drive2.speed)
            animate['delay'] = 100 / np.abs(drive2.speed)
        elif drive2.speed == 0:
            animate['frames'] = 360 / np.abs(drive1.speed)
            animate['delay'] = 100 / np.abs(drive1.speed)
        elif np.abs(drive1.speed) > np.abs(drive2.speed):
            lcm = lcm(np.abs(drive1.speed), np.abs(drive2.speed))
            print(lcm)
            animate['frames'] = int(lcm)
            lowest = lcm / np.abs(drive2.speed)
            animate['frames'] = int(lowest) * 360
            
            drive2['interval'] = 360 * lowest * drive2.speed
            print(drive2['interval'])
            #drive2['interval'] = (lcm / drive1.speed) / 360
            
            drive1['interval'] = drive1.speed
            
            animate['delay'] = 100 # / np.abs(drive2.speed)
            #animate = { 'delay': 100 / np.abs(drive2.speed), 'frames':  np.abs(drive2.speed)}
            speed2 = 1
            speed1 = np.abs(drive1.speed / drive2.speed)
        else:
            lcm = lcm(np.abs(drive1.speed), np.abs(drive2.speed))
            print(lcm)
            animate = { 'delay': 100 / np.abs(drive1.speed), 'frames':  np.abs(drive1.speed)}
            speed1 = 1
            speed2 = np.abs(drive2.speed / drive1.speed)
    