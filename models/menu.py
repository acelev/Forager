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
    (T('Home'), False, URL('default','index'), []),
    (T('Search'), False, URL('default','index'), []),
    (T('Profile'), False, URL('default','index'), []),
    (T('Forum'), False, URL('default','index'), []),
    (T('About'), False, URL('default','index'), []),
    ]
