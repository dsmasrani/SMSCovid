import COVID19Py

def main():
    covid19 = COVID19Py.COVID19(data_source="jhu")
    location = covid19.getLocationByCountryCode("US")
    print(location[0])
    print('location: ' + location[0]['country'] + '\n' + 'country population: ' + "{:,}".format(
    location[0]['country_population']) + '\n' 'confirmed: ' + "{:,}".format(
    location[0]['latest']['confirmed']) + '\n' + 'deaths: ' + "{:,}".format(
    location[0]['latest']['deaths']) + '\n' + 'recovered: ' + "{:,}".format(location[0]['latest']['recovered']))
    print(location[0]['latest'])
    print(location[0]['province'])
    location = covid19.getLatest()
    print(location)
if __name__ == '__main__':
    main()
