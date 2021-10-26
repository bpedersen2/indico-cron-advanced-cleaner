# This file is part of the MLZ Indico plugins.
# Copyright (C) 2018 MLZ
#
# The MLZ Indico plugins are free software; you can redistribute
# them and/or modify them under the terms of the MIT License; see
# the LICENSE file for more details.

from __future__ import unicode_literals

from datetime import timedelta
from hashlib import sha512

from celery.schedules import crontab
from sqlalchemy.sql.expression import or_

from indico.core.celery import celery
from indico.core.db import db
from indico.modules.events.models.events import Event
from indico.modules.events.features.util import set_feature_enabled
from indico.modules.events.registration.models.form_fields import RegistrationFormField
from indico.modules.events.logs import EventLogEntry
from indico.modules.users.models.users import User
from indico.util.date_time import now_utc


@celery.periodic_task(run_every=crontab(day_of_month='1', hour='5'), plugin='cron_advanced_cleaner')
def run_anonymize():
    events = Event.query.filter(or_(Event.is_deleted, Event.end_dt < now_utc() - timedelta(days=365))).all()
    for event in events:
        if event.has_feature('anonymize_registrations'):
            anonymize_registrations(event)
            # disable feature to avoid multiple runs
            set_feature_enabled(event, 'anonymize_registrations', False)
            cleanup_logs(event)


@celery.periodic_task(run_every=crontab(day_of_month='1', hour='5'), plugin='cron_advanced_cleaner')
def run_anonymize_deleted_users():
    users = User.query.filter(User.is_deleted).all()
    for user in users:
        anonymize_deleted_user(user)


@celery.periodic_task(run_every=crontab(day_of_month='1', hour='5'), plugin='cron_advanced_cleaner')
def run_cleanup_log():
    events = Event.query.filter(Event.end_dt < now_utc() - timedelta(days=365)).all()
    for event in events:
        if event.has_feature('cleanup_log'):
            cleanup_logs(event)


def cleanup_logs(event):
    query = EventLogEntry.query.filter(EventLogEntry.logged_dt < now_utc() - timedelta(days=31),
                                       EventLogEntry.event == event)
    query.delete()
    db.session.commit()


def _hash(val):
    return sha512(val.encode('utf-8')+now_utc().isoformat().encode('utf-8')).hexdigest()[:12]


def anonymize_deleted_user(user):
    _anon_attrs = ['first_name', 'last_name', 'phone', 'address',]
    _clear_attrs_str = ['affiliation', 'email', 'secondary_emails', ]
    _clear_attrs_set = ['favorite_users', 'favorite_categories', 'identities']
    _clear_attrs_list = ['old_api_keys',]
    _clear_attrs_None = ['api_key',]


    for attr in _clear_attrs_str:
        setattr(user, attr, '')

    for attr in _clear_attrs_set:
        setattr(user, attr, set())

    for attr in _clear_attrs_list:
        setattr(user, attr, list())

    for attr in _anon_attrs:
        setattr(user, attr, _hash(getattr(user, attr) ))

def anonymize_registrations(event):
    for registration in event.registrations.all():
        for fid, rdata in registration.data_by_field.items():
            fieldtype = RegistrationFormField.find(id=fid).first().input_type
            if fieldtype in ('text', 'textarea'):
                rdata.data = _hash(rdata.data)
            elif fieldtype == 'email':
                rdata.data = _hash(rdata.data) + '@invalid.invalid'
            elif fieldtype == 'phone':
                rdata.data = '(+00) 0000000'
            elif fieldtype == 'date':
                # Keep dates for now
                pass
            elif fieldtype == 'country':
                # Keep country for now
                pass
        # other field types are not touched (choice, mulitchoice, radio)

        registration.first_name = _hash(registration.first_name)
        registration.last_name = _hash(registration.last_name)
        registration.email = _hash(registration.email)
        if registration.user:
            registration.user = None
    db.session.commit()
