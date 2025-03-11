import pyb
from pyb import UART
import ustruct
import sensor

uart = UART(3,115200,bits=8, parity=None, stop=1, timeout_char = 1000)#初始化串口

roi1 = [( 20,  105, 10, 10),
        ( 45,  105, 10, 10),
        ( 75,  105, 10, 10),
        (105,  105, 10, 10),
        (130,  105, 10, 10)]

led = pyb.LED(1)
led.on()

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.set_vflip(True)  #垂直方向翻转
sensor.skip_frames(time=2000)
sensor.set_auto_whitebal(True)#自动白平衡模式
sensor.set_auto_gain(False)#关闭自动增益模式

GROUND_THRESHOLD=(0, 30, -22, 23, -128, 80)


def send_five_uchar(c1,c2,c3,c4,c5):#功能发送五个无符号字符（unsigned char）
    global uart;
    data = ustruct.pack("<BBBBBBBB",
                   0xA5,
                   0xA6,
                   c1,
                   c2,
                   c3,
                   c4,
                   c5,
                   0x5B
                   )
    uart.write(data);
    print(data)

GROUND_THRESHOLD=(0, 30, -22, 23, -128, 80)

while(True):
    data=0
    blob1=None
    blob2=None
    blob3=None
    blob4=None
    blob5=None
    flag = [0,0,0,0,0]
    img = sensor.snapshot().lens_corr(strength = 1.7 , zoom = 1.0)#对获取到的图像执行镜头校正
    blob1 = img.find_blobs([GROUND_THRESHOLD], roi=roi1[0])
    blob2 = img.find_blobs([GROUND_THRESHOLD], roi=roi1[1])
    blob3 = img.find_blobs([GROUND_THRESHOLD], roi=roi1[2])
    blob4 = img.find_blobs([GROUND_THRESHOLD], roi=roi1[3])
    blob5 = img.find_blobs([GROUND_THRESHOLD], roi=roi1[4])

    if blob1:#如果roi1区域内找到阈值色块 就会赋值flag[0]为1
        flag[0] = 1
    if blob2:
        flag[1] = 1
    if blob3:
        flag[2] = 1
    if blob4:
        flag[3] = 1
    if blob5:
        flag[4] = 1
    print(flag[0],flag[1],flag[2],flag[3],flag[4])
    # send_five_uchar(flag[0],flag[1],flag[2],flag[3],flag[4])

    for i, rec in enumerate(roi1):
        img.draw_rectangle(rec, color=(255,0,0))
        result_text = str(flag[i])
        text_y_position = rec[1] - 15
        img.draw_string(rec[0], text_y_position, result_text, color=(255, 255,
        255), scale=2)

