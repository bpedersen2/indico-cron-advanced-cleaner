# This file is part of the CERN Indico plugins.
# Copyright (C) 2014 - 2018 CERN
#
# The CERN Indico plugins are free software; you can redistribute
# them and/or modify them under the terms of the MIT License; see
# the LICENSE file for more details.

from __future__ import unicode_literals

from indico.core import signals
from indico.modules.events.features.base import EventFeature


@signals.import_tasks.connect
def _import_tasks(sender, **kwargs):
    import indico_cron_advanced_cleaner.tasks

@signals.event.get_feature_definitions.connect
def _get_feature_definitions(sender, **kwargs):
    yield CleanLogFeature
    yield AnonymizeFeature

class CleanLogFeature(EventFeature):
    name = 'cleanup_log'
    friendly_name = _('Cleanup Logs')
    description = _('Let a cron task cleanup the log after a certain period.')

class AnonymizeFeature(EventFeature):
    name = 'anonymize_registrations'
    friendly_name = _('Anonymize Registrations')
    description = _('Let a cron task anonymize registrations after a certain period.')
