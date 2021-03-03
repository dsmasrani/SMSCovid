from flask import Flask, request
import requests
import COVID19Py
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

@app.route('/bot', methods=['POST'])
def bot():
    covid19 = COVID19Py.COVID19(data_source="jhu")
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    body = '\n' + 'Invalid command, Please try again or type COVID for list of commands'
    if 'covid' in incoming_msg:
        body = '\n' + "Welcome to SMSCovid" + '\n' + "Available Commands: " + '\n' + "global" + '\n' + "country rank - <confirmed,deaths>" + '\n' + "2 Digit Country Name <IN,US,AU,...>" + '\n' + "<County>,US - <default - 1,county index, all>"
        msg.body(body)
        print(body)
        responded = True
    elif 'global' in incoming_msg:
        location = covid19.getLatest()
        body = '\n' + 'location: ' + 'global' + '\n' + 'confirmed: ' + "{:,}".format(
            location['confirmed']) + '\n' + 'deaths: ' + "{:,}".format(
            location['deaths']) + '\n' + 'recovered: ' + "{:,}".format(location['recovered'])
        msg.body(body)
        responded = True
    elif 'country rank - confirmed' in incoming_msg:
        location = covid19.getLocations(rank_by='confirmed')
        countryarr = []
        for i in range(10):
            countryarr.append(location[i])
        body = '\n' + 'Top Countries Leading by Confirmed Cases:' + '\n'
        for j in range(10):
            body += countryarr[j]['country'] + ' ' + countryarr[j]['country_code'] + '\n'
        msg.body(body)
        responded = True
    elif 'country rank - deaths' in incoming_msg:
        location = covid19.getLocations(rank_by='deaths')
        countryarr = []
        for i in range(10):
            countryarr.append(location[i])
        body = '\n' + 'Top Countries Leading by Deaths:' + '\n'
        for j in range(10):
            body += countryarr[j]['country'] + ' ' + countryarr[j]['country_code'] + '\n'
        msg.body(body)
        responded = True
    elif 'us' in incoming_msg:
        if ',' in incoming_msg:
            county = incoming_msg.split(', ')
            newcounty = county[0].replace(' county', '')
            covid191 = COVID19Py.COVID19(data_source="csbs")
            location = covid191.getLocations()
            indexcounty = []
            indexanswer = []
            # print(county)
            # print(newcounty)
            for index in range(3006):
                # print("Current county: " + location[index]['county'] + "County inputted: " + newcounty)
                if (location[index]['county'].lower() == newcounty):
                    # print("found it")
                    # print(index)
                    indexcounty.append(index)
            number = [int(i) for i in incoming_msg.split() if i.isdigit()]
            if (len(indexcounty) == 0):
                body = '\n' + 'Invalid County name, please try again'
                msg.body(body)
                responded = True
            else:
                for index in indexcounty:
                    print(location[index])
                    indexanswer.append('Location: ' + location[index]['county'] + ' County, ' + location[index][
                        'province'] + '\n' + 'Confirmed: ' + "{:,}".format(
                        location[index]['latest']['confirmed']) + '\n' + 'Deaths: ' + "{:,}".format(
                        location[index]['latest']['deaths']) + '\n' + 'recovered: ' + "{:,}".format(
                        location[index]['latest']['recovered']) + '\n')
                if 'all' in incoming_msg:
                    for index in range(len(indexanswer)):
                        if (index == 0):
                            body = '\n' + indexanswer[0]
                        else:
                            body += indexanswer[index]
                    msg.body(body)
                    responded = True
                elif len(number) == 1:
                    if (len(number) < len(indexcounty)):
                        try:
                            body = '\n' + indexanswer[number[0] - 1]
                        except:
                            body = '\n' + 'Index out of range: Please try again'
                        msg.body(body)
                        responded = True
                    else:
                        body = '\n' + 'Index out of range: Please try again'
                        msg.body(body)
                        responded = True
                elif len(number) == 0:
                    body = '\n' + indexanswer[0]
                    msg.body(body)
                    responded = True
                else:
                    body = '\n' + 'Invalid format: Please try again'
                    msg.body(body)
                    responded = True
        else:
            try:
                location = covid19.getLocationByCountryCode(incoming_msg, timelines=True)
                print(location[0])
                body = '\n' + 'location: ' + location[0]['country'] + '\n' + 'country population: ' + "{:,}".format(
                    location[0]['country_population']) + '\n' 'confirmed: ' + "{:,}".format(
                    location[0]['latest']['confirmed']) + '\n' + 'deaths: ' + "{:,}".format(
                    location[0]['latest']['deaths']) + '\n' + 'recovered: ' + "{:,}".format(
                    location[0]['latest']['recovered'])
            except:
                body = '\n' + 'Invalid command format: Please try again'
            msg.body(body)
            responded = True
    elif (len(incoming_msg) == 2):
        try:
            location = covid19.getLocationByCountryCode(incoming_msg, timelines=True)
            print(location[0])
            body = '\n' + 'location: ' + location[0]['country'] + '\n' + 'country population: ' + "{:,}".format(
                location[0]['country_population']) + '\n' 'confirmed: ' + "{:,}".format(
                location[0]['latest']['confirmed']) + '\n' + 'deaths: ' + "{:,}".format(
                location[0]['latest']['deaths']) + '\n' + 'recovered: ' + "{:,}".format(
                location[0]['latest']['recovered'])
        except:
            body = '\n' + 'Invalid country name: Please try again'
        msg.body(body)
        responded = True
    else:
        msg.body(body)
        responded = True
    return str(resp)