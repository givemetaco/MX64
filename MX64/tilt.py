# This code is for Dynamixel MX-64 motor using protocol 1.0

import os
from pickle import PROTO
import time


if os.name == 'nt':
    import msvcrt

    def getch():
        return msvcrt.getch().decode()
else:
    import sys
    import tty
    import termios
    fd = sys.stdin.fileno()
    #old_settings = termios.tcgetattr(fd)

    def getch():
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch

import dynamixel_sdk as dy

# Control table address
# Control table address is different in Dynamixel model

ADDR_TORQUE_ENABLE = 24
ADDR_GOAL_POSITION = 30
ADDR_PRESENT_POSITION = 36
ADDR_TORQUE_LIMIT = 34
ADDR_MOVING_SPEED = 32
ADDR_LED = 25
ADDR_GOAL_ACCELERATION =73

LEN_MOVING_SPEED=2

# Protocol version
# See which protocol version is used in the Dynamixel
PROTOCOL_VERSION = 1.0

# Default setting
DXL1_ID = 1                 # Dynamixel#1 ID : 1
DXL2_ID = 7                 # Dynamixel#1 ID : 2
BAUDRATE = 1000000             # Dynamixel default baudrate : 57600
DEVICENAME = '/dev/ttyUSB0'    # Check which port is being used on your controller
# ex) Windows: "COM1"   Linux: "/dev/ttyUSB0" Mac: "/dev/tty.usbserial-*"

TORQUE_ENABLE = 1                 # Value for enabling the torque
TORQUE_DISABLE = 0                 # Value for disabling the torque


# Initialize PortHandler instance
# Set the port pathdlerLinux or PortHandlerWindows
portHandler = dy.PortHandler(DEVICENAME)

# Initialize PacketHandler instance
# Set the protocol version
# Get methods and members of Protocol1PacketHandler or Protocol2PacketHandler
packetHandler = dy.PacketHandler(PROTOCOL_VERSION)


# Open port
if portHandler.openPort():
    print("Succeeded to open the port")
else:
    print("Failed to open the port")
    print("Press any key to terminate...")
    getch()
    quit()
    

# Set port baudrate
if portHandler.setBaudRate(BAUDRATE):
    print("Succeeded to change the baudrate")
else:
    print("Failed to change the baudrate")
    print("Press any key to terminate...")
    getch()
    quit()
    
class MX64:
    def __init__(self,ID:int) -> None:
        self.ID=ID
        
        # Enable Dynamixel Torque
        self.dxl_comm_result, self.dxl_error = packetHandler.write1ByteTxRx(portHandler, self.ID, ADDR_TORQUE_ENABLE, TORQUE_ENABLE)
        if self.dxl_comm_result != dy.COMM_SUCCESS:
            print(f'[#{self.ID} does not exist. check the ID again]')
            exit()
        elif self.dxl_error != 0:
            print("%s fail_2" % packetHandler.getRxPacketError(self.dxl_error))
        else:
            print(f'[#{self.ID} toque enabled]')

        # default torque limit set to 1023(MAX)
        packetHandler.write2ByteTxRx(portHandler,self.ID,ADDR_TORQUE_LIMIT,1023)
        packetHandler.write1ByteTxRx(portHandler,self.ID,ADDR_GOAL_ACCELERATION,0)
        
            
    def set_torque_limit(self,val:int):
        if not(0<=val<1023):
            print(f'[#{self.ID} torque_limit_setting_value_error] input value has to be 0~1023]')
            exit()
        else:
            self.dxl_comm_result,self.dxl_error = packetHandler.write2ByteTxRx(portHandler,self.ID,ADDR_TORQUE_LIMIT,val)
            if self.dxl_comm_result != dy.COMM_SUCCESS:
                print("%s" % packetHandler.getTxRxResult(self.dxl_comm_result))
            elif self.dxl_error != 0:
                print("%s" % packetHandler.getRxPacketError(self.dxl_error))
            else:
                print(f'[#{self.ID} torque_limit_setting success] torque limit set to {val}')
    
    def movingspeed_ccw(self,speed:int):
        if not(0<=speed<=1023):
            print(f'[#{self.ID} move_forward_value_error] input value has to be 0~1023')
            exit()
        else:
            packetHandler.write2ByteTxRx(portHandler,self.ID,ADDR_MOVING_SPEED,speed)
            print(f'[#{self.ID} moving forward] speed : {speed}')
    
    def movingspeed_cw(self,speed:int):
        if not(0<=speed<=1023):
            print(f'[#{self.ID} move_backward_value_error] input value has to be 0~1023')
            exit()
        else:
            packetHandler.write2ByteTxRx(portHandler,self.ID,ADDR_MOVING_SPEED,speed+1024) # add 1024 because moving backward range is (1024~2047)
            print(f'[#{self.ID} moving backward] speed : {speed}')
    
    def led(self,val:int):
        if not(val==0 or val==1):
            print(f'[#{self.ID} LED setting error] value must be 0 or 1')
            exit()
        self.dxl_comm_result,self.dxl_error = packetHandler.write1ByteTxRx(portHandler,self.ID,ADDR_LED,val)
        if self.dxl_comm_result != dy.COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(self.dxl_comm_result))
        elif self.dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(self.dxl_error))
        else:
            if(val==1):
                print(f'[#{self.ID} LED ON]')
            elif(val==0):
                print(f'[#{self.ID} LED OFF]')
    
    
    def set_acceleration(self,val:int):
        if not(0<=val<=254):
            print(f'[#{self.ID} acceleration setting error] value must be 0~254')
            exit()
        self.dxl_comm_result,self.dxl_error = packetHandler.write1ByteTxRx(portHandler,self.ID,ADDR_GOAL_ACCELERATION,val)
        if self.dxl_comm_result != dy.COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(self.dxl_comm_result))
        elif self.dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(self.dxl_error))
        else:
            print(f'[#{self.ID} acceleration set to {val}')
    
    def goal_position(self,position:int):
        if not(0<=position<=4095):
            print(f'[#{self.ID} goal position setting error] value must be 0~4095 (starting point : 2048) ')
            exit()
        self.dxl_comm_result,self.dxl_error = packetHandler.write2ByteTxRx(portHandler,self.ID,ADDR_GOAL_POSITION,position)
        if self.dxl_comm_result != dy.COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(self.dxl_comm_result))
        elif self.dxl_error != 0:
            print("%s" % packetHandler.getRxPacketError(self.dxl_error))
        else:
            print(f'[#{self.ID} goal position set to {position}]')
                
                
