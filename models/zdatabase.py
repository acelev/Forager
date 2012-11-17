# coding: utf8
from datetime import datetime


db.define_table('trade',
                Field('user_to', 'reference auth_user', readable = False,
                                                   writable = False),
                Field('user_from', 'reference auth_user', default =
                                                     auth.user,
                                                    readable = False,
                                                    writable = False),
                Field('location_to', 'reference location'
          #,requires= IS_IN(db().select(db.location.user.user == auth.user
                ),
                Field('location_from', 'reference location'),
                Field('approved', 'boolean'),
                Field('date', 'datetime',default=datetime.utcnow()),
                )

db.define_table('location',
                Field('user', 'reference auth_user', default=auth.user_id,
                                          readable = False,
                                          writable = False),
                Field('date', 'datetime',default=datetime.utcnow(),
                                          readable = False,
                                          writable = False),
                Field('longitude', 'float'),
                Field('latitude', 'float'),
                Field('title', 'string', default="Title",
                                          requires=IS_NOT_EMPTY()),
                Field('mushroom', 'string', default= "Mushroom",
                                          requires=IS_NOT_EMPTY()),
                Field('note', 'text', default = "Enter note here"),
                Field('rating', 'integer', default=1,
                                           writable = False),
                #Field('photo', 'reference photo'),
                Field('photo', 'upload'),
                )

db.define_table('location_rating',
                Field('user', 'reference auth_user'),
                Field('rating', 'integer', default=1),
                Field('location', 'reference location'),
                Field('date', 'datetime',default=datetime.utcnow()),
                )

db.define_table('message',
                Field('user_to', 'reference auth_user'),
                Field('user_from', 'reference auth_user'),
                Field('subject', 'string', default=""),
                Field('date', 'datetime', default=datetime.utcnow()),
                Field('note', 'text'),
                )

db.define_table('comment',
                Field('location', 'reference location'),
                Field('date', 'datetime', default=datetime.utcnow()),
                Field('note', 'text'),
                Field('user', 'reference auth_user'),
                )

db.define_table('photo',
                Field('location', 'reference location'),
                Field('image', 'upload'),
                Field('private', 'boolean'),
                )
