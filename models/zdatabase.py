# coding: utf8
from datetime import datetime

db.define_table('trade',
                Field('user_to', 'reference auth_user'),
                Field('user_from', 'reference auth_user'),
                Field('location', 'reference location'),
                Field('approved', 'boolean'),
                Field('date', 'datetime'),
                )

db.define_table('location',
                Field('user', 'reference auth_user'),
                Field('cord', 'string', default=""),
                Field('date', 'datetime'),
                Field('title', 'string', default=""),
                Field('note', 'text'),
                Field('rating', 'integer', default=1),
                Field('photo', 'reference photo'),
                )

db.define_table('rating',
                Field('user', 'reference auth_user'),
                Field('rating', 'integer', default=1),
                Field('location', 'reference location'),
                Field('date', 'datetime'),
                )

db.define_table('message',
                Field('user_to', 'reference auth_user'),
                Field('user_from', 'reference auth_user'),
                Field('subject', 'string', default=""),
                Field('date', 'datetime'),
                Field('note', 'text'),
                )

db.define_table('comment',
                Field('location', 'reference location'),
                Field('date', 'datetime'),
                Field('note', 'text'),
                Field('user', 'reference auth_user'),
                )

db.define_table('photo',
                Field('location', 'reference location'),
                Field('image', 'upload'),
                Field('private', 'boolean'),
                )
