# This file is part of the MLZ Indico plugins.
# Copyright (C) 2018 MLZ
#
# The MLZ Indico plugins are free software; you can redistribute
# them and/or modify them under the terms of the MIT License; see
# the LICENSE file for more details.

from __future__ import unicode_literals

from wtforms import ValidationError

from indico.core.plugins import IndicoPlugin
from indico.core.settings.converters import SettingConverter
from indico.modules.categories.models.categories import Category
from indico.modules.rb.models.rooms import Room
from indico.util.string import natural_sort_key
from indico.web.forms.base import IndicoForm
from wtforms.fields.simple import BooleanField


class AdvancedCleanerCronjobsPlugin(IndicoPlugin):
    """Advanced event cleaner cronjobs

    This plugin provides two task and associated event features:

    1) run_anonymize: If the feature `anonymize_registrations` is
       enabled on an event, then all registrations will be anonymized
       if the  event is older than 1 year or deleted.
       The task per default runs on the first of every month.
       Log entries will be deleted in this case as well.
    2) run_anonymize_deleted_users: Anonymize deleted user records
       The task per default runs on the first of every month.
    3) run_cleanup_log: If the feature `cleanup_log` is set, then clean
       log  entries if the event is older than 1 year.
       The task per default runs  on the first of every month.
    """
    configurable = False
