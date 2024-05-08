import time
import serial

usb_port = '/dev/ttyUSB0'
ser = serial.Serial(usb_port, 115200)

right_speed = 50
left_speed = 0

def base_control(speed, radius):
    pid_controller(50,0.5,10)
    cs = 0
    barr = bytearray([170, 85, 6, 1, 4])
    barr += speed.to_bytes(2, byteorder='little', signed=True)
    barr += radius.to_bytes(2, byteorder='little', signed=True)
    for i in range(2, len(barr)-1):
        cs = cs ^ barr[i]
    barr += cs.to_bytes(1, byteorder='big')
    ser.write(barr)

def rotate(angle):
    radius = 1
    bot_speed = ((right_speed + left_speed) / 2)
    while True:
        bot_angle = read_data()  # Read angle data
        print("Bot Angle:", bot_angle)
        if bot_angle >= angle:
            print("Reached Desired Angle")
            break
        base_control(int(bot_speed), int(radius))

def read_data():
    while True:
        if ser.read(2) == b"\xaa\x55":  # Check for header bytes
            data = ser.read(200)
            for i in range(0, len(data) - 1):
                if data[i] == 0xAA and data[i + 1] == 0x55:
                    # Inertial sensor data starts at index 21
                    return process_angle_data(data[21:30])  # Return processed data
            time.sleep(0.1)  # Adjust as needed

def process_angle_data(data):
    y_angle = int.from_bytes(data[4:6], byteorder="little", signed=True)
    print("Y-Angle:", y_angle)
    actual_angle = (y_angle * 180) / 18000
    print("Actual Angle:", actual_angle)
    return actual_angle

def pid_controller(p,i,d):
    cs = 0
    barr = bytearray([170, 85, 15, 1, 13])
    barr +=p.to_bytes(4,byteorder='little',signed = True)
    barr +=i.to_bytes(4,byteorder='little',signed = True)
    barr +=d.to_bytes(4,byteorder='little',signed = True)
    for i in range(2,len(barr) - 1):
        cs = cs^barr[i]
    barr += cs.to_bytes(1,byteorder='big')
    ser.write(barr)




rotate(270)
