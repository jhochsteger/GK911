import machine
import utime
import ustruct
import sys

###############################################################################
# Constants

# Registers
REG_DEVID = 0x00
REG_POWER_CTL = 0x2D
REG_DATAX0 = 0x32

# Other constants
DEVID = 0xE5
INSTRUCTIONS = {
    'RESET': 0xC0,
    'READ': 0x03,
    'WRITE': 0x02,
    'READ RX': 0x90,
    'READ STATUS': 0xA0,
}
MODES = {
    'LOOPBACK': 0x02,
    'NORMAL': 0x00,
}

###############################################################################
# Settings

# Assign chip select (CS) pin (and start it high)
cs = machine.Pin(17, machine.Pin.OUT)

# Initialize SPI
spi = machine.SPI(0,
                  baudrate=125000,
                  polarity=1,
                  phase=1,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(18),
                  mosi=machine.Pin(19),
                  miso=machine.Pin(16))

###############################################################################
# Functions

def reg_write(spi, cs, address, data):
    """
    Write 1 byte to the specified register.
    """

    # Construct message (set ~W bit low, MB bit low)
    msg = bytearray()
    msg.append(INSTRUCTIONS['WRITE'])
    msg.append(address)
    msg.append(data)

    # Send out SPI message
    cs.value(0)
    spi.write(msg)
    cs.value(1)
    
def reg_reset(spi, cs):
    """
    Write 1 byte to the specified register.
    """

    # Construct message (set ~W bit low, MB bit low)
    msg = bytearray()
    msg.append(INSTRUCTIONS['RESET'])

    # Send out SPI message
    cs.value(0)
    spi.write(msg)
    cs.value(1)

def reg_set_mode(spi, cs, mode):
    """
    Write 1 byte to the specified register.
    """

    # Construct message (set ~W bit low, MB bit low)
    msg = bytearray()
    msg.append(INSTRUCTIONS['WRITE'])
    msg.append(0x0f)
    msg.append(0x07 | MODES[mode] << 5)

    # Send out SPI message
    cs.value(0)
    spi.write(msg)
    cs.value(1)

def reg_read_rx(spi, cs):
    """
    Read byte(s) from specified register. If nbytes > 1, read from consecutive
    registers.
    """

    # Construct message (set ~W bit high)
    msg = bytearray()
    msg.append(INSTRUCTIONS['READ RX'] | 0x01 << 1)

    # Send out SPI message and read
    cs.value(0)
    spi.write(msg)
    data = spi.read(8)
    cs.value(1)

    return data

def reg_read_status(spi, cs):
    """
    Read byte(s) from specified register. If nbytes > 1, read from consecutive
    registers.
    """

    # Construct message (set ~W bit high)
    msg = bytearray()
    msg.append(INSTRUCTIONS['READ STATUS'])

    # Send out SPI message and read
    cs.value(0)
    spi.write(msg)
    data = spi.read(8)
    cs.value(1)

    return data

def reg_read(spi, cs, address):
    """
    Read byte(s) from specified register. If nbytes > 1, read from consecutive
    registers.
    """

    # Construct message (set ~W bit high)
    msg = bytearray()
    msg.append(INSTRUCTIONS['READ'] | 0x01 << 1)
    msg.append(address)

    # Send out SPI message and read
    cs.value(0)
    spi.write(msg)
    data = spi.read(8)
    cs.value(1)

    return data

###############################################################################
# Main

# Start CS pin high
cs.value(1)

print(reg_read_status(spi, cs))

reg_set_mode(spi, cs, 'NORMAL')

print(reg_read_status(spi, cs))
