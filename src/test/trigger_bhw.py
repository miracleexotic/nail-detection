import RPi.GPIO as GPIO
from time import sleep

PWM_PIN = 18
TRIGGER_PIN = 23

GPIO.setmode(GPIO.BCM)
GPIO.setup(PWM_PIN, GPIO.OUT)
GPIO.setup(24, GPIO.IN)
#GPIO.output(24, GPIO.LOW)
GPIO.setup(TRIGGER_PIN, GPIO.IN)
# sleep(5)

pwm = GPIO.PWM(PWM_PIN,0.5)#freq  
pwm.start(50) #50%duty cycle

i = 0

def run(arg):
    import graph
    pwm.stop()
    GPIO.cleanup()

    #GPIO.wait_for_edge(TRIGGER_PIN, GPIO.RISING)
GPIO.add_event_detect(TRIGGER_PIN, GPIO.RISING, callback=run,bouncetime=200)
    #print("falling", i)
    #i+=1
#runpy.run_path("graph.py")
#GPIO.output(24,GPIO.HIGH)
#import graph as mai

#mai.start()
#pwm.stop()
#GPIO.cleanup()

