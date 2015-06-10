import os
import logging

from flask import Flask
from flask import request, render_template, flash, url_for, redirect

from google.appengine.ext import ndb

from wtforms.ext.appengine.ndb import model_form
from wtforms import validators, Form

from secret_keys import CSRF_SECRET_KEY, SESSION_KEY

app = Flask(__name__)
app.config.update(
    SECRET_KEY=CSRF_SECRET_KEY,
    CSRF_SESSION_KEY=SESSION_KEY,
    CSRF_ENABLED=True
)

if 'SERVER_SOFTWARE' in os.environ and os.environ['SERVER_SOFTWARE'].startswith('Dev'):
    app.config.update(
        DEBUG=True
    )
else:
    app.config.update(
        DEBUG=False
    )


USERS = tuple('DXLR')

class Expense(ndb.Model):
    """Expense entity"""
    item_name = ndb.StringProperty(required=True)
    amount = ndb.FloatProperty(required=True)
    purchase_date = ndb.DateProperty()

    timestamp = ndb.DateTimeProperty(auto_now_add=True)

ExpenseForm = model_form(Expense, field_args={
    'item_name': dict(validators=[validators.Required()]),
    'amount': dict(validators=[validators.Required()]),
})

@app.route('/')
def index():
    """Show the default view"""
    form = ExpenseForm()
    return render_template('index.html', form=form)


@app.route('/', methods=['POST'])
def new():
    form = ExpenseForm()
    if request.method == 'POST' and form.validate():
        flash('Success', 'success')
        return "submitted"

    flash('Error submitting form.', 'error')
    return redirect(url_for('index'))
