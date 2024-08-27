#!/usr/bin/python3
from flask import Flask, render_template, abort, jsonify, request, redirect, url_for
import requests


app = Flask(__name__)

url_link = 'https://jws-collections-gi44.vercel.app/api/v1/'

def get_pics(page_num=1, per_page=20):
    link = url_link + f'products?page={page_num}&per_page={per_page}'
    print(link)
    r = requests.get(link)
    return r.json() if r.status_code == 200 else None

@app.route('/', methods=['GET'], strict_slashes=False)
def index():
    data = get_pics().get('products', None)
    if data is None:
        abort(400)
    return render_template('landing-page.html', data=data)

@app.route('/login', strict_slashes=False)
@app.route('/signup', strict_slashes=False)
def login_signup():
    return render_template('login_signup.html'), 200

@app.route('/store', strict_slashes=False)
def store():
    return render_template('store.html'), 200


@app.route('/checkout', strict_slashes=False)
def checkout():
    return render_template('checkout.html'), 200

@app.route('/order', strict_slashes=False)
def order():
    return render_template('orders.html'), 200


@app.errorhandler(400)
def error400(error):
    return jsonify('Page not found'), 400

if __name__ == "__main__":
    app.run('0.0.0.0', debug=True)

