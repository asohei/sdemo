from django.shortcuts import render
import requests
import json
import base64
from django.views.decorators.csrf import csrf_protect,csrf_exempt
from django.http import HttpResponse
from django.http import JsonResponse
import os
import stripe
from django.contrib.sessions.backends.db import SessionStore
from django.contrib.sessions.models import Session
from django.shortcuts import redirect

stripe.api_key = os.environ.get('s_api_secret')
s_public_key = os.environ.get('s_public_key')
#assume loggedin buyer id is user_123 in this app
login_user = 'user_123'
user_cart = login_user + '_cart'


def checkout(request):
    context = {
    #     'client_token': get_client_token(),
    #     'client_id' : client_id
        }
    return render(request, 's/index.html', context)

@csrf_exempt
def add_to_cart(request):

    req = json.loads(request.body)

    session = request.session

    if user_cart not in session:
        session[user_cart] = []
        print("cart session added")

    current_cart = session[user_cart]

    current_cart.append(
        {
        "product_id":req['product_id'],
        "price_id":req['price_id'],
        "price":req['price'],
        "currency":req['currency'],
        "name":req['name'],
        "image":req['image']
        }
    )

    session[user_cart] = current_cart

    return HttpResponse('ok') 



@csrf_exempt
def count_cart_items(request):

    session = request.session

    if user_cart not in session:
        return JsonResponse( {"items":0 } )

    else:
        return JsonResponse( {"items":len(session[user_cart]) } )


def products(request):


    prices = stripe.Price.list(limit=4)

    products = []

    for price in prices:
            product = stripe.Product.retrieve(price.product)
            if product.active:
                try: 
                    products.append (
                        {
                        "price_id" : price.id,
                        "price" : price.unit_amount,
                        "currency" : price.currency,
                        "name": product.name,
                        "product_id" : product.id,
                        "image":product.images[0]
                        }
                    )

                except IndexError as error :
                    print(error)

    print(type(products))

    context = {
        'products': products
    }
    return render(request, 's/products.html', context)


@csrf_exempt
def remove_item(request):

    session = request.session
    
    position = json.loads(request.body)['index']

    current_cart = session[user_cart]

    current_cart.pop(position)


    session[user_cart] = current_cart


    return JsonResponse( {'message':'item removed'}) 

@csrf_exempt
def grab_cart(request):

    session = request.session
    # session.pop(user_cart)

    if user_cart not in session:

        return JsonResponse({})
    else :

        cart_items = []
        
        for index, item in enumerate(session[user_cart]):

            _item = {

                'index': index,
                'product_id' : item['product_id'],
                'price_id' : item['price_id'],
                'price': item['price'],
                'name' : item['name'],
                'image' : item['image'],
                'currency':item['currency'],
            }

            cart_items.append(_item)


        return JsonResponse( cart_items, safe=False) 


@csrf_exempt
def cart(request):


    context = {}

    return render(request, 's/cart.html', context)


@csrf_exempt
def create_checkout_session(self):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card','alipay'],
            billing_address_collection='required',
            shipping_address_collection={
            'allowed_countries': ['US', 'CA'],
            },
            line_items=[{
            'price_data': {
                'currency': 'JPY',
                'product_data': {
                'name': 'T-shirt',
                },
                'unit_amount': 1000,
            },
            'quantity': 1,
            }],
            mode='payment',
            customer_email='abc@gmail.com',
            success_url='https://www.yahoo.co.jp',
            cancel_url='https://www.yahoo.co.jp',
            # payment_intent_data = {

            #     'shipping': {

            #         'name' : '安部草平',

            #         'address':{
            #             'line1' : '1-2-3',
            #             'country' : 'JP'
                        

            #         }
            #     }

            # }

        )

        res={
            "id":session.id
        }

        return JsonResponse(res)


    except Exception as e:
        return HttpResponse(e)

