#!/usr/bin/env pybricks-micropython
from pybricks.hubs import EV3Brick
from pybricks.ev3devices import (Motor, TouchSensor, ColorSensor,
                                 InfraredSensor, UltrasonicSensor, GyroSensor)
from pybricks.parameters import Port, Stop, Direction, Button, Color
from pybricks.tools import wait, StopWatch, DataLog
from pybricks.robotics import DriveBase
from pybricks.media.ev3dev import SoundFile, ImageFile

ev3 = EV3Brick()

rMotor = Motor(Port.A, positive_direction=Direction.COUNTERCLOCKWISE)
lMotor = Motor(Port.D, positive_direction=Direction.COUNTERCLOCKWISE)
cMotor = Motor(Port.C)
colorS = ColorSensor(Port.S3)
ultraS = UltrasonicSensor(Port.S4)

opgavenr = 4
active = 1
glCount = 0

# Hver procentdel afvigelse af lys fra 'threshold' , 
# sætter turn_rate i drivebase 1.5 grader i sekundet
# fx hvis lyset afviger 10 fra 'threshold', så drejer 10*x grader pr. sekund

proportionalGain = 1.5

#Drive base

robot = DriveBase(lMotor, rMotor, wheel_diameter=50, axle_track=172)

#Definer farverne
greyLine = colorS.reflection()
print(greyLine)
robot.turn(-45)
white = colorS.reflection()
print(white)
robot.turn(45)
threshold = (greyLine + white) / 2 #Threshhold hvor sensor skal skifte imellem grå og hvid
blackLines = greyLine / 2 # sort streg
    
#Definere en general drive funktion
def drive(x):
    deviation = colorS.reflection() - threshold

    turnRate = proportionalGain * deviation

    robot.drive(x, turnRate)

    wait(10)    
    
