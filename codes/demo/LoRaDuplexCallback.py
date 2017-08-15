import time
from config import NODE_NAME, millisecond

msgCount = 0            # count of outgoing messages
localAddress = 0xBB     # address of this device
broadcastAddress = 0xFF # destination to send to
lastSendTime = 0        # last send time
interval = 2000         # interval between sends
 

def duplexCallback(lora): 
    
    print("LoRa Duplex with callback")
    # lora.setSpreadingFactor(8)           # ranges from 6-12,default 7 see API docs

    # register the receive callback
    lora.onReceive(on_receive) 
    lora.receive()  # go into receive mode
    do_loop(lora)  
  

def do_loop(lora):    
    
    lastSendTime = millisecond()
    interval = (lastSendTime % 2000) + 1000
    global msgCount

    while True:
        if (millisecond() - lastSendTime > interval):
            message = "HeLoRa World! - from {} {}".format(NODE_NAME, msgCount)
            sendMessage(lora, message)
            print("Sending message:\n{}\n".format(message))
            lastSendTime = millisecond()          # timestamp the message
            interval = (lastSendTime % 2000) + 1000    # 2-3 seconds
            msgCount += 1 

            lora.receive()  # go back into receive mode
    

def sendMessage(lora, outgoing, destination = broadcastAddress):
    global msgCount
    
    lora.beginPacket()                   # start packet
    
    # meta = bytearray()         
    # meta.append(destination)              # add destination address
    # meta.append(localAddress)             # add sender address
    # meta.append(msgCount)                 # add message ID
    # meta.append(len(outgoing))            # add payload length
    # lora.write(meta)
    lora.print(outgoing)                 # add payload
    
    lora.endPacket()                     # finish packet and send it

    
def on_receive(lora, packetSize):
    if packetSize == 0: 
        return False       # if there's no packet, return
        
    lora.controller.blink_led()
    
    # read packet header bytes:
    # recipient = lora.read()         # recipient address
    # sender = lora.read()            # sender address
    # incomingMsgId = lora.read()     # incoming msg ID
    # incomingLength = lora.read()    # incoming msg length

    payload = lora.read_payload()
            
    try:
        print("*** Received message ***\n{}".format(payload.decode()))
    except Exception as e:
        print(e)
    print("with RSSI {}\n".format(lora.packetRssi()))

    # if len(payload) != incomingLength :   # check length for error
        # print(len(payload), incomingLength)
        # print("Error: message length does not match length")
        
    # # if the recipient isn't this device or broadcast,
    # elif recipient != localAddress and recipient != broadcastAddress :
        # print("This message is not for me or broadcasted.")
    
    # else:
        # # if message is for this device, or broadcast, print details:
        # print("*** Received message ***\nReceived from: 0x{0:0x}".format(sender))
        # print("Sent to: 0x{0:0x}".format(recipient))
        # print("Message ID: {}".format(incomingMsgId))
        # print("Message length: {}".format(incomingLength))
        # print("Message: {}".format(payload.decode()))
        # print("RSSI: {}".format(lora.packetRssi()))
        # print("Snr: {}\n".format(lora.packetSnr()))
        
        # return True