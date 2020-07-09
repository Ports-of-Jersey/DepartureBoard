from templates import *
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import json

BST = True

class TableGenerator():
    def __init__(self, template, source, elements, output):
        self.template = template
        self.source = source
        self.element = elements
        self.output = output

    def read_file(self):
        file = open(self.source, 'r')
        self.content = file.read()

    def fetch_records(self):
        soup = BeautifulSoup(self.content, 'lxml')
        self.records = soup.find_all(elements['parent'])

    def parse_records(self):

        def status_times(timemessage, operationqualifier, timetype):
            try:
                row[timemessage] = record.find('operationtime', operationqualifier=operationqualifier, timetype=timetype).get_text()
            
                date_time_str = row[timemessage]
                if BST:
                    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(hours = 1)
                else:
                    date_time_obj = datetime.strptime(date_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
                
                row[timemessage] = date_time_obj.strftime('%H:%M')

            except AttributeError:
                row[timemessage] = " "

        def time_delta(operationtime):
            timenow = datetime.now()
            if BST:
                timestd = datetime.strptime(operationtime, '%Y-%m-%dT%H:%M:%S.%fZ') + timedelta(hours = 1)
            else:
                timestd = datetime.strptime(operationtime, '%Y-%m-%dT%H:%M:%S.%fZ')

            if timestd > timenow:
                delta = timestd - timenow
                row['timedelta'] = (delta.seconds / 60) // 1
            else:
                delta = timenow - timestd
                row['timedelta'] = -(delta.seconds / 60) // 1

        def gate_times(scheduledtime):
            date_time_str = row['scheduledtime']

            try:
                gatetime = gatetimeslookup[row['airline']] / 60
            except KeyError:
                gatetime = 0.5

            try:
                date_time_obj = datetime.strptime(date_time_str, '%H:%M')
                date_time_obj = date_time_obj + timedelta(hours = -gatetime)
                row['gatetime'] = date_time_obj.strftime('%H:%M')
            except ValueError:
                pass

        def lookup_airport(airportlookup):
            arrivalairport = row['arrivalairport']
            row['arrivalairport'] = airportlookup[arrivalairport]

        def lookup_status(statuslookup):
            try:
                remarkfreetext = row['remarkfreetext']
                try:
                    additionalfield = statuslookup[remarkfreetext][2]
                    row['remarkfreetext'] = statuslookup[remarkfreetext][0] + " " + row[additionalfield]
                    row['statuscolor'] = statuslookup[remarkfreetext][1]
                except IndexError:
                    row['remarkfreetext'] = statuslookup[remarkfreetext][0]
                    row['statuscolor'] = statuslookup[remarkfreetext][1]
                    print("[",datetime.now(),"] -",row['airline'],row['flightnumber'],"- No additional field specified")
            except KeyError:
                if row['airline'] == 'EZY':
                    row['remarkfreetext'] = "Info on EasyJet App"
                    print("[",datetime.now(),"] -",row['airline'],row['flightnumber'],"- No value found for remarkfreetext")
        
            if row['remarkfreetext'] == 'Go to Gate  ' and row['passengergate'] == " ":
                row['remarkfreetext'] = 'Gate Info Shortly'
            else:
                pass

    # parse_records    
        self.context = {'table': []}
        flightcount = 0

        for record in self.records:
            row = {}
            for key in elements['child']:
                try:
                    row[key] = record.find(key).get_text()
                except AttributeError:
                    row[key] = " "
                    print("[",datetime.now(),"] -",row['airline'],row['flightnumber'],"- No value found for",key)

            status_times('airbornetime', 'TKO', 'ACT')
            status_times('estimatedtime', 'OFB', 'EST')
            status_times('scheduledtime', 'OFB', 'SCT')

            gate_times('scheduledtime')
            time_delta(row['operationtime'])

            # Rules for which flights are displayed
            displayrules = [
                row['departureairport'] == 'JER',
                row['origindate'] == effectivedate,
                360 > row['timedelta'] > -90
                ]

            if all(displayrules):
                self.context['table'].append(row)
                flightcount += 1
            else:
                pass

            lookup_airport(airportlookup)
            lookup_status(statuslookup)
            
        print("[",datetime.now(),"] -",flightcount,"valid flight(s) to display")


    def render(self):
        self.rendered = get_template("index.html").render(self.context)

    def write(self):
        file = open(output, "w")
        file.write(self.rendered)
        file.close


source = 'flightinfo.xml'
output = 'output/index.html'
template = 'index.html'
parent = 'flightleg'
child = ['airline', 'flightnumber', 'departureairport', 'arrivalairport', 'origindate', 'operationtime', 'remarkfreetext', 'passengergate']
elements = {'parent': parent, 'child': child }

# configs = ['airportlookup', 'statuslookup', 'gatetimeslookup']
airportlookup = 'airportlookup.json'
statuslookup = 'statuslookup.json'
gatetimeslookup = 'gatetimeslookup.json'

effectivedate = datetime.strftime(datetime.now(), '%Y-%m-%d')


# load json lookup files
""" for config in configs:
    configfile = config + '.json'
    with open(configfile, "r") as read_file:
        config = json.load(read_file) """

with open(airportlookup, "r") as read_file:
    airportlookup = json.load(read_file)

with open(statuslookup, "r") as read_file:
    statuslookup = json.load(read_file)

with open(gatetimeslookup, "r") as read_file:
    gatetimeslookup = json.load(read_file)


generator = TableGenerator(template, source, elements, output)

# xml read/parse
generator.read_file()
generator.fetch_records()
generator.parse_records()

# html template parse/write
generator.render()
generator.write()