#Definer opgaverne der skal løses
def Opgaver():
    global opgavenr
    opgavenr += 1
    if opgavenr == 1:           #Brudt streg - Tobias
        
        # Mens overfladen er over sort (grå) skal den følge den grå linje 
        while colorS.reflection() > blackLines:
            drive(100)
        robot.drive(100, 0)
        wait(300)

        # Robotten skal dreje 45 grader

        robot.turn(45)

        # Hvis sensoren støder på den grå streg skal den stoppe og dreje -45 grader

        while colorS.reflection() > greyLine:
            robot.drive(100, 0)

        robot.stop()

        robot.turn(-45)
        # Følg den grå linje igen mens farven er over Sort
        # Og så skal den stoppe når det er sort
        while colorS.reflection() > blackLines:
            drive(100)
        # Robotten skal dreje -45 grader

        robot.turn(-45)

        # Kør lige ud og stop ved den grå streg

        while colorS.reflection() > greyLine:
            robot.drive(100, 0)
        wait(750)

        robot.stop()

        # Robotten skal dreje 45 grader og følge den grå linje igen

        robot.turn(45)
        # Nu er den nået til den sidste sorte streg inden første flaske
              
    elif opgavenr == 2:         #Flyt flaske
        speed = 400
        robot.drive(100,0)
        wait(1000)
        flaskTime = 0
        while flaskTime < 90: #drive i given tid
            drive(50)
            flaskTime += 1
        robot.drive(50,90)
        wait(1000) #drejetid
        while ultraS.distance() > 100 : #få længde på ultrasonic sensor
            drive(100)
        robot.straight(50)
        robot.stop()
        cMotor.run_until_stalled(150) # løft klo / flaske
        seeBlack = 0
        robot.drive(100,0)
        wait(2000)
        robot.stop()
        while seeBlack == 0: #Fang i while loop indtil den ser sort
            if colorS.reflection() > blackLines:
                robot.drive(20, 0)
            else:
                seeBlack += 1
        robot.stop()
        cMotor.run_until_stalled(-150) #Sænk klo / flaske
        robot.drive(50, 0)  #Giv flaske et lille kærligt skub for at rette den op
        wait(400)
        robot.stop()
        cMotor.run(0)
        lMotor.run(-speed)
        rMotor.run(-speed)
        wait(2500)
        rMotor.run(50)
        wait(1500)
        lMotor.run(0)
        rMotor.run(0)

    elif opgavenr == 3:         #Vippe - David
        robot.straight(150)     #Robotten kører 150 mm frem
        robot.turn(-90)         #Den drejer til venstre
        while colorS.reflection() > blackLines:
            drive(100)          #Robotten kører indtil den ser en sort streg
        robot.straight(1575)    #Den kører ligeud henover vippen
        vippeTime = 0           #Definerer tiden den skal være på vippen
        while vippeTime < tid:  #Så længe at robotten er på vippen
            drive(100)          #skal den følge linjen ned af vippen 
            vippeTime += 1
        robot.turn(-90)         #Defefter drejer den til venstre efter vippen
        
    elif opgavenr == 4:         # Parallele Streger - Rasmus
        glCount=0               # Definerer glCount variable
        if glCount == 0:        # Checker om glCount er lig med 0
            robot.straight(300) # Kører 300mm lige frem
            robot.turn(-30)     # Drejer 30 grader til venstre
            robot.drive(100, 0) # Robotten begynder at køre lige fremad
            glCount += 1        # Lægger 1 til glCount
        while glCount < 3:      # Loop der kører mens glCount er mindre end 3
            if colorS.reflection() > threshold:     # Checker om farvesensorerens reflection er højere end threshold
                glCount += 1    # Lægger 1 til glCount
                wait(1500)      # Venter i 1500ms
        robot.straight(20)      # Kører 20mm lige frem
        robot.turn(30)          # Drejer 30 grader til højre
    
    elif opgavenr == 5:         #Målskive - Simon
        robot.straight(170)
        robot.turn(-90)

        while colorS.reflection() > blackLines:
            drive(100)
        robot.straight(500)
        robot.turn(-40)

        cMotor_Stalled=0
        robot.reset()
        while cMotor_Stalled != 1:
            if ultraS.distance() < 80:
                robot.stop()
                Distance_to_bottle=robot.distance()
                print("Distance to bottle: " + str(Distance_to_bottle))
                cMotor.run_until_stalled(150)
                cMotor_Stalled = 1

            else:
                robot.drive(100,0)

        robot.straight(-Distance_to_bottle-220)
        print(1)
        cMotor.run_until_stalled(-150)
        print(2)
        robot.straight(20)
        robot.straight(-280)
        robot.turn(-140)

        while True:
            if colorS.reflection() > threshold:    
                robot.drive(100,0)
            else:
                robot.straight(100)
                robot.turn(-90)
                break

    elif opgavenr == 6:         #Undvig flaske 1 - Mohamad
        robot.stop()
        lMotor.run(-200)
        rMotor.run(200)
        wait(881)
        lMotor.run(298.08)
        rMotor.run(200)
        wait(7168)

    elif opgavenr == 7:         #murparkour skrrrt - Faur
        robot.stop()
        drivespeed = 200
        lMotor.run(drivespeed)
        rMotor.run(drivespeed)         # før svinget
        wait(4520)
        lMotor.run(drivespeed)          # sving 1
        rMotor.run(drivespeed*4.1524)
        wait(473.94)
        lMotor.run(drivespeed*1.7591)  # sving 2
        rMotor.run(drivespeed)
        wait(3935.97)
        lMotor.run(drivespeed)         #  3
        rMotor.run(drivespeed*4.1524)
        wait(473.94)
        lMotor.run(drivespeed)     # efter svinget
        rMotor.run(drivespeed)
        wait(4520)

    elif opgavenr == 8:         #Undvig flaske 2 - Mohamad
        robot.stop()
        lMotor.run(-200)
        rMotor.run(200)
        wait(881)
        lMotor.run(298.08)
        rMotor.run(200)
        wait(7168)
        lMotor.run(200)
        rMotor.run(200)
        wait(700)
        lMotor.run(-200)
        rMotor.run(200)
        wait(881)

    elif opgavenr == 9:         #Landingsbane - Thomas
        global active
        robot.straight((340/2) * 10)
        active = 2

while active == 1:
    drive(100)
    if colorS.reflection() < blackLines:
        Opgaver()

while active == 2:
    robot.stop()
    #Insert Music
    active = 3
    