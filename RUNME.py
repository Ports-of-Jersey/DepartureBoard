import os
import time

while True:
    os.system('python grabdata.py')

    os.system('python generate.py')

    print('sleep 15 seconds')
    time.sleep(15)