#!coding:utf-8
import time

addr = 0x01

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

class SGateway(object):
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
                                  stopbits=serial.STOPBITS_ONE, timeout=0.1)

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

    def get_numbers(self):
        cmd = [addr, 0x02, 0x01, 0x00]
        cmd.extend(crc16_cal(cmd))
        self.send_hex(cmd)
        res = self.read_hex(6)
        print(res)
        if len(res) == 6:
            return res[3]
        else:
            return None

    def send_raw_hex(self,str):
        cmd = [int(i,16) for i in str.split(' ')]
        # cmd.extend(crc16_cal(cmd))
        self.send_hex(cmd)
        res = self.read_hex()
        print(res)

    def get_climate_state(self,id):
        cmd = [addr, 0x02, 0x02, id]
        cmd.extend(crc16_cal(cmd))
        self.send_hex(cmd)
        res = self.read_hex(10)
        print(res)
        if len(res) == 10:
            return res[4:8]
        else:
            return None

    def set_climate_state(self,id,power,mode,temperature,fan_speed):
        cmd = [addr, 0x06, 0x02, id,power,mode,temperature,fan_speed]
        cmd.extend(crc16_cal(cmd))
        self.send_hex(cmd)
        res = self.read_hex(6)
        print(res)
        if len(res) == 6:
            return res[3] == 1
        else:
            return None

if __name__ == '__main__':
    import serial.tools.list_ports
    serial_ports = [i[0] for i in serial.tools.list_ports.comports()]
    print(serial_ports)
    # /dev/ttyAMA2 对应485-1
    gateway = SGateway('/dev/ttyAMA1')
    print(gateway.get_numbers())
    print(gateway.get_climate_state(1))
    print(gateway.get_climate_state(2))
    print(gateway.get_climate_state(3))
    print(gateway.get_climate_state(4))
    print(gateway.set_climate_state(1,0,0,18,2))