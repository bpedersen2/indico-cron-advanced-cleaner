# This file is part of the MLZ Indico plugins.
# Copyright (C) 2018 MLZ
#
# The MLZ Indico plugins are free software; you can redistribute
# them and/or modify them under the terms of the MIT License; see
# the LICENSE file for more details.

from indico.util.i18n import _
from indico.modules.events.features.base import EventFeature


class CleanLogFeature(EventFeature):
    name = 'cleanup_log'
    friendly_name = _('Cleanup Logs')
    description = _('Let a cron task cleanup the log after a certain period.')

class AnonymizeFeature(EventFeature):
    name = 'anonymize_registrations'
    friendly_name = _('Anonymize Registrations')
    description = _('Let a cron task anonymize registrations after a certain period.')
