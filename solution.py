import csv
from math import sin, cos, sqrt, atan2, radians


class Route():
	def __init__(self, start, cost= 0):
		self.cost= cost
		self.visited= start

class PriorityQueue:
	def __init__(self):
		self.queue = []
		self.length= 0

	def isEmpty(self):
		return self.length == 0

	def insert(self, data):
		i= 0
		while(i < self.length):
			if self.queue[i].cost > data.cost:
				break
			i+= 1
		self.queue.insert(i, data)
		self.length+= 1

	def pop(self):
		if(self.length > 0):
			item= self.queue[0]
			self.queue= self.queue[1:]
			self.length-= 1
			return item

################################################################

# databases

class Aircraft:
	def __init__(self, Code, Type, Units, Manufacturer, Range):
		self.code= Code 
		self.type= Type
		self.units= Units
		self.manufacturer= Manufacturer
		self.range= Range

class Airport:
	def __init__(self, AirportId, AirportName, CityName, Country, IATA, ICAO, Latitude, Longitude, Altitude, TimeZone, DST, Continent):
		self.AirportId= AirportId
		self.AirportName= AirportName
		self.CityName= CityName
		self.Country= Country # use this as key for currencies
		self.IATA= IATA # key
		self.ICAO= ICAO
		self.Latitude= Latitude
		self.Longitude= Longitude
		self.Altitude= Altitude
		self.TimeZone= TimeZone
		self.DST= DST
		self.Continent= Continent

class Currency:
	def __init__(self, currency, currencyCode, toEuro, fromEuro):
		self.currency= currency
		self.currencyCode= currencyCode # key Code to get from currencies
		self.toEuro= toEuro
		self.fromEuro= fromEuro

class CountryCurrency:
	def __init__(self, name,name_fr,ISO3166_1_Alpha_2,ISO3166_1_Alpha_3,ISO3166_1_numeric,ITU,MARC,WMO,DS,Dial,FIFA,FIPS,GAUL,IOC,currency_alphabetic_code,currency_country_name,currency_minor_unit,currency_name,currency_numeric_code,is_independent):
		self.name= name # key
		self.name_fr= name_fr
		self.ISO3166_1_Alpha_2= ISO3166_1_Alpha_2
		self.ISO3166_1_Alpha_3= ISO3166_1_Alpha_3
		self.ISO3166_1_numeric= ISO3166_1_numeric
		self.ITU= ITU
		self.MARC= MARC
		self.WMO= WMO
		self.DS= DS
		self.Dial= Dial
		self.FIFA= FIFA
		self.FIPS= FIPS
		self.GAUL= GAUL
		self.IOC= IOC
		self.currency_alphabetic_code= currency_alphabetic_code # the key for currency
		self.currency_country_name= currency_country_name
		self.currency_minor_unit= currency_minor_unit
		self.currency_name= currency_name
		self.currency_numeric_code= currency_numeric_code
		self.is_independent= is_independent

#################################################################

#reading functions

def read_airports(filename):
	database= {}
	with open(filename) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			tmp= Airport(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11])
			database[tmp.IATA]= tmp
	return database

def read_aircrafts(filename):
	database= {}
	with open(filename) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		index= 0
		for row in csv_reader:
			if index != 0: 
				tmp= Aircraft(row[0], row[1], row[2], row[3], row[4])
				database[tmp.code]= tmp
			index+= 1
	return database

def read_currencies(filename):
	database= {}
	with open(filename) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		index= 0
		for row in csv_reader:
			if index != 0:
				tmp= Currency(row[0], row[1], row[2], row[3])
				database[tmp.currencyCode]= tmp
			index+= 1
	return database

def read_countrycurrencies(filename):
	database= {}
	with open(filename) as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		index= 0
		for row in csv_reader:
			if index != 0:
				tmp= CountryCurrency(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8], row[9], row[10], row[11], row[12], row[13], row[14], row[15], row[16], row[17], row[18], row[19])
				database[tmp.name]= tmp
			index+= 1
	return database

#################################################################

#optimization functions

def distance_cal(LatC,LongC,LatT,LongT):
    R = 6373.0
    lat1 = radians(LatC)
    lon1 = radians(LongC)
    lat2 = radians(LatT)
    lon2 = radians(LongT)
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    distance = R * c
    return distance

def cost(airportA, airportB, currencies, countrycurrencies, maxrange):
	dist= distance_cal(float(airportA.Latitude), float(airportA.Longitude), float(airportB.Latitude), float(airportB.Longitude))
	if dist > maxrange:
		return -1
	countryA= airportA.Country #United Kingdom
	currencyA= countrycurrencies[countryA].currency_alphabetic_code #GBP
	rate= currencies[currencyA].toEuro
	return dist * float(rate)

def dijikstra(airportsToVisit, maxrange, currencies, countrycurrencies, airports):
	pq= PriorityQueue()
	pq.insert(Route([airportsToVisit[0]]))
	while not pq.isEmpty():
		route_act= pq.pop()
		airport_act= route_act.visited[-1]
		if airport_act == airportsToVisit[0] and len(route_act.visited)>1:
			return route_act
		visitedEverything= True
		for airport in airportsToVisit[1:]:
			if airport not in route_act.visited:
				visitedEverything= False
				ct= cost(airports[airport_act] ,airports[airport] ,currencies, countrycurrencies, maxrange)
				if ct >0:
					pq.insert(Route(route_act.visited+[airport], route_act.cost + ct))
		if visitedEverything:
			ct= cost(airports[airport_act] ,airports[airportsToVisit[0]] ,currencies, countrycurrencies, maxrange)
			if ct >0:
				pq.insert(Route(route_act.visited+[airportsToVisit[0]], route_act.cost + ct))
	return None

def maxrange(aircraftCode, aircrafts):
	aircraft= aircrafts[aircraftCode]
	rate= 1
	if aircraft.units=="imperial":
		rate= 1.6
	return rate * float(aircraft.range)


#################################################################

def main():

	airports= read_airports("airport.csv")
	aircrafts= read_aircrafts("aircraft.csv")
	currencies= read_currencies("currencyrates.csv")
	countrycurrencies= read_countrycurrencies("countrycurrency.csv")

	with open("test.csv") as csv_file:
		csv_reader = csv.reader(csv_file, delimiter=',')
		for row in csv_reader:
			length= len(row)
			airportsToVisit= []
			for index in range(length-1):
				airportsToVisit.append(row[index])
			aircraftCode= row[-1]
			bestroute= dijikstra(airportsToVisit, maxrange(aircraftCode, aircrafts), currencies, countrycurrencies, airports)
			if(bestroute != None):
				print(bestroute.visited, bestroute.cost)
			else:
				print("The " + aircraftCode + " can't do the trip")

if __name__=="__main__":
	main()