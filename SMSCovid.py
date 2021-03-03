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
    responded = False
    if 'covid' in incoming_msg:
        text = 'Welcome to the COVID-19 INFORMATION BOT'
        location = covid19.getLocationByCountryCode("US")
        print(location)
        msg.body(text)
        responded = True
    if not responded:
        msg.body("invalid command, please try again")
        responded = True
    return str(resp)