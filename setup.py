# This file is part of the MLZ Indico plugins.
# Copyright (C) 2018 MLZ
#
# The MLZ Indico plugins are free software; you can redistribute
# them and/or modify them under the terms of the MIT License; see
# the LICENSE file for more details.

from __future__ import unicode_literals

from setuptools import find_packages, setup


setup(
    name='indico-cron-advanced-cleaner',
    url='https://github.com/bpedersen2/indico-cron-advanced-cleaner',
    license='MIT',
    author='MLZ Indico Team',
    author_email='bjoern.pedersen@frm2.tum.de',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=['indico>=3.1'],
    use_scm_version={"write_to":"indico_cron_advanced_cleaner/version.py",
                     "local_scheme":"node-and-timestamp"},
    setup_requires = ["setuptools>=39", "setuptools_scm[toml]>=3.4"],
    entry_points={
        'indico.plugins': {'cron_advanced_cleaner=indico_cron_advanced_cleaner.plugin:AdvancedCleanerCronjobsPlugin'}
    },
    classifiers=[
        'Environment :: Plugins',
        'Environment :: Web Environment',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
)
