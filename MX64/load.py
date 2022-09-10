import MX64 as mx
import time

mx_3=mx.MX64(3)
mx_4=mx.MX64(4)
mx_5=mx.MX64(5)
mx_6=mx.MX64(6)

mx_3.movingspeed_cw(40)
mx_4.movingspeed_cw(40)
mx_5.movingspeed_cw(40)
mx_6.movingspeed_cw(60)

# shrink (initial pose)
mx_6.goal_position(2560)

time.sleep(3)

# table down (initial pose)
mx_3.goal_position(2048)
mx_4.goal_position(2048) 
mx_5.goal_position(2048)

time.sleep(5)

# table up
mx_3.goal_position(1229) 
mx_4.goal_position(1229)
mx_5.goal_position(1229)

time.sleep(5) 

# table down
mx_3.goal_position(2048)
mx_4.goal_position(2048)
mx_5.goal_position(2048)

print('end')
