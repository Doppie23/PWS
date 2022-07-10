from gpiozero import AngularServo

#hoek is nog niet goed of wel geen idee
servo = AngularServo(18, min_angle=-15, max_angle=20)

def Stuurhoek(hoek):
    #code voor hoek
    servo.angle = hoek
    print(hoek)