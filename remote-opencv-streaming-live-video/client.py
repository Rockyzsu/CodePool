import cv2
import numpy as np
import socket
import sys
import pickle
import struct
from io import StringIO
import json
from tempfile import TemporaryFile
cap=cv2.VideoCapture(0)
clientsocket=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
clientsocket.connect(('localhost',7777))

while(cap.isOpened()):
  ret,frame=cap.read()
  f = TemporaryFile()
  # memfile = StringIO()
  np.save(f, frame)
  f.seek(0)
  # data = json.dumps(f.read()).decode('latin-1')

  clientsocket.sendall(struct.pack("L", len(data))+data)
  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

cap.release()