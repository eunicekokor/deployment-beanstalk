from flask import render_template, redirect, request, jsonify, json, url_for, session
from client import create_app
import requests
import os
import boto.sqs
from boto.sqs.message import Message

application = create_app()

ACCOUNTS_URL="https://i9p6a7vjqf.execute-api.us-west-2.amazonaws.com/prod/apps/accounts/"
# ACCOUNTS_URL="https://i9p6a7vjqf.execute-api.us-west-2.amazonaws.com/prod/apps/accounts/test@test.com"

CATALOGUE_URL="https://i9p6a7vjqf.execute-api.us-west-2.amazonaws.com/prod/apps/catalog"
stripe_keys = {
  'secret_key': os.environ['SECRET_KEY'],
  'publishable_key': os.environ['PUBLISHABLE_KEY']
}

# Get the service resource
# sqs = boto3.resource('sqs', region_name='us-west-2')
# Get the queue
print "LISTING QUEUES"
# conn = boto.sqs.connect_to_region("us-west-2",aws_access_key_id='AKIAJZVZLE5Z427RCPLQ',aws_secret_access_key='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')
# # for queue in sqs.queues.all():
# #     print(queue.url)
# # queue = sqs.get_queue_by_name(QueueName='StripeMugsQueue')

# # for queue in conn.get_all_queues():
# #   print(queue.url)
# global queue
# queue = conn.get_queue('StripeMugsQueue')
# while(1):
#   queue()

# def queue():
#   # Process messages by printing out body and optional author name
#   for message in queue.receive_messages(MessageAttributeNames=['Author']):
#     # Get the custom author message attribute if it was set
#     author_text = ''
#     if message.message_attributes is not None:
#         author_name = message.message_attributes.get('Author').get('StringValue')
#         if author_name:
#             author_text = ' ({0})'.format(author_name)

#     # Print out the body and author (if set)
#     print('Hello, {0}!{1}'.format(message.body, author_text))

#     # Let the queue know that the message is processed
#     message.delete()

# stripe.api_key = stripe_keys['secret_key']
@application.route('/', methods=['GET'])
def landing():
  return render_template('index.html')


@application.route('/login', methods=['POST'])
def login():
  LOGIN_URL = 'https://i9p6a7vjqf.execute-api.us-west-2.amazonaws.com/prod/apps/customers/'
  params = {
  	'username': request.form.get('username'),
  	'password': request.form.get('password')
  }
  r = requests.get(LOGIN_URL, params=params)
  conn = boto.sqs.connect_to_region("us-west-2",aws_access_key_id='AKIAJZVZLE5Z427RCPLQ',aws_secret_access_key='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')
  # for queue in sqs.queues.all():
  #     print(queue.url)
  # queue = sqs.get_queue_by_name(QueueName='StripeMugsQueue')

  # for queue in conn.get_all_queues():
  #   print(queue.url)
  q = conn.create_queue('myqueue')
  # Create a new message
  # response = queue.send_message(MessageBody='login detected')
  m = Message()
  m.set_body('login detected.')
  q.write(m)

  print(r.url)
  print(r.json())
  if r.json() and 'body' in r.json() and 'Item' in r.json()['body']:
    # Success
    session['jwt'] = r.json()['headers']['authorizationToken']
    print session['jwt']
    email = "test@test.com"
    items = getStoreItems()
    return redirect(url_for('store'))
  else:
  	# Fail
  	return redirect(url_for('landing'))


@application.route('/join', methods=['POST'])
def join():
  SIGNUP_URL = 'https://i9p6a7vjqf.execute-api.us-west-2.amazonaws.com/prod/apps/customers/'
  params = {
  	'username': request.form.get('username'),
  	'password': request.form.get('password')
  }
  print params
  r = requests.post(SIGNUP_URL, params=params)
  print(r.url)
  print(r.json())
  return redirect(url_for('landing'))


