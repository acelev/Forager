# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################

@auth.requires_login()
def index():
    user = auth.user
    locations = db(db.location.user == auth.user_id).select(
                                       orderby=~db.location.date)
    pendingtrades = db(db.trade).select()
     
    return dict(user=user, locations=locations,
pendingtrades=pendingtrades)

@auth.requires_login()
def createprofile(): 
   form = SQLFORM(db.user)
   if form.process().accepted:
       response.flash = 'profile saved'
       redirect(URL('index'))
   elif form.errors:
       response.flash = 'profile has errors'
   else:
       response.flash = 'Please take a minute to fill out your profile'
   return dict(form=form)

@auth.requires_login()
def trade():
   if session.location == None:
      redirect(URL('index'))
   location = db.location[session.location]
   db.trade.user_from.readable = db.trade.user_from.writable = False
   db.trade.user_to.default = db.auth_user[location.user]
   db.trade.user_to.readable = db.trade.user_to.writable = False
   db.trade.approved.default  = False
   db.trade.approved.readable = db.trade.approved.writable = False
   db.trade.location_to.default = location 
   db.trade.location_to.readable = db.trade.location_to.writable = False
   form = SQLFORM(db.trade) 
   if form.process().accepted:
      #response.flash = 'trade sent'
      session.location = None
      redirect(URL('viewlocation', args=[location.id])) 
   elif form.errors:
      response.flash = 'trade has errors'
   else:
      response.flash = 'pick a location to trade!'
   return dict(form=form,location=location, user=db.auth_user[location.user] ) 

@auth.requires_login()
def addlocation():
   form = SQLFORM(db.location)
   if form.process().accepted:
       response.flash = 'location saved'
       redirect(URL('index'))
   elif form.errors:
       response.flash = 'location has errors'
   else:
       response.flash = 'give us some info about the location'
   return dict(form=form) 

@auth.requires_login()
def viewlocation():
   location = db.location(request.args[0]) or redirect(URL('index'))
   if auth.user_id == location.user:
      return dict(fullview=True,location=location) 
   #db(db.trade.user_to == auth.user
       # ,db.trade.location_from == location, db.trade.approved == True)
 
   return dict(fullview = False, location=location) 

def ajaxlivesearch():
    partialstr = request.vars.values()[0]
    query = db.location.title.like('%'+partialstr+'%')
    locations = db(query).select(db.location.title)
    items = []
    for (i,location) in enumerate(locations):
        items.append(DIV(A(location.title, _id="res%s"%i, 
          _href="#", _onclick="copyToBox($('#res%s').html())"%i), 
          _id="resultLiveSearch"))

    return TAG[''](*items) 

def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()


@auth.requires_signature()
def data():
    """
    http://..../[app]/default/data/tables
    http://..../[app]/default/data/create/[table]
    http://..../[app]/default/data/read/[table]/[id]
    http://..../[app]/default/data/update/[table]/[id]
    http://..../[app]/default/data/delete/[table]/[id]
    http://..../[app]/default/data/select/[table]
    http://..../[app]/default/data/search/[table]
    but URLs must be signed, i.e. linked with
      A('table',_href=URL('data/tables',user_signature=True))
    or with the signed load operator
      LOAD('default','data.load',args='tables',ajax=True,user_signature=True)
    """
    return dict(form=crud())
