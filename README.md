Advanced event cleaner cronjobs
===========================

This plugin provides two task and associated event features:

  1) run_anonymize: If the feature `anonymize_registrations` is
     enabled on an event, then all registrations will be anonymized
     if the  event is older than 1 year or deleted.
     The task per default runs on the first of every month.
     Log entries will be deleted in this case as well.
  2) run_cleanup_log: If the feature `cleanup_log` is set, then clean
     log  entries if the event is older than 1 year.
     The task per default runs  on the first of every month.
