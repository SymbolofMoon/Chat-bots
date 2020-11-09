from flask import Flask, request
import requests
from twilio.twiml.messaging_response import MessagingResponse


app= Flask(__name__)

@app.route('/mybot', methods=['POST'])

def mybot():
    incoming_msg = request.values.get('Body','').lower()
    resp = MessagingResponse()
    msg = resp.message()
    responded = False
    if 'hi' in incoming_msg:
        msg.body("Hello, I am Chandra's Bot")
        responded = True
    if 'quote' in incoming_msg:
        r=requests.get('http://api.quotable.io/random')
        if r.status_code == 200:
                     data= r.json()
                     quote = f'{data["content"]} ({data["author"]})'
        else:
            quote= 'Sorry I am not able to retrieve quote this time'

        msg.body(quote)
        responded = True
    if 'who are you?' in incoming_msg:
        msg.body("Hi! I am Chandra's Whatsapp Chatbot")
        responded = True

    if not responded:
        msg.body("Hi!! What should I do for you?")
        responded = True


    return str(resp)


if __name__ == '__main__':
    app.run()       
 