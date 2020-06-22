from zeep import Client

wsdl = 'https://podbwebservice.ports.je/AIDXQueryFlights/Services/RequestFlightService.svc?wsdl'
service = 'RequestFlightService'
port = 'BasicHttpsBinding_IRequestFlightService'
userID = 'POJInternal123'

client = Client(wsdl = wsdl)

service2 = client.bind(service, port)

#print(service2.flightRequest(userID = userID, fullRefresh = False))

data = service2.flightRequest(userID = userID, fullRefresh = False)

print(data)  