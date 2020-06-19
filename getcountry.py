import requests

def country_search1(region):
    result = requests.get('http://countryapi.gear.host/v1/Country/getCountries?pRegion={}'.format(region))
    data = result.json()
    return data['Response']


def country_search2(subregion):
    result = requests.get('http://countryapi.gear.host/v1/Country/getCountries?pSubRegion={}'.format(subregion))
    data = result.json()
    return data['Response']


def country_search3(country):
    result = requests.get('http://countryapi.gear.host/v1/Country/getCountries?pName={}'.format(country))
    data = result.json()
    return data['Response']


def airports(country):
    url = 'https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/autosuggest/v1.0/UK/GBP/en-GB/'
    querystring = {'query': country}
    headers = {
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        'x-rapidapi-key': "8b94c2dff2msh2b9bba43f59172ep13d124jsnd749853da445"
    }
    response = requests.request('GET', url, headers=headers, params=querystring)
    responses = response.json()
    return responses


def flight_prices(airport, date1, date2):
    url = 'https://skyscanner-skyscanner-flight-search-v1.p.rapidapi.com/apiservices/browsequotes/v1.0/UK/GBP/en-GB/LHR-sky/{}/{}'.format(
        airport, date1)
    querystring = {'inboundpartialdate': date2}
    headers = {
        'x-rapidapi-host': "skyscanner-skyscanner-flight-search-v1.p.rapidapi.com",
        'x-rapidapi-key': "8b94c2dff2msh2b9bba43f59172ep13d124jsnd749853da445"
    }
    response = requests.request("GET", url, headers=headers, params=querystring)
    responses = response.json()
    return responses


def run():
    with open('travelpack.txt', 'w+') as text_file:
        text_file.write('TRAVEL PACK')
    region = input('Which continent would you like to travel to? ')
    results = country_search1(region)
    subregions = [0] * len(results)
    count = 0
    for result in results:
        subregion = result['SubRegion']
        subregions[count] = subregion
        count = count + 1
    subregions = list(dict.fromkeys(subregions))
    for result in subregions:
        print(result)
    next = input('Now choose a subregion from this list. ')
    results1 = country_search2(next)
    for result in results1:
        name = result['Name']
        print(name)
    next2 = input('Narrow this down to a country to find out all about your destination! ')
    results2 = country_search3(next2)
    count = 0
    for result in results2:
        if count == 0:
            name = result['Name']
            lat = result['Latitude']
            long = result['Longitude']
            currency = result['CurrencyName']
            # code = result['Alpha2Code']
            print('Your chosen country is {}. '.format(name))
            print('You might need to change some currency. Over in {}, they use {}. '.format(name, currency))
            print('If you\'re navigating there yourself, the co-ordinates you\'ll need are: \nLatitude: {} \nLongitude: {}'.format(
                lat,
                long))
            count = count + 1
    location = '\nCountry: {} \nRegion: {} \nContinent: {} \nCurrency: {} '.format(next2, next, region, currency)
    with open('travelpack.txt', 'a') as text_file:
        text_file.write(location)
    lastly = input('Otherwise, we\'ll need to fly. Want me to check out flight prices? (yes/no) ')
    if lastly == 'no':
        print('Fair enough - Have a good trip! Check out the document travel pack for some information.')
        return
    else:
        results3 = airports(name)
        places = results3['Places']

        codes = [0] * len(places)
        airportnames = [0] * len(places)
        count = 0
        for place in places:
            if place['CountryName'] == name:
                city = place['PlaceName']
                codes[count] = place['PlaceId']
                airportnames[count] = city
                if city != name:
                    count = count + 1
                    print(city)
    airport = int(input(
        'Here are some airports you might want to fly into. Pick one by choosing a number from 1 to {}: '.format(
            count)))
    airport1 = airportnames[airport - 1]
    code = codes[airport - 1]
    destination = '\nDeparture Airport: London Heathrow \nDestination: {}'.format(airport1)
    with open('travelpack.txt', 'a') as text_file:
        text_file.write(destination)
    outbound = input(
        'When should we fly out to {}? Choose a date in yyyy-mm-dd format (or just yyyy-mm). '.format(airport1))
    inbound = input('And when would you like to return? ')
    results4 = flight_prices(code, outbound, inbound)
    quotes = results4['Quotes']
    prices = [0] * len(quotes)
    count = 0
    for quote in quotes:
        if count == 0:
            price = quote['MinPrice']
            if quote['Direct']:
                direct = 'Yes'
            else:
                direct = 'No'
            prices[count] = price
            outcarrierid = quote['OutboundLeg']['CarrierIds']
            outcarrierid = outcarrierid[0]
        #incarrierid = quote['InboundLeg']
            count = count + 1
    carriers = results4['Carriers']
    for carrier in carriers:
        if outcarrierid == carrier['CarrierId']:
            outcarrier = carrier['Name']
        #if incarrierid == carrier['CarrierId']:
         #   incarrier = carrier['Name']
    if any(t > 0 for t in prices):
        minprice = min([x for x in prices if x!=0])
        print('Wow! Looks like you can get from London Heathrow to {} for just £{}! '.format(airport1, minprice))
        print('Check out the document called Travel Pack. I\'ve put some info '
              'in there for you, including details of the cheapest flight.')
        outbounddetails = '\nOutbound: {}  \nInbound: {} \nCarrier: {} \nDirect? {} \nPrice: £{}'.format(outbound, inbound, outcarrier,direct, minprice)
        with open('travelpack.txt', 'a') as text_file:
            text_file.write(outbounddetails)
    else:
        print('Looks like there are no flights to this airport for those dates. ')


run()
