# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a samples controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
## - call exposes all registered services (none by default)
#########################################################################
import re


@auth.requires_login()
def index():
    user = auth.user
    locations = db(db.location.user == auth.user_id).select(
                                       orderby=~db.location.date)
    pendingtrades = db((db.trade.user_to == auth.user_id)
      & (db.trade.approved == False)).select(orderby=~db.trade.date)
    approvedtrades = db((db.trade.user_to == auth.user_id) | (db.trade.user_from == auth.user_id) 
      &(db.trade.approved == True)).select(orderby=~db.trade.date)
    newmessages = db((db.message.user_to==auth.user_id)&(db.message.read==False)).count()
    return dict(user=user, newmessages=newmessages,
            locations=locations,pendingtrades=pendingtrades, approvedtrades=approvedtrades)

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
def viewuser():
  user = db.auth_user[request.args[0]] or redirect(URL('index'))
  locations = db(db.location.user == user.id).select(
                                       orderby=~db.location.date)
  return dict(user=user, locations=locations)

def search():
  syntax = re.compile('^.*$')
  order = db.location.date
  results = []
  page = int(request.args[0])
  if not request.args:
    redirect( URL('search', args = [0,'all']))
  search_terms = request.args[1]
  if search_terms == 'all':
    results = pagination(db.location,9, page, order) 
    return dict(results=results, search_terms=search_terms, page=page)
  for terms in search_terms:
    terms = terms.lower()
    terms = syntax.findall(terms)
    for term in terms:
      term = term.split('_')
      for word in term:
        word = '%'+word+'%'
        query = (db.location.title.lower().like(word))|(db.location.mushroom.like(word)) 
        results = pagination(query, 9, page, ~order)
  return dict(results=results, search_terms=search_terms, page=page)

def pagination(query,itemsPerPage, page, orderby):
   limitby = (page*itemsPerPage,(page+1)*itemsPerPage+1)
   return db(query).select(orderby=orderby, limitby=limitby) 
   

@auth.requires_login()
def viewlocations():
   user = db.auth_user[request.args[0]] or redirect(URL('index'))
   page = int(request.args[1]) or 0
   query = (db.location.user == user)
   orderby = ~db.location.date   
   if page < 0:
      page = 0 
   return dict(user=user,page=page, locations = pagination(query, 4,page, orderby))

@auth.requires_login()
def viewpendingtrades():
   user = db.auth_user[request.args[0]] or redirect(URL('index'))
   page = int(request.args[1]) or 0
   query = (db.trade.user_to == auth.user_id) & (db.trade.approved == False)
   orderby = ~db.trade.date
   if page < 0:
      page = 0 
   return dict(user=user,page=page, pendingtrades = pagination(query, 4,
page,orderby))


@auth.requires_login()
def viewtrades():
   user = db.auth_user[request.args[0]] or redirect(URL('index'))
   page = int(request.args[1])
   query = (db.trade.user_to == auth.user_id) | (db.trade.user_from == auth.user_id) & (db.trade.approved == True)
   orderby = ~db.trade.date
   if page < 0:
      page = 0 
   return dict(user=user,page=page, approvedtrades = pagination(query, 4,page,orderby))

def accept(trade):
   trade.approved = True
   trade.update_record()
   db.commit()
   redirect(URL('index'))

def declined(trade):
   db(db.trade.id == trade.id).delete()
   db.commit()
   redirect(URL('index'))

@auth.requires_login()
def viewtrade():
   trade = db.trade[request.args[0]] or redirect(URL('index'))
   if trade.approved:
      form = FORM(INPUT(_type='submit', _name='decline', _value='Remove'))
   else:
      form = FORM(INPUT(_type='submit', _name='accept', _value= 'Accept'),
                  INPUT(_type='submit', _name='decline', _value='Decline')) 
   if request.vars['accept']:
      accept(trade) 
   elif request.vars['decline']:
      declined(trade)
   return dict(trade=trade, form=form)

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
      response.flash = form.vars.location_from 
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


def upvote(location, user):
   location.rating+=1
   location.update_record()
   id_ = db.location_rating.insert()
   location.user.rating+=1
   location.update_record()
   location.user.update_record() 
   db.commit()
   return id_

def downvote(location,user):
   if location.rating - 1 > 0:
      location.rating-=1
   else:
      location.rating = 0
   if location.user.rating - 1 > 0:
      location.user.rating-=1
   else:
      user.rating = 0
   id_ = db.location_rating.insert()
   location.update_record()
   location.user.update_record()
   db.commit()