def custom(request):
    context = {
    #     'client_token': get_client_token(),
    #     'client_id' : client_id
        }
    return render(request, 's/custom.html', context)

def custom5(request):
    context = {
    #     'client_token': get_client_token(),
    #     'client_id' : client_id
        }
    return render(request, 's/custom5.html', context)


@csrf_exempt
def create_payment(request):

    try:
        data = json.loads(request.body)
        intent = stripe.PaymentIntent.create(
            amount=999,
            currency='JPY',
            payment_method_types=["card","alipay"]
        )

        res = {
            'clientSecret' : intent['client_secret']
        }

        return JsonResponse(res)

    except Exception as e:
        return HttpResponse(e) 

@csrf_exempt
def charge_token(request):
    try:

        res=stripe.Charge.create(
        amount=2000,
        currency="jpy",
        source=json.loads(request.body.decode('utf-8'))['tokenId'],
        description="charge on Token",
        )

        response = {
            "id":res.id,
            "amount":res.amount,
            "currency":res.currency,
            "status":res.status
        }
        print(type(response))
        return JsonResponse(response)

    except Exception as e:
        return HttpResponse(e) 

@csrf_exempt
def checkoutstart(request):

    session = request.session


    # if cart does not exist or cart is empty, immediately redirect to Cart page
    if user_cart not in session:
        
        return redirect('/s/cart')

    elif len(session[user_cart]) < 1:
        return redirect('/s/cart')

    _total = 0

    context = {
        's_public_key':s_public_key,
        'cart':session[user_cart],
    }

    return render(request, 's/checkoutstart.html', context)

@csrf_exempt
def create_paymentIntent(request):

    session = request.session

    _total = 0

    for item in session[user_cart]:
        _total += int(item['price'])

    _paymentIntentError = ''

    # chech if transaction session and paymentIntent exists for this user

    # session.pop('transaction')

    if 'transaction' in session :
        print('transaction exists')
        print(session['transaction'])

        # check the status of the paymentIntent within transaction session

        try:
            paymentIntent = stripe.PaymentIntent.retrieve( session['transaction']['paymentIntentId'])

            print(paymentIntent)

            if paymentIntent['status'] == 'requires_payment_method' :

                intentResult = {
                    "clientSecret" : paymentIntent.client_secret,
                    # "clientSecret" : "pi_1IHnuYCEBHSS0wYChABms9Fo_secret_716NycxVdsGzgssD62VSUHTCs",
                    "error" : _paymentIntentError
                }

                return JsonResponse(intentResult)
            
            elif paymentIntent['status'] == 'succeeded' :

                print('the payment has been already paid')

                session.pop(user_cart)
                session.pop('transaction')

                return redirect('/s/cart')
            
            
        except Exception as e:
            print(e)
            # redirect user to cart page to restart
            return redirect('/s/cart')


    # No Transaction Session exists so create paymentIntent and add to session transaction
    # paymentIntent expires much before Session expires

    else :

        try:
            paymentIntent = stripe.PaymentIntent.create(
                amount=_total,
                currency="jpy",
                payment_method_types=["card"],
            )

            print(paymentIntent)

            intentResult = {
                "clientSecret" : paymentIntent.client_secret,
                # "clientSecret" : "pi_1IHnuYCEBHSS0wYChABms9Fo_secret_716NycxVdsGzgssD62VSUHTCs",
                "error" : _paymentIntentError
            }

            transaction_data  = {

                "paymentIntentId" : paymentIntent.id,
                "clientSecret" : paymentIntent.client_secret

            }

            # add paymentIntent to transaction session
            session['transaction'] = transaction_data



            return JsonResponse(intentResult)

        except Exception as e:
            print(e)
            _paymentIntentError = e
            data ={
                "clientSecret" : '',
                "error" : _paymentIntentError
            }

            return JsonResponse(data)

@csrf_exempt
def clear_cart_transaction(request):

    session = request.session

    session[user_cart] = []
    session.pop('transaction')

    return HttpResponse('ok')