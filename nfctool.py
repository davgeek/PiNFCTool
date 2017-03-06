import binascii
import sys

import Adafruit_PN532 as PN532

# Options supported
# 1 = Read tag
# 2 = Write tag

# Hack to make code compatible with Py2 and Py3
try:
    input = raw_input
except NameError:
    pass

# PN532 configuration pins for Pi 1
CS = 8
MOSI = 10
MISO = 9
SCLK = 11

# Card key for block data
CARD_KEY = {0xFF, 0xFF, 0xFF, 0xFF, 0xFF, 0xFF}

# Create and initialize an instance of the PN532 class
pn532 = PN532.PN532(cs=CS, sclk=SCLK, mosi=MOSI, miso=MISO)
pn532.begin()
pn532.SAM_configuration()

# Step 1, wait for card to be present
print('Pi NFC Tool')
print('Options: 1 = Read, 2 = Write')
numberOpt = input('Please select an option:')
try:
    option = int(numberOpt)
except ValueError:
    print('Error! Unreconized option')
    # check choice bounds

if option == 1:
    print('Read tag')
    print(' ')
    print('Waiting for MiFare card...')
    while True:
        # Wait for a card to be available.
        uid = pn532.read_passive_target()
        # Try again if no card found.
        if uid is None:
            continue
        # Found a card, now try to read block 4 to detect the block type.
        print('Found card with UID 0x{0}'.format(binascii.hexlify(uid)))
        # Read all blocks
        for x in range(4, 63):
            if not pn532.mifare_classic_authenticate_block(uid, x, PN532.MIFARE_CMD_AUTH_B, CARD_KEY):
                print('Failed to authenticate with card!')
                continue
            data = pn532.mifare_classic_read_block(x)
            if data is None:
                print('Failed to read data from card!')
                continue
        print('Data: ')
        print data

elif option == 2:
    print('Write tag')

else:
    sys.exit(-1)