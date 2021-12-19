#---------------------------------------------------------
# Program: Recursion Assignment - RecursionImage.py
# Author: Pearl
# Date: May 15th, 2017
# Description: Upon running program, a picture will be
#              drawn in a pygame window. The picture will
#              feature use of recursion to draw trees,
#              clouds, and a moon. Randomization is also
#              used to simulate nature.
# Inputs: None.
# Output: Picture is drawn in a pygame canvas
#---------------------------------------------------------

import math
import cmath
import time
import pygame
import random

# Colors and color sets, probability of color used within a color set
# is controlled through the frequency at which a color appears in the list
# and is selected by a random function
MOON = [(252,251,227),(252,251,227),(252,251,227),(240,240,216),(240,240,216),(205,215,182),(250,242,248),(250,242,248),(235,239,201),(235,239,201)]
SKY = [(50,51,58),(46,51,62),(42,51,66),(38,51,70),(34,51,74),(30,51,78), (27,51,81),(23,51,85),(19,51,89),(15,51,93),(11,51,97),(7,51,101),(3,51,105)]
CLOUD = [(209,214,220),(197,205,212),(197,205,212),(197,205,212),(183,195,203),(183,195,203),(183,195,203),(175,185,195),(164,175,187),(153,165,178),(141,156,170)]
DARKRED = (139,0,0)
ORANGE = (254, 102, 13)
GREEN = [(0,100,0),(0,100,0),(0,95,0),(0,95,0),(0,90,0),(0,85,0),(0,60,0)]
BARK = (82,54,27)
WHITE = (255,255,255)

# [Tree]: The probability of an extra branch being grown is a fixed 1 in 4 ratio
# which is selected by a random function 
Prob = [2,3,2,2]

pygame.init()
Canvas = pygame.display.set_mode((1300, 800))

# [Sky]: Sky is a fixed "gradient" created through drawing rectangles of fixed dimensions
# onto pygame canvas, color is selected chronologically through the "SKY" color set
yLoc = 0
ySpace = int(800/len(SKY))
for color in SKY:
    pygame.draw.rect(Canvas, color, (0, yLoc, 1300, ySpace))
    yLoc += ySpace
    
# [Moon]:
class Circles(): # All circles in the Apollo Gasket is a circle object, has: radius, (x,y) position, and a curvature

    def __init__(self, x, y, radius):
        self.r = radius
        self.pos = (x + y*1j) # Position of circle is stored as a real number and an imaginary number
                              # instead of a tuple or a list. X is defined as the real number, Y is
                              # defined as the imaginary number. 

    def curvature(self): # Circle's curvature is the reciprocal of its radius
        return 1/self.r
    
def outerTangCirc(circle1, circle2, circle3): # Function calculates a 4th tangent circle that encloses 3 tangent circles
    curv1 = circle1.curvature() 
    curv2 = circle2.curvature()
    curv3 = circle3.curvature()
    pos1 = circle1.pos
    pos2 = circle2.pos
    pos3 = circle3.pos
    
    # New position and curvature is calculated with Vieta's formula
    curv4 = -2 * cmath.sqrt(curv1*curv2 + curv2*curv3 + curv1*curv3) + curv1 + curv2 + curv3 
    pos4 = (-2 * cmath.sqrt(curv1*pos1*curv2*pos2 + curv2*pos2*curv3*pos3 + curv1*pos1*curv3*pos3 ) + curv1*pos1 + curv2*pos2 + curv3*pos3)/curv4
    circle4 = Circles(pos4.real, pos4.imag, 1/curv4) # New information is created into a Circles object
    return circle4

def innerTangCirc(circle2, circle3, circle4): # Function calculates an enclosed tangent circle, as well as a circle that encloses them
    r2 = circle2.r
    r3 = circle3.r
    r4 = circle4.r

    circle2 = Circles(0,0, r2)
    circle3 = Circles(r2 + r3, 0 , r3)
    x_of_4 = (r2*r2 + r2*r4 + r2*r3 - r3*r4)/(r2+r3)
    y_of_4 = cmath.sqrt((r2 + r4)*(r2 + r4) - x_of_4*x_of_4)
    circle4 = Circles(x_of_4, y_of_4, r4) # 4th circle created here
    circle1 = outerTangCirc(circle2, circle3, circle4) # Function calls outerTangCirc(function) to create external circle
    return (circle1, circle2, circle3, circle4)

def secSolution(fixedCirc, circle1, circle2, circle3): # Function that is able to generate circles based on known information on existing circles
    curvF = fixedCirc.curvature()
    curv1 = circle1.curvature()
    curv2 = circle2.curvature()
    curv3 = circle3.curvature()

    # Variation of Vieta's formula
    newCurv = 2*(curv1 + curv2 + curv3) - curvF
    newPos = (2*(curv1*circle1.pos + curv2*circle2.pos + curv3*circle3.pos) - curvF*fixedCirc.pos)/newCurv
    return Circles(newPos.real, newPos.imag, 1/newCurv)
        