def sync_movingspeed_ccw(speed:int,*IDS):
    # Initialize GroupSyncWrite instance
    move_cw_groupSyncWrite = dy.GroupSyncWrite(portHandler, packetHandler, ADDR_MOVING_SPEED, LEN_MOVING_SPEED)
    if not(0<=speed<=1023):
        print("[sync_move_ccw value error] value must be 0~1023")
        exit()
    else:
        speed_parm= [dy.DXL_LOBYTE(dy.DXL_LOWORD(speed)), dy.DXL_HIBYTE(dy.DXL_LOWORD(speed))]
        for ID in IDS:
            print(f'{ID}')
            dxl_addparam_result=move_cw_groupSyncWrite.addParam(ID,speed_parm)
            if dxl_addparam_result != True:
                print("[ID:%03d] groupSyncWrite addparam failed" % ID)
                quit()
        dxl_comm_result=move_cw_groupSyncWrite.txPacket()
        if dxl_comm_result != dy.COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        move_cw_groupSyncWrite.clearParam()


def sync_movingspeed_cw(speed:int,*IDS):
    # Initialize GroupSyncWrite instance
    move_cw_groupSyncWrite = dy.GroupSyncWrite(portHandler, packetHandler, ADDR_MOVING_SPEED, LEN_MOVING_SPEED)
    if not(0<=speed<=1023):
        print("[sync_move_cw value error] value must be 0~1023")
        exit()
    else:
        speed=speed+1024
        speed_parm= [dy.DXL_LOBYTE(dy.DXL_LOWORD(speed)), dy.DXL_HIBYTE(dy.DXL_LOWORD(speed))]
        for ID in IDS:
            print(f'{ID}')
            dxl_addparam_result=move_cw_groupSyncWrite.addParam(ID,speed_parm)
            if dxl_addparam_result != True:
                print("[ID:%03d] groupSyncWrite addparam failed" % ID)
                quit()
        dxl_comm_result=move_cw_groupSyncWrite.txPacket()
        if dxl_comm_result != dy.COMM_SUCCESS:
            print("%s" % packetHandler.getTxRxResult(dxl_comm_result))
        move_cw_groupSyncWrite.clearParam()

#set_accelertion [0~254]
#led (0 or 1)
#movingspeed_cw , movingspeed_ccw [0~1023]
#set_torque_limit [0~1023]
#goal_position[0,4095] (2048이 원점)
#sync_movingspeed_ccw(speed,id,id) 
#sync_movingspeed_cw(속도,모터아이디(여러개))


mx_6=MX64(6)

mx_3=MX64(3)
mx_4=MX64(4)
mx_5=MX64(5)
while True:
    mx_6.movingspeed_cw(60)

    mx_3.movingspeed_cw(40)
    mx_4.movingspeed_cw(40)
    mx_5.movingspeed_cw(40)


    #head down
    mx_3.goal_position(2048)
    mx_4.goal_position(2048)
    mx_5.goal_position(2048)

    time.sleep(15)

    #tilt 1
    mx_3.goal_position(1598)
    mx_4.goal_position(2048)
    mx_5.goal_position(2575)

    time.sleep(7)

    #head down
    mx_3.goal_position(2048)
    mx_4.goal_position(2048)
    mx_5.goal_position(2048)

    time.sleep(15)

    #expand
    mx_6.goal_position(480)

    time.sleep(15)

    #tilt2
    mx_3.goal_position(2575)
    mx_4.goal_position(2048)
    mx_5.goal_position(1598)
    time.sleep(7)


    mx_3.goal_position(2048)
    mx_4.goal_position(2048)
    mx_5.goal_position(2048)


    time.sleep(7)

    mx_6.goal_position(2560)
    time.sleep(7)

#######################

