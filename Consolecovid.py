import COVID19Py

def SMSCovid():
    print('Welcome to the COVIDSMS Number System. Please enter the respective country(or global for all) you would like to receive data for:')
    for i in range(5000):
        input1 = input()
        input1 = input1.lower()
        covid19 = COVID19Py.COVID19(data_source="jhu")
        body = 'Invalid command, Please try again or type HELP for list of commands'
        if 'global' in input1:
            location = covid19.getLatest()
            body = 'location: ' + 'global' + '\n' + 'confirmed: ' + "{:,}".format(
                location['confirmed']) + '\n' + 'deaths: ' + "{:,}".format(
                location['deaths']) + '\n' + 'recovered: ' + "{:,}".format(location['recovered'])
        elif 'help' in input1:
            body = "Availible Commands: " + '\n' + "global" + '\n' + "country rank - <confirmed,deaths>" + '\n' + "2 Digit Country Name <IN,US,GB,...>" + '\n' + "<County>,US - <default - 1,county index, all>"
        elif 'country rank - confirmed' in input1:
            location = covid19.getLocations(rank_by='confirmed')
            countryarr = []
            for i in range(10):
                countryarr.append(location[i])
            body = 'Top Countries Leading by Confirmed Cases:' + '\n'
            for j in range(10):
                body += countryarr[j]['country'] + ' ' + countryarr[j]['country_code'] + '\n'
        elif 'country rank - deaths' in input1:
            location = covid19.getLocations(rank_by='deaths')
            countryarr = []
            for i in range(10):
                countryarr.append(location[i])
            body = 'Top Countries Leading by Deaths:' + '\n'
            for j in range(10):
                body += countryarr[j]['country'] + ' ' + countryarr[j]['country_code'] + '\n'
        elif 'us' in input1:
            if ',' in input1:
                county = input1.split(', ')
                newcounty = county[0].replace(' county','')
                covid191 = COVID19Py.COVID19(data_source="csbs")
                location = covid191.getLocations()
                indexcounty = []
                indexanswer = []
                #print(county)
                #print(newcounty)
                for index in range(3006):
                    #print("Current county: " + location[index]['county'] + "County inputted: " + newcounty)
                    if(location[index]['county'].lower() == newcounty):
                        #print("found it")
                        #print(index)
                        indexcounty.append(index)
                number = [int(i) for i in input1.split() if i.isdigit()]
                if(len(indexcounty) == 0):
                    body = 'Invalid County name, please try again'
                else:
                    for index in indexcounty:
                        print(location[index])
                        indexanswer.append('Location: ' + location[index]['county'] + ' County, ' + location[index]['province'] + '\n' + 'Confirmed: ' + "{:,}".format(
                            location[index]['latest']['confirmed']) + '\n' + 'Deaths: ' + "{:,}".format(
                            location[index]['latest']['deaths']) + '\n' + 'recovered: ' + "{:,}".format(
                            location[index]['latest']['recovered']) + '\n')
                    if 'all' in input1:
                        for index in range(len(indexanswer)):
                            if(index == 0):
                                body = indexanswer[0]
                            else:
                                body += indexanswer[index]
                    elif len(number) == 1:
                        if(len(number) < len(indexcounty)):
                            body = indexanswer[number[0]]
                        else:
                            body = 'Index out of range: Please try again'
                    elif len(number) == 0:
                            body = indexanswer[0]
                    else:
                      body = 'Invalid format: Please try again'
            else:
                try:
                    location = covid19.getLocationByCountryCode(input1, timelines=True)
                    print(location[0])
                    body = 'location: ' + location[0]['country'] + '\n' + 'country population: ' + "{:,}".format(location[0]['country_population']) + '\n' 'confirmed: ' + "{:,}".format(location[0]['latest']['confirmed']) + '\n' + 'deaths: ' + "{:,}".format(location[0]['latest']['deaths']) + '\n' + 'recovered: ' + "{:,}".format(location[0]['latest']['recovered'])
                except:
                    body = 'Invalid command format: Please try again'
        elif(len(input1) == 2):
            try:
                location = covid19.getLocationByCountryCode(input1, timelines=True)
                print(location[0])
                body = 'location: ' + location[0]['country'] + '\n' + 'country population: ' + "{:,}".format(location[0]['country_population']) + '\n' 'confirmed: ' + "{:,}".format(location[0]['latest']['confirmed']) + '\n' + 'deaths: ' + "{:,}".format(location[0]['latest']['deaths']) + '\n' + 'recovered: ' + "{:,}".format(location[0]['latest']['recovered'])
            except:
                body = 'Invalid country name: Please try again'
        print(body)
if __name__ == '__main__':
    SMSCovid()