@auth.requires_login()
def viewlocation():
   location = db.location(request.args[0]) or redirect(URL('index'))
   rateForm = None
   rating = db((db.location_rating.user == auth.user_id) &
   (db.location_rating.location == location.id)).select().first()
   if rating ==  None:
      rateForm = FORM(INPUT(_type = 'submit', _name ='upvote', _value ='Up vote'),
               INPUT(_type = 'submit', _name ='downvote', _value= 'Down Vote')) 
   
   if request.vars['upvote']:
      db.location_rating.location.default = location
      upvote(location, auth.user)
      redirect(URL('viewlocation', args=[request.args[0]]))
   if request.vars['downvote']:
      db.location_rating.location.default = location
      downvote(location, auth.user)
      redirect(URL('viewlocation', args=[request.args[0]]))

   if auth.user_id == location.user:
      return dict(fullview=True,location=location, form=rateForm) 
   trade = db((db.trade.user_from == auth.user_id) &
            (db.trade.location_to == location)).select().first()
   if trade <> None and trade.approved:
      return dict(fullview=True, location=location, form=rateForm) 
   othertrade = db((db.trade.user_to == auth.user_id) &
               (db.trade.location_from == location)).select().first()
   if othertrade <> None  and othertrade.approved: 
      return dict(fullview=True, location=location, form=rateForm) 
 
   return dict(fullview = False, location=location, trade=trade) 

def ajaxlivesearch():
    partialstr = request.vars.values()[0]
    query = db.location.title.like('%'+partialstr+'%')
    shroomquery = db.location.mushroom.like('%'+partialstr+'%')
    shroomlocations = db(shroomquery).select(db.location.mushroom)
    locations = db(query).select(db.location.title)
    items = []
    for (i,location) in enumerate(locations):
        items.append(DIV(A(location.title, _id="res%s"%i, 
          _href="#", _onclick="copyToBox($('#res%s').html())"%i), 
          _id="resultLiveSearch"))
        
    for(i, location) in enumerate(shroomlocations):
        items.append(DIV(A(location.mushroom, _id="res%s"%i, 
          _href="#", _onclick="copyToBox($('#res%s').html())"%i), 
          _id="resultLiveSearch"))
    return TAG[''](*items) 

@auth.requires_login()
def messages():
  orderby=~db.message.date
  ipage = int(request.args[0])
  spage = int(request.args[1])
  iquery = (db.message.user_to == auth.user_id)
  squery = (db.message.user_from == auth.user_id)
  if ipage < 0:
      ipage = 0
  if spage < 0:
      spage = 0
  inbox = pagination(iquery, 9, ipage, orderby)
  sent = pagination(squery, 9, spage,orderby)
  return dict(inbox=inbox, ipage=ipage, spage=spage, sent=sent)

@auth.requires_login()
def viewmessage():
  message = db.message[request.args[0]]
  message.read = True
  message.update_record()
  db.commit()
  sender = message.user_from
  if message == None:
    redirect(URL('messages', args=[0,0]))
  return dict(message=message, sender=sender)

@auth.requires_login()
def newmessage():
  if request.args[0] == 'reply':
    message = db.message[request.args[1]]
    db.message.user_to.default=message.user_from.id
    db.message.user_from.default=auth.user_id
    db.message.user_to.writable=db.message.user_to.readable=False
    db.message.user_from.writable=db.message.user_from.readable=False
    db.message.subject.default='Re:'+message.subject
    note = '\n\n\nOn '+str(message.date)+' '+message.user_from.user_name+' wrote: \n'+message.note
    db.message.note.default=note
    db.message.read.default=False
    db.message.read.readable=db.message.read.writable=False
    db.message.date.readable=db.message.date.writable=False
    recipient=message.user_from
  else:
    db.message.user_to.default=db.auth_user[request.args[0]].id
    db.message.user_from.default=auth.user_id
    db.message.user_to.writable=db.message.user_to.readable=False
    db.message.user_from.writable=db.message.user_from.readable=False
    db.message.note.default=""
    db.message.read.default=False
    db.message.read.readable=db.message.read.writable=False
    db.message.date.readable=db.message.date.writable=False
    recipient=db.auth_user[request.args[0]]
  sender=auth.user

  form = SQLFORM(db.message)
  if form.process().accepted:
    response.flash = 'message sent'
    redirect(URL('messages', args=[0,0]))
  elif form.errors:
    response.flash = 'message has errors'
  else:
    response.flash = 'fill out message'
  return dict(form=form, sender=sender, recipient=recipient)


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
