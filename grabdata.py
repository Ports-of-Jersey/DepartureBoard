from zeep.plugins import HistoryPlugin
from zeep import Client
from lxml import etree

wsdl_url = 'https://podbwebservice.ports.je:8443/AIDXQueryFlights/Services/RequestFlightService.svc?wsdl'
service = 'RequestFlightService'
port = 'BasicHttpsBinding_IRequestFlightService'
userID = 'POJWebInternalTest456'

history = HistoryPlugin()

client = Client(wsdl_url, plugins=[history])

service2 = client.bind(service, port)

service2.flightRequest(userID = userID, fullRefresh = True)
flight_xml = etree.tostring(history.last_received["envelope"], encoding="unicode", pretty_print=True)

print(flight_xml)

f = open("flightinfo.xml", "w")
f.write(flight_xml)
f.close()