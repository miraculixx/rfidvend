import serial

class RFIDTag:
  '''
  Represents an RFID tag, encapsulating its data
  '''
  def __init__(self, bytes=None):
	self.bytes = bytes

  def __str__(self):
	return "".join(self.bytes)

  def get_id(self):
      return self.__str__()

class RFIDReader:
  '''
  Software equivalent of the RFID reader. Reads from USB
  and is able to return RFIDTag instances upon receiving data
  from the hardware reader.
  '''
  def __init__(self, port='/dev/ttyUSB0'):
    self.ser = serial.Serial('/dev/ttyUSB0', 9600,
                          bytesize=serial.EIGHTBITS,
                          parity=serial.PARITY_NONE,
                          stopbits=serial.STOPBITS_ONE,
                          rtscts=False)

  def read(self):
    '''
    read tag data from serial port. tag data is embedded
    between ASCII text start 0x02 and text stop 0x03 delimiters,
    and embedded CRLF 0x0a 0x0d. All of these are ignored and
    the actual data is is retrieved as a string and a RFIDTag
    instance returned
    '''
    stop = False
    tag = []
    while stop == False:
	c = self.ser.read()
	if ord(c) == 0x03:
	  stop = True
        elif ord(c) == 0x02:
          tag = []
        elif ord(c) == 0x0d or ord(c) == 0x0a:
	  pass
	else:
	  tag.append(c)
    return RFIDTag(tag)