@application.route('/charge', methods=['GET'])
def getCharge():
  # print "RECEIVED CHARGE!"
  amount = int(request.args.get('amount'))
  return render_template("charges.html", amount=amount)

@application.route('/transactions', methods=["GET"])
def getTransactions():
    ACCOUNTS_URL="https://i9p6a7vjqf.execute-api.us-west-2.amazonaws.com/prod/apps/payments/"

    account_email = request.args.get('email')
    transactions_list = requests.get(ACCOUNTS_URL).json()
    # print transactions_list
    transactions = []

    #only the transactions for this user
    for t in transactions_list:
      if t["email"] == account_email:
        transactions.append(t)

    return render_template("transactions.html", transactions=transactions)

  # link to user's tranactions / email / name
@application.route('/storeItem', methods=['GET'])
def store():
  print "store GETALL"
  headers = {'authorizationtoken': session.get('jwt')}
  print headers
  response = requests.get(CATALOGUE_URL, headers=headers)
  print "RESPONSE\n"
  print response
  print "JSON RESPONSE\n"
  print response.json()

  if response.status_code == 401:
    return '401 Unauthorized'


  # The email shouldd be from the user info that is logged in
  email = "test@test.com"

  # items_dict = jsonify(json.loads(response.text))
  items_dict = response.json()
  # items_dict = {}
  # items_dict['price'] = str(response['price']).encode('utf-8')
  # items_dict['itemName'] = str(response['itemName'])
  # items_dict['imgUrl'] = str(response['imgUrl'])
  # items_dict['description'] = str(response['description'])
  # items_dict['id'] = str(response['id'])

  # print items_dict
  # print "STRIPE KEYS {}".format(stripe_keys)

  return render_template('store.html', storeItems=items_dict, key=stripe_keys['publishable_key'], email=email)

def getStoreItems():
  print "store GETALL"
  headers = {'authorizationtoken': session.get('jwt')}
  print headers
  response = requests.get(CATALOGUE_URL, headers=headers)
  print "RESPONSE\n"
  print response
  print "JSON RESPONSE\n"
  print response.json()

  if response.status_code == 401:
    return '401 Unauthorized'


  # The email shouldd be from the user info that is logged in
  email = "test@test.com"

  # items_dict = jsonify(json.loads(response.text))
  items_dict = response.json()
  return items_dict
  # return redirect("https://i9p6a7vjqf.execute-api.us-west-2.amazonaws.com/prod/apps/catalog/2")

# @app.route('/accounts', methods=['GET'])
# def getAccounts():
#   request = requests.get(ACCOUNTS_URL)
#   print json.dumps(request.json)
#   items_dict = json.dumps(request.json)
#   # return render_template()
#   return render_template('store.html', storeItems=items_dict['Items'], key=stripe_keys['publishable_key'])


# customer
# https://i9p6a7vjqf.execute-api.us-west-2.amazonaws.com/prod/apps/customers/{id}

# payment
# https://i9p6a7vjqf.execute-api.us-west-2.amazonaws.com/prod/apps/payments/{id}

# @app.route('/charge', methods=['POST'])
# def charge():

#     amount = int(request.form['amount'])
#     count = int(db.Table('Transactions').scan()['Count'])

#     customer = stripe.Customer.create(
#         email=request.form['stripeEmail'],
#         source=request.form['stripeToken']
#     )

#     charge = stripe.Charge.create(
#         customer=customer.id,
#         amount=amount*100,
#         currency='usd',
#         description='Flask Charge',
#         metadata={'order_id': count+1}
#     )

#     i = datetime.now()
#     response = db.Table('Transactions').put_item(
#      Item={
#           'trans_id': count + 1,
#           'customer': customer.id,
#           'email': request.form['stripeEmail'],
#           'amount': amount,
#           'date': i.strftime('%Y/%m/%d %H:%M:%S'),
#           'item_id': request.form['item_id']
#       }
#   )

#     return render_template('charges.html', amount=amount)



if __name__ == "__main__":
    application.run(port=8080)
