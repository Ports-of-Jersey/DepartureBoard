from zeep.plugins import HistoryPlugin
from zeep import Client
from lxml import etree

wsdl_url = 'https://podbwebservice.ports.je/AIDXQueryFlights/Services/RequestFlightService.svc?wsdl'
service = 'RequestFlightService'
port = 'BasicHttpsBinding_IRequestFlightService'
userID = 'POJInternal123'

history = HistoryPlugin()

client = Client(wsdl_url, plugins=[history])

service2 = client.bind(service, port)

data = service2.flightRequest(userID = userID, fullRefresh = False)

service2.flightRequest(userID = userID, fullRefresh = False)
flight_xml = etree.tostring(history.last_received["envelope"], encoding="unicode", pretty_print=True)

f = open("flightinfo.xml", "a")
f.write(flight_xml)
f.close()