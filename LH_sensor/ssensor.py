#!coding:utf-8
import time

def crc16_cal(datalist):
    test_crc=0xFFFF                 #预置1个16位的寄存器为十六进制FFFF（即全为1），称此寄存器为CRC寄存器；
    poly=0xa001
    # poly=0x8005
    numl=len(datalist)
    for num in range(numl):
        data=datalist[num]
        test_crc=(data&0xFF)^test_crc   #把第一个8位二进制数据（既通讯信息帧的第一个字节）与16位的CRC寄存器的低8位相异或，把结果放于CRC寄存器，高八位数据不变；
        """
        （3）、把CRC寄存器的内容右移一位（朝低位）用0填补最高位，并检查右移后的移出位；
        （4）、如果移出位为0：重复第3步（再次右移一位）；如果移出位为1，CRC寄存器与多
            项式A001（1010 0000 0000 0001）进行异或；
        """
        #右移动
        for bit in range(8):
            if(test_crc&0x1)!=0:
                test_crc>>=1
                test_crc^=poly
            else:
                test_crc>>=1
    #print(hex(test_crc))
    return [test_crc&0xFF,test_crc>>8]



class EEPROM(object):
    ID = 0x05
    MIN_POSITION_H = 0x09
    MIN_POSITION_L = 0x0a
    MAX_POSITION_H = 0x0b
    MAX_POSITION_L = 0x0c
    OFFSET = 0x1f
    TARGET_POSITION_H = 0x2a
    TARGET_POSITION_L = 0x2b
    SPEED_H = 0x2e
    SPEED_L = 0x2f
    LOCK = 0x30
    CURRENT_POSITION_H = 0x38
    CURRENT_POSITION_L = 0x39


class SSensor(object):
    """
    serial client
    """

    def __init__(self, port=None, baud_rate=9600):
        import serial
        if port is None:
            import serial.tools.list_ports
            serial_ports = [i[0] for i in serial.tools.list_ports.comports()]
            print(serial_ports)
            if 'USB' in serial_ports[0]:
                port = serial_ports[0]
            else:
                port = '/dev/ttyAMA2'
        self.port = serial.Serial(port=port, baudrate=baud_rate, bytesize=8, parity=serial.PARITY_NONE,
                                  stopbits=serial.STOPBITS_ONE, timeout=0.2)

    def send_cmd(self, cmd):
        self.port.write(cmd.encode('utf-8'))

    def read_cmd(self):
        response = self.port.readline()
        return response.decode('utf-8')

    def read_num(self, num):
        response = self.port.read(num)
        return response

    def send_hex(self, cmd):
        # print(cmd)
        self.port.write(cmd)
        time.sleep(0.01)
        # self.port.flushInput()

    def read_hex(self, n=0):
        if(n > 0):
            response = self.port.read(n)
        else:
            response = self.port.readline()
        array = []
        for i in response:
            array.append(i)
        time.sleep(0.1)
        return array

    def get_temperature(self,id):
        cmd = [id, 0x03, 0x00, 0x013, 0x00, 0x01]
        cmd.extend(crc16_cal(cmd))
        self.send_hex(cmd)
        res = self.read_hex(7)
        print(res)
        if len(res) == 7:
            return res[3] << 8 | res[4]
        else:
            return None

    def get_humidity(self,id):
        cmd = [id, 0x03, 0x00, 0x012, 0x00, 0x01]
        cmd.extend(crc16_cal(cmd))
        self.send_hex(cmd)
        res = self.read_hex(7)
        print(res)
        if len(res) == 7:
            return (res[3] << 8 | res[4])/10.0
        else:
            return None

    def get_both(self,id):
        cmd = [id, 0x03, 0x00, 0x012, 0x00, 0x02]
        cmd.extend(crc16_cal(cmd))
        self.send_hex(cmd)
        res = self.read_hex(9)
        print(res)
        if len(res) == 9:
            return [res[3] << 8 | res[4],res[5] << 8 | res[6]]
        else:
            return None

if __name__ == '__main__':
    import serial.tools.list_ports
    serial_ports = [i[0] for i in serial.tools.list_ports.comports()]
    print(serial_ports)
    # /dev/ttyAMA2 对应485-1
    sensor = SSensor('/dev/ttyUSB1')

    print(sensor.get_both(1))
    # print(sensor.get_humidity(1))
    # time.sleep(1)
    # print(sensor.get_temperature(1))
