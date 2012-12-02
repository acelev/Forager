# coding: utf8
from datetime import datetime

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
                Field('photo', 'upload', uploadfield='picture_file'),
                Field('picture_file', 'blob'),
                )


db.define_table('trade',
                Field('user_to', 'reference auth_user'), 
                                                  #readable = False,
                                                  #writable = False),
                Field('user_from', 'reference auth_user', default = auth.user_id),
                                                    #,readable = False,
                                                    #writable = False),
                Field('location_to', 'reference location'), #default = db.location[0],
                                                    #writable = False,
                                                    #readable = False),
                Field('location_from', 'reference location', requires =
                  IS_IN_DB(db(db.location.user.like(auth.user_id)), 'location.id')),
                  #default = 0, 
                  #requires = IS_IN_DB(db(db.location.user ==
                  #         auth.user_id).select(), 'title', zero=T('choose location'))),
                Field('approved', 'boolean' ),#default = False,
                                             #writable = False,
                                             #readable = False),
                Field('date', 'datetime',default = datetime.utcnow(),
                                                    readable = False,
                                                    writable = False),
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
