## Aufbau

### Pinbelegung

| Pico | MCP2515 |
| ---- | ------- |
| 26   | INT     |
| 24   | SCK     |
| 25   | SI      |
| 21   | SO      |
| 22   | CS      |
| 38   | GND     |
| 40   | VCC1    |
| 36   | VCC     |

![pin connections 1](.\images\image1.jpeg)

![pin connections 2](.\images\image2.jpeg)

![pin connections 3](.\images\image3.jpeg)

### Definition bestimmter Befehle

```python
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
```

### Definition der Methoden zur Kommunikation mit MCP2515

```python
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
```

Ausführung zur Setzung des CAN Modes 

```python
cs.value(1)

print(reg_read_status(spi, cs))

reg_set_mode(spi, cs, 'NORMAL')

print(reg_read_status(spi, cs))
```



## Fragestellungen

* Welche Übertragungsreichweiten und Geschwindigkeiten kommen beim CAN-Bus zum Einsatz?
  
    | Bitrate     | Kabellänge |
    | ----------- | ---------- |
    | 10 kbits/s  | 6,7 km     |
    | 20 kbits/s  | 3,3 km     |
    | 50 kbits/s  | 1,3 km     |
    | 125 kbits/s | 530 m      |
    | 250 kbits/s | 270 m      |
    | 500 kbits/s | 130 m      |
    | 1 Mbits/s   | 40 m       |
    
* Wieviele Teilnehmer können dabei miteinander kommunizieren?
    > theoretisch unendlich viele
    
* Welche Möglichkeiten des einfachen Deployments bieten sich an, wenn verschiedene Services zur Darstellung von Sensordaten miteinander agieren sollen?
    > Raspberry Pi, Pico
    
* Wie können Grenzwerte definiert werden, die zur Steuerung bzw. Notifikation herangezogen werden?
    > 

## Quellen

https://www.itwissen.info/CAN-Bus-controller-area-network-CAN.html#:~:text=Theoretisch%20ist%20die%20Teilnehmerzahl%20unbegrenzt,CAN%2DBus%20angeschlossen%20werden%20k%C3%B6nnen.

https://www.mikrocontroller.net/attachment/6819/canbus.pdf
