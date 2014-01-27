# automated-ebs-snapshots

Automated EBS Snapshots helps you ensure that you have up to date snapshots of
your EBS volumes.

All you need to do to get started is documented below.

## Installation

    pip install automated-ebs-snapshots

## Authentication configuration

Automated EBS snapshots can be configured either via command line options
or via command line options.

### Command line options

You can use the following command line options to authenticate to AWS.

    AWS configuration options:
      --access-key-id ACCESS_KEY_ID
                            AWS access key
      --secret-access-key SECRET_ACCESS_KEY
                            AWS secret access key
      --region REGION       AWS region

### Configuration file

Create a configuration file anywhere on you file system.

    [general]
    access-key-id: xxxx
    secret-access-key: xxxxxxxx
    region: eu-west-1

Then use the `--config` command line option to point at your
configuration file.

## Watching and unwatching volumes

### Start watching a volume

In order to enable automatic snapshots, you need to start watching the volume.
The following command will add `vol-13245678` to the watchlist with snapshots
created daily.

    automated-ebs-snapshots --config ~/auto-ebs-snapshots.conf --watch vol-12345678 --interval daily

### List watched volumes

List the currently watched volumes and their backup interval

    automated-ebs-snapshots --config ~/auto-ebs-snapshots.conf --list

### Stop watching a volume

To stop creating automated backups for a volume, run this:

    automated-ebs-snapshots --config ~/auto-ebs-snapshots.conf --unwatch vol-12345678

## Creating snapshots

Now, to start taking snapshots you will need to have Automated EBS Snapshots
running in the background.

    automated-ebs-snapshots --config ~/auto-ebs-snapshots.conf --run

It will check if there are any volumes with no or too old snapshots. New
snapshots will be created if needed.

## Author

This project is maintained by [Sebastian Dahlgren](http://www.sebastiandahlgren.se) and it is supported by [Skymill Solutions](http://www.skymillsolutions.com).

## License

The MIT License (MIT)

Copyright (c) 2014 Sebastian Dahlgren, Skymill Solutions

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
