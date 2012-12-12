# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.title = ' '.join(word.capitalize() for word in request.application.split('_'))
response.subtitle = T('mushroom database')

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Aidan Seine <aidanseine@gmail.com>'
response.meta.description = 'A searchable user-generated mushroom database'
response.meta.keywords = 'edibles, foraging, mushroom'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('login'), False, URL('default','index'), []),
    (T('Browse'), False, URL('default','search', args=['0','all']), []),
    (T('About'), False, URL('default','index'), []),
    ]
if auth.user:
	response.menu = [
    (T(auth.user.user_name), False, URL('default','index'), []),
    (T('Messages'), False, URL('default','messages', args=['0','0']), []),
    (T('Trades'), False, URL('default','viewtrades', args=[auth.user.id, '0']), []),
    (T('Locations'), False, URL('default','viewlocations',args=[auth.user.id, '0']), []),
    (T('Browse'), False, URL('default','search', args=['0','all']), []),
    (T('About'), False, URL('default','index'), []),
    (T('Logout'), False, URL('user/logout'), []),
    ]


