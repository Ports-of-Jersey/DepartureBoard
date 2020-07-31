import os
import time

os.chdir(os.path.dirname(os.path.abspath(__file__)))

while True:
    os.system('python grabdata.py')

    os.system('python generate.py')

    print('sleep 15 seconds')
    time.sleep(15)
