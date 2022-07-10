from gpiozero import AngularServo

servo = AngularServo(18, min_angle=-22, max_angle=32)

def Stuurhoek(hoek):
    #code voor hoek
    servo.angle = hoek
    print(hoek)