# coding: utf8
from datetime import datetime

db.define_table('trade',
                Field('user_to', 'refrence auth_user'),
                Field('user_from', 'refrence auth_user'),
                Field('location', 'refrence location'),
                Field('approved', 'boolean', default=FALSE),
                Field('date', 'datetime'),
                )

db.define_table('location',
                Field('user', 'refrence auth_user'),
                Field('cord', 'string', default=""),
                Field('date', 'datetime'),
                Field('title', 'string', default=""),
                Field('note', 'text'),
                Field('rating', 'integer', default=1),
                Field('photo', 'refrence photo'),
                )

db.define_table('rating',
                Field('user' 'refrence auth_user'),
                Field('rating', 'integer', default=1),
                Field('location', 'refrence location'),
                Field('date', 'datetime'),
                )

db.define_table('message',
                Field('user_to', 'refrence auth_user'),
                Field('user_from', 'refrence auth_user'),
                Field('subject', 'string', default=""),
                Field('date', 'datetime'),
                Field('note', 'text'),
                )

db.define_table('comment',
                Field('location', 'refrence location'),
                Field('date', 'datetime'),
                Field('note', 'text'),
                Field('user', 'refrence auth_user'),
                )

db.define_table('photo',
                Field('location', 'refrence location'),
                Field('image', 'upload'),
                Field('private', 'boolean', default=TRUE),
                )
