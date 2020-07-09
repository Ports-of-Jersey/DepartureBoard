import os
import time
from datetime import datetime

while True:
    os.system('python grabdata.py')

    os.system('python generate.py')

    print("[",datetime.now(),"] - Sleep 15 seconds")
    time.sleep(15)