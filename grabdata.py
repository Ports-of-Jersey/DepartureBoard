import os
from zeep.plugins import HistoryPlugin
from zeep import Client
from lxml import etree
from datetime import datetime

wsdl_url = 'https://podbwebservice.ports.je/AIDXQueryFlights/Services/RequestFlightService.svc?wsdl'
service = 'RequestFlightService'
port = 'BasicHttpsBinding_IRequestFlightService'
userID = 'POJWebInternal456'

history = HistoryPlugin()

client = Client(wsdl_url, plugins=[history])

service2 = client.bind(service, port)

service2.flightRequest(userID = userID, fullRefresh = True)
flight_xml = etree.tostring(history.last_received["envelope"], encoding="unicode", pretty_print=True)

if "Success" in flight_xml:
    f = open("flightinfo.xml", "w")
    f.write(flight_xml)
    f.close()

    print("[",datetime.now(),"] -",os.path.getsize('flightinfo.xml'),"Bytes pulled from AIDX")
else:
    print("[",datetime.now(),"] - WARNING! Unable to access AIDX")
    print(flight_xml)