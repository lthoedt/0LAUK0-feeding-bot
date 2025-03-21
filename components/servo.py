#!/usr/bin/python3
import RPi.GPIO as GPIO
import pigpio
import time

servo = 12

# more info at http://abyz.me.uk/rpi/pigpio/python.html#set_servo_pulsewidth

pwm = pigpio.pi()
pwm.set_mode(servo, pigpio.OUTPUT)

pwm.set_PWM_frequency( servo, 50 )

# print( "0 deg" )
# pwm.set_servo_pulsewidth( servo, 500 ) ;
# time.sleep( 3 )

# print( "90 deg" )
# pwm.set_servo_pulsewidth( servo, 1500 ) ;
# time.sleep( 3 )

# print( "180 deg" )
# pwm.set_servo_pulsewidth( servo, 2500 ) ;
# time.sleep( 3 )

# safe between 1000 and 2000
angle_1 = 500   # 0 deg
angle_2 = 1500  # 90 deg

tdiff = 0.009
total_time = 5 # change total time

n_steps = total_time / tdiff
step_size = (angle_2 - angle_1) / n_steps


# Move to the first angle
pwm.set_servo_pulsewidth(servo, angle_1)
time.sleep(1)

# Move slowly to the second angle
for i in range(int(n_steps)):
    pwm.set_servo_pulsewidth(servo, angle_1 + step_size * i)
    time.sleep(tdiff)

# turning off servo
pwm.set_PWM_dutycycle( servo, 0 )
pwm.set_PWM_frequency( servo, 0)