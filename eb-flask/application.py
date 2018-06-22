from flask import Flask, session, redirect, url_for, render_template, request, jsonify, Response, flash, Blueprint, session
import json
import os
import boto3
from datetime import datetime
import json
from client import create_app
import stripe
import requests

#MUST CHANGE WHEN CLIENT APP DEPLOYED
# CLIENT_CHARGE_URL="http://eunicekokor.localhost.run/charge"
application = create_app()
application.config.from_object('config')
boto_session = boto3.session.Session(aws_access_key_id=application.config['AWS_ACCESS_KEY_ID'], aws_secret_access_key=application.config['AWS_SECRET_ACCESS_KEY'])
db = boto_session.resource('dynamodb',region_name='us-west-2')

stripe_keys = {
  'secret_key':application.config['STRIPE_SECRET_KEY'],
}

stripe.api_key = stripe_keys['secret_key']

# @application.route('/charge', methods=['GET'])
# def thanks():
@application.route('/', methods=['GET'])
def index():
  return "HelloWorld"

@application.route('/charge', methods=['POST'])
def charge():
    print "REQUEST {}".format(request.form)
    print "STRIPECONFIG {}\n\n".format(stripe.api_key)

    amount = int(request.form['amount'])
    count = int(db.Table('Transactions').scan()['Count'])
    customer = stripe.Customer.create(
        email=request.form['stripeEmail'],
        source=request.form['stripeToken']
    )

    charge = stripe.Charge.create(
        customer=customer.id,
        amount=amount*100,
        currency='usd',
        description='Flask Charge',
        metadata={'order_id': count+1}
    )

    i = datetime.now()
    print "response"
    response = db.Table('Transactions').put_item(
	   Item={
	        'trans_id': count + 1,
	        'customer': customer.id,
	        'email': request.form['stripeEmail'],
	        'amount': amount,
	        'date': i.strftime('%Y/%m/%d %H:%M:%S'),
	        'item_id': request.form['item_id']
	    }
	   )

    print "AMOUNT {}\n".format(amount)
    post_info = {'amount':amount}
    CLIENT_CHARGE_URL="http://flask-env-client.xykuphpmsf.us-west-2.elasticbeanstalk.com/charge?amount={}".format(amount)
    # we can also do return a response with all the data like here http://stackoverflow.com/questions/42098396/redirect-to-external-url-while-sending-a-json-object-or-string-from-flask-app
    return redirect(CLIENT_CHARGE_URL)
    # requests.post(CLIENT_CHARGE_URL, data=post_info)
    # return json.dumps({"amount":amount})



if __name__ == "__main__":
    application.run(port=5002)
