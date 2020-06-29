import os
import time
from http import server

http.server(1234)

while True:
    os.system('python grabdata.py')

    os.system('python generate.py')

    print('sleep 15 seconds')
    time.sleep(15)