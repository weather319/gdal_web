from app import app, db
from flask_login import login_user, logout_user, current_user, login_required
from flask import render_template, flash, redirect, session, url_for, request, g
from .forms import LoginForm
from .models import User

@app.route('/')
@app.route('/index')
def index():
    pass

@app.errorhandler(404)
def page_not_found(e):
     return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
     return render_template('500.html'), 500


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME']:
            error = 'Invalid username'
        elif request.form['password'] != app.config['PASSWORD']:
            error = 'Invalid password'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('history'))
    return render_template('login.html', error=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    stripe_token = request.form['stripeToken']
    email = request.form['stripeEmail']
    product_id = request.form['product_id']
    product = Product.query.get(product_id)
    try:
        charge = stripe.Charge.create(
                amount=int(product.price * 100),
                currency='usd',
                card=stripe_token,
                description=email)
    except stripe.CardError, e:
        return """<html><body><h1>Card Declined</h1><p>Your chard could not
        be charged. Please check the number and/or contact your credit card
        company.</p></body></html>"""
    print charge
    purchase = Purchase(uuid=str(uuid.uuid4()),
            email=email,
            product=product)
    db.session.add(purchase)
    db.session.commit()
    message = Message(
            subject='Thanks for your purchase!',
        sender="jeff@jeffknupp.com", 
        html="""<html><body><h1>Thanks for buying Writing Idiomatic Python!</h1>
                <p>If you didn't already download your copy, you can visit 
                <a href="http://buy.jeffknupp.com/{}">your private link</a>. You'll be able to
download the file up to five times, at which point the link will
                expire.""".format(purchase.uuid),
        recipients=[email])
    with mail.connect() as conn:
        conn.send(message)
    return redirect('/{}'.format(purchase.uuid))


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))

@app.route('/history')
def history():
    pass

@app.route('/analysis')
def analysis():
    pass


@app.route('/vedio')
def vedio():
    pass