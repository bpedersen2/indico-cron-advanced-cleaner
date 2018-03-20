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
from indico.modules.events.logs import EventLogEntry
from indico.util.date_time import now_utc


@celery.periodic_task(run_every=crontab(day_of_month='1', hour='5'), plugin='cron_advanced_cleaner')
def run_anonymize():
    events = Event.query.filter(or_(Event.is_deleted, Event.end_dt < now_utc() - timedelta(days=365))).all()
    for event in events:
        if event.has_feature('anonymize_registrations'):
            anonymize_registrations(event)
            # disable feature to avoid multiple runs
            set_feature_enabled(event,'anonymize_registrations',False)
            cleanup_logs(event)

@celery.periodic_task(run_every=crontab(day_of_month='1', hour='5'), plugin='cron_advanced_cleaner')
def run_cleanup_log():
    events = Event.query.filter(Event.end_dt < now_utc() - timedelta(days=365) ).all()
    for event in events:
        if event.has_feature('cleanup_log'):
            cleanup_logs(event)

def cleanup_logs(event):
    query = EventLogEntry.query.filter(EventLogEntry.logged_dt < now_utc() - timedelta(days=31),
                                       EventLogEntry.event == event)
    query.delete()
    db.session.commit()

def _hash(val):
    return sha512(val.encode('utf-8')).hexdigest()[:12]

def anonymize_registrations(event):
    for registration in event.registrations.all():
        for rdata in registration.data:
            if isinstance(rdata.data, unicode):
                rdata.data = _hash(rdata.data)
        registration.first_name = _hash(registration.first_name)
        registration.last_name = _hash(registration.last_name)
        registration.email = _hash(registration.email)
    db.session.commit()
