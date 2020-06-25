from bs4 import BeautifulSoup
from datetime import datetime, timedelta

BST = True

source = 'flightinfo.xml'

parent = 'flightleg'
child = ['airline', 'flightnumber', 'callsign', 'arrivalairport', 'remarkfreetext', 'passengergate']
elements = {'parent': parent, 'child': child }


file = open(source, 'r')
content = file.read()

soup = BeautifulSoup(content, 'lxml')
records = soup.find_all(elements['parent'])

# print(soup)

def status_times(timemessage, operationqualifier, timetype):
    try:
        row[timemessage] = record.find('operationtime', operationqualifier=operationqualifier, timetype=timetype).get_text()
    
        date_time_str = row[timemessage]
        date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
        if BST == True:
            date_time_obj = date_time_obj + timedelta(hours = 1)
        else:
            date_time_obj = date_time_obj
        
        row[timemessage] = date_time_obj.strftime("%H:%M")

    except AttributeError:
        print("No value found for " + timemessage)
        row[timemessage] = " "




context = {'table': []}

for record in records:
    row = {}

    for key in elements['child']:
        try:
            row[key] = record.find(key).get_text()
        except AttributeError:
            print("No value found for " + key)
            row['key'] = " "
    
    status_times('approxtime', 'OFB', 'EST')
    status_times('airbornetime', 'TKO', 'ACT')
    status_times('scheduledtime', 'OFB', 'SCT')

    context['table'].append(row)

print(context)