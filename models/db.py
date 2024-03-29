# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL('sqlite://storage.sqlite')
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'

#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Crud, Service, PluginManager, prettydate
from datetime import datetime
auth = Auth(db)

## after auth = Auth(db)
db.define_table(
    auth.settings.table_user_name,
    Field('user_name', length=128, default='', unique=True),
    Field('email', length=128, default=''), # required
    Field('password', 'password', length=512,            # required
          readable=False, label='Password'),
    Field('city'),
    Field('zip'),
    Field('bio', 'text', default=''),
    Field('rating', 'integer', default=1, readable=False, writable=False),
    Field('image', 'upload', uploadfield='picture_file'),
    Field('picture_file', 'blob'),
    Field('date', 'datetime', default=datetime.utcnow(), writable=False),
    Field('registration_key', length=512,                # required
          writable=False, readable=False, default=''),
    Field('reset_password_key', length=512,              # required
          writable=False, readable=False, default=''),
    Field('registration_id', length=512,                 # required
          writable=False, readable=False, default=''))

''' gmail logon
from gluon.contrib.login_methods.email_auth import email_auth
auth.settings.login_methods.append(
    email_auth("smtp.gmail.com:587", "@gmail.com"))
'''

## do not forget validators
custom_auth_table = db[auth.settings.table_user_name] # get the custom_auth_table
custom_auth_table.user_name.requires = [
  IS_NOT_EMPTY(error_message=auth.messages.is_empty),
  IS_NOT_IN_DB(db, custom_auth_table.user_name, 
        error_message='User name already taken. Try another.')]
#custom_auth_table.password.requires = [IS_STRONG(), CRYPT()]
custom_auth_table.email.requires = [
  IS_EMAIL(error_message=auth.messages.invalid_email),
  IS_NOT_IN_DB(db, custom_auth_table.email,
        error_message='Email already in use. Try another.')]

auth.settings.table_user = custom_auth_table # tell auth to use custom_auth_table


## before auth.define_tables(
crud, service, plugins = Crud(db), Service(), PluginManager()


## create all tables needed by auth if not custom tables
auth.define_tables(username=False, signature=False)

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' or 'smtp.gmail.com:587'
mail.settings.sender = 'you@gmail.com'
mail.settings.login = 'username:password'

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

## if you need to use OpenID, Facebook, MySpace, Twitter, Linkedin, etc.
## register with janrain.com, write your domain:api_key in private/janrain.key
from gluon.contrib.login_methods.rpx_account import use_janrain
use_janrain(auth, filename='Forager:d38c6962a4c1fb2c8b591e09fa5f3f1b29f08005')

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
