#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Website server for geekup.in
"""

from flask import Flask
from flaskext.assets import Environment, Bundle
from flaskext.mail import Mail
from coaster import configureapp
from os import environ

# First, make an app and config it

app = Flask(__name__, instance_relative_config=True)
configureapp(app, 'GEEKUP_ENV')
mail = Mail()
mail.init_app(app)
assets = Environment(app)

# Second, setup assets

js = Bundle('js/libs/jquery-1.6.4.js',
            'js/libs/jquery.form.js',
            'js/scripts.js',
            filters='jsmin', output='js/packed.js')

assets.register('js_all', js)

# Third, after config, import the models and views

import geekup.models
import geekup.views
if environ.get('GEEKUP_ENV') == 'prod':
    import geekup.loghandler

# Fourth, setup admin for the models

from flask.ext import admin
from flask.ext.admin.datastore.sqlalchemy import SQLAlchemyDatastore
from geekup.views.login import lastuser

admin_datastore = SQLAlchemyDatastore(geekup.models, geekup.models.db.session)
admin_blueprint = admin.create_admin_blueprint(admin_datastore,
    view_decorator=lastuser.requires_permission('siteadmin'))

app.register_blueprint(admin_blueprint, url_prefix='/admin')