class containGasket(): # Class contains list containing all calculated and generated information on the circle objects

    def __init__(self, circle1, circle2, circle3, circle4):
        self.start = innerTangCirc(circle1, circle2, circle3) # Start with 3 known tangent circles and the enclosing circle
        self.generate = list(self.start) # Start list of objects with 3 known tangent circles

    def ApolloGasket(self, circles, depth, maxDepth): # Generation and recursive calls are made here
        if depth == maxDepth: # Stop if the max depth has been reached
            return
        (circle1, circle2, circle3, circle4) = circles
        if depth == 0: # First depth requires creation of the enclosed circle
            specialCirc = secSolution(circle1, circle2, circle3, circle4)
            self.generate.append(specialCirc)
            self.ApolloGasket((specialCirc, circle2, circle3, circle4), 1, maxDepth) # Recursive call for next depth

        newCircle2 = secSolution(circle2, circle1, circle3, circle4) # Three circles can be generated based off of which circle is "fixed"
        self.generate.append(newCircle2)                             # For depth "n" we get total of 2*3^(n+1) circles
        newCircle3 = secSolution(circle3, circle1, circle2, circle4)
        self.generate.append(newCircle3)
        newCircle4 = secSolution(circle4, circle1, circle2, circle3)
        self.generate.append(newCircle4)

        self.ApolloGasket((newCircle2, circle1, circle3, circle4), depth + 1, maxDepth) # Recursive call for next depth
        self.ApolloGasket((newCircle3, circle1, circle2, circle4), depth + 1, maxDepth) # Three circles generated means three calls to be made
        self.ApolloGasket((newCircle4, circle1, circle2, circle3), depth + 1, maxDepth)

# [Tree]:
def Branching(screen, x1, y1, angle, length, n): # Recursive function to draw tree
    x2 = x1 + length * math.cos(angle)
    y2 = y1 - length * math.sin(angle)
    pygame.draw.line(screen, BARK, (x1,y1), (x2, y2), n+5) # Draws branches
    if Prob[random.randrange(4)] == 3: # Draws an extra branch if probability indicates creation of three branches
        Branching(screen, x2, y2, angle, length* 0.8, n-1)
    if n > 0: # Recurse if max depth has not been reached
        Branching(screen, x2, y2, angle + (0.14 * random.randrange(1, 6)), length* 0.8, n-1)
        Branching(screen, x2, y2, angle - (0.14 * random.randrange(1, 6)), length* 0.8, n-1)
    if n < 3: # Draws leaves during the last three recursion depths
        pygame.draw.circle(screen, GREEN[random.randrange(len(GREEN))], (int(x2)+random.randrange(5,10),int(y2)+random.randrange(5,10)), random.randint(15,28))
    if (n <= 4) and(Prob[random.randrange(4)] == 3): # Draws oranges if during last four recursion depths, and fixed probability is three
            pygame.draw.circle(screen, ORANGE, (int(x2) + random.randint(0,9), int(y2) + random.randint(0,9)), 10)

# [Clouds]:    
def Clouds(screen, x1, y1, n):
    changex = random.randint(5,15)
    changey = random.randint(-3,6)
    if n > 0: # Recurse if max depth has not been reached
        pygame.draw.circle(screen, CLOUD[random.randrange(len(CLOUD))], (x1,y1), 10 + random.randint(7,13))
        Clouds(screen, x1 + changex, y1 + changey, n-1) # Draws a circle above and below the previous circle
        Clouds(screen, x1 + changex, y1 - changey, n - random.randint(2,6))

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#[Main]:

largestRad = 0
r1 = random.randrange(30,100)
r2 = random.randrange(30,100)
r3 = random.randrange(30,100)                                     
randX = random.randrange(100, 1200)
randY = random.randrange(100, 200)

# Calculations using Vieta's formula to find 3 tangent circles
test1 = Circles(randX, randY, r1)
test2 = Circles(randX + r1 + r2, 100, r2)
x3 = randX + (r1*r1 + r1*r3 + r1*r2 - r2*r3)/(r1+r2)
y3 = randY + cmath.sqrt(((r1+r3)*(r1+r3)) - (r1*r1 + r1*r3 + r1*r2 - r2*r3)/(r1+r2)*(r1*r1 + r1*r3 + r1*r2 - r2*r3)/(r1+r2))
test3 = Circles(x3, y3, r3)

# Keep track of the largest radius (has to be the enclosing circle), largest circle must be drawn first 
largestRad = math.fabs(outerTangCirc(test1, test2, test3).r.real)
stuff = containGasket(test1, test2, test3, outerTangCirc(test1, test2, test3)) # Create the Apollo Gasket list of Circles objects
stuff.ApolloGasket(stuff.generate, 0, 6) # Base recursion call

pygame.draw.rect(Canvas, (0,49,0), (0,700,1300,100)) # Draws ground

# [Moon]:
for current in stuff.generate:
    if 0 < int(math.fabs(current.r.real)) < math.fabs(largestRad): # Draws all circles that have a radius over 1, and under the largest radius
        pygame.draw.circle(Canvas, MOON[random.randrange(len(MOON))], (randX + int(current.pos.real), randY + int(current.pos.imag)), int(math.fabs(current.r.real)), 0)
# Pygame does not support float radius, because of this, once circles get small enough, the rounding may cause circles to no longer appear tangent to one another

# [Clouds]:
for x in range(random.randint(0,10)):
    Clouds(Canvas, random.randint(0,1300), random.randint(0, 300), 20)

# [Tree]:
for x in range(20):
    Branching(Canvas, random.randint(0,1300), random.randint(700,800), (math.pi)/2, random.randint(60,80), random.randint(5, 10))

pygame.display.update()