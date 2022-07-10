from gpiozero import AngularServo

#hoek is nog niet goed of wel geen idee
servo = AngularServo(18, min_angle=-35, max_angle=35, min_pulse_width=0.001, max_pulse_width=0.0018)

def Stuurhoek(hoek):
    #code voor hoek
    servo.angle = hoek
    print(hoek)