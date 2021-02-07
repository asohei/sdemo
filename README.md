# Stripe: Getting Started with sample demo application

## Running Locally

Make sure you have Python 3 [installed locally](http://install.python-guide.org). To push to Heroku, you'll need to install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli), as well as [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ git clone https://github.com/asohei/sdemo.git
$ cd sdemo

$ pip3 install -r requirements.txt

$ python3 manage.py migrate

$ touch .env

add your stripe api keys

    s_public_key = pk_test_XXXXX
    s_api_secret = sk_test_XXXXX

$ python3 manage.py runserver