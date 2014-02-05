automated-ebs-snapshots
=======================

Automated EBS Snapshots helps you ensure that you have up to date snapshots of
your EBS volumes.

All you need to do to get started is documented below.

Installation
------------
::

    pip install automated-ebs-snapshots

Authentication configuration
----------------------------

Automated EBS snapshots can be configured either via command line options or via command line options.

Command line options
^^^^^^^^^^^^^^^^^^^^

You can use the following command line options to authenticate to AWS.
::

    AWS configuration options:
      --access-key-id ACCESS_KEY_ID
                            AWS access key
      --secret-access-key SECRET_ACCESS_KEY
                            AWS secret access key
      --region REGION       AWS region

Configuration file
^^^^^^^^^^^^^^^^^^

Create a configuration file anywhere on you file system.
::

    [general]
    access-key-id: xxxx
    secret-access-key: xxxxxxxx
    region: eu-west-1

Then use the ``--config`` command line option to point at your configuration file.

Watching and unwatching volumes
-------------------------------

Start watching a volume
^^^^^^^^^^^^^^^^^^^^^^^

In order to enable automatic snapshots, you need to start watching the volume.
The following command will add ``vol-13245678`` to the watchlist with snapshots
created daily.
::

    automated-ebs-snapshots --config ~/auto-ebs-snapshots.conf --watch vol-12345678 --interval daily

List watched volumes
^^^^^^^^^^^^^^^^^^^^

List the currently watched volumes and their backup interval
::

    automated-ebs-snapshots --config ~/automated-ebs-snapshots.conf --list

Stop watching a volume
^^^^^^^^^^^^^^^^^^^^^^

To stop creating automated backups for a volume, run this:
::

    automated-ebs-snapshots --config ~/automated-ebs-snapshots.conf --unwatch vol-12345678

Creating snapshots
------------------

Now, to start taking snapshots you will need to have Automated EBS Snapshots
running.
::

    automated-ebs-snapshots --config ~/automated-ebs-snapshots.conf --run

It will check if there are any volumes with no or too old snapshots. New
snapshots will be created if needed.

There is no daemon mode currently, so you will need to run something like this.
::

  nohup while true ; do automated-ebs-snapshots --config ~/automated-ebs-snapshots.conf --run >> /var/log/automated-ebs-snapshots.log 2>&1 ; sleep 600 ; done

Author
------

This project is maintained by `Sebastian Dahlgren <http://www.sebastiandahlgren.se>`__ and it is supported by `Skymill Solutions <http://www.skymillsolutions.com>`__.

License
-------

APACHE LICENSE 2.0
Copyright 2014 Skymill Solutions

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   `http://www.apache.org/licenses/LICENSE-2.0 <http://www.apache.org/licenses/LICENSE-2.0>`__

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
