# This file is part of the MLZ Indico plugins.
# Copyright (C) 2018 MLZ
#
# The MLZ Indico plugins are free software; you can redistribute
# them and/or modify them under the terms of the MIT License; see
# the LICENSE file for more details.

from __future__ import unicode_literals

from indico.core import signals


@signals.import_tasks.connect
def _import_tasks(sender, **kwargs):
    import indico_cron_advanced_cleaner.tasks

@signals.event.get_feature_definitions.connect
def _get_feature_definitions(sender, **kwargs):
    from .features import CleanLogFeature, AnonymizeFeature
    yield CleanLogFeature
    yield AnonymizeFeature
