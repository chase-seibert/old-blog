---
layout: post
title: Getting Started with AWS Device Farm and Python Appium
tags:
---

[AWS Device Farm](https://aws.amazon.com/device-farm) is a service for running
mobile app integration tests against a suite of physical devices. The
Amazon [documentation](http://boto3.readthedocs.io/en/latest/reference/services/devicefarm.html)
is exhaustive, and they support many different API clients.
However, the documentation does not have a quick start example for thing most
people are going to want to do first: run a test. Here is some working code
using the Python `boto3` client.


# Setup

First, you will want to create a Python virtual environment for this and install
some dependencies. Feel free to omit the versions numbers, but I've tested the
script against these versions.

```bash
virtualenv venv
. venv/bin/activate
pip install boto3==1.4.4 requests==2.13.0
```


# Pre-requisites

This script assumes you have already built an APK file for your mobile
app, and that you have bundled your Appium Python tests in a zip file as
per the [Amazon Appium Python documentation](http://docs.aws.amazon.com/devicefarm/latest/developerguide/test-types-android-appium-python.html).

Need to write your first tests? I have a [Appium Python Quickstart](http://chase-seibert.github.io/blog/2017/01/06/appium-react-native-quickstart.html),
too.

*Note: for the bundled Appium tests, make sure to do the wheel step on a Linux
 x86_64 vm.*

Also, you need to be authenticated to AWS. The easiest method is to generate an
API key and secret for your user in the AWS web console, and run `aws configure`
via the AWS [Command line interface](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html).


# Running the Test Suite

The script bellow will do the following:

1. Find the ID your AWS device farm project by name.
2. Find the ID of the pool of devices you want to use to test by name.
3. Upload a local Android APK file to AWS.
4. Upload a local zip file of your tests, requirements.txt and wheelhouse.
5. Start a test run.
6. Poll until the test run is completed.

```python
#!/usr/bin/env python
import logging
import pprint
import time

import boto3
import requests


REGION = 'us-west-2'
PROJECT_NAME = 'My Mobile App'
DEVICE_POOL_NAME = 'Top Devices'  # this is a default pool
RUN_TIMEOUT_SECONDS = 60 * 20
WEB_URL_TEMPLATE = 'https://us-west-2.console.aws.amazon.com/devicefarm/home#/projects/%s/runs/%s'


device_farm = boto3.client('devicefarm', region_name=REGION)
s3 = boto3.client('s3', region_name=REGION)
logger = logging.getLogger(__name__)


def get_project_arn(name):
    for project in device_farm.list_projects()['projects']:
        if project['name'] == name:
            return project['arn']
    raise KeyError('Could not find project %r' % name)


def get_device_pool(project_arn, name):
    for device_pool in device_farm.list_device_pools(arn=project_arn)['devicePools']:
        if device_pool['name'] == name:
            return device_pool['arn']
    raise KeyError('Could not find device pool %r' % name)


def _upload_presigned_url(url, file_path):
    with open(file_path) as fp:
        data = fp.read()
        result = requests.put(url, data=data, headers={'content-type': 'application/octet-stream'})
        assert result.status_code == 200


def create_upload(project_arn, upload_type, name, file_path):
    # name needs to be a file name like app-releaseProduction.apk, not "Android App"
    logger.info('Uploading %s %r' % (upload_type, file_path))
    result = device_farm.create_upload(
        projectArn=project_arn,
        name=name,
        type=upload_type,
        contentType='application/octet-stream',
    )
    upload = result['upload']
    _upload_presigned_url(upload['url'], file_path)
    return upload['arn']


def schedule_run(project_arn, name, device_pool_arn, app_arn, test_package_arn):
    logger.info('Scheduling test run %r' % name)
    result = device_farm.schedule_run(
        projectArn=project_arn,
        appArn=app_arn,
        devicePoolArn=device_pool_arn,
        name=name,
        test={
            'type': 'APPIUM_PYTHON',
            'testPackageArn': test_package_arn,
        }
    )
    run = result['run']
    return run['arn']


def _poll_until(method, arn, get_status_callable, success_statuses, timeout_seconds=10):
    check_every_seconds = 10 if timeout_seconds == RUN_TIMEOUT_SECONDS else 1
    start = time.time()
    while True:
        result = method(arn=arn)
        current_status = get_status_callable(result)
        if current_status in success_statuses:
            return result
        logger.info('Waiting for %r status %r to be in %r' % (arn, current_status, success_statuses))
        now = time.time()
        if now - start > timeout_seconds:
            raise StopIteration('Time out waiting for %r to be done' % arn)
        time.sleep(check_every_seconds)


def wait_for_upload(arn):
    return _poll_until(
        device_farm.get_upload,
        arn,
        get_status_callable=lambda x: x['upload']['status'],
        success_statuses=('SUCCEEDED', ),
    )


def wait_for_run(test_package_arn):
    result = _poll_until(
        device_farm.get_run,
        test_package_arn,
        get_status_callable=lambda x: x['run']['status'],
        success_statuses=('COMPLETED', ),
        timeout_seconds=RUN_TIMEOUT_SECONDS,
    )
    final_run = result['run']
    logger.info('Final run counts: %(counters)s' % final_run)
    return final_run['result'] == 'PASSED'


def get_run_web_url(project_arn, test_run_arn):
    # project_arn = arn:aws:devicefarm:us-west-2:foo:project:NEW-ARN-HERE
    # test_run_arn = arn:aws:devicefarm:us-west-2:foo:run:project-arn/NEW-ARN-HERE
    project_arn_id = project_arn.split(':')[6]
    test_run_arid = test_run_arn.split('/')[1]
    return WEB_URL_TEMPLATE % (
        project_arn_id,
        test_run_arid,
    )


if __name__ == '__main__':
    logging.basicConfig(format='%(message)s')
    logger.setLevel(logging.INFO)
    project_arn = get_project_arn(PROJECT_NAME)
    logger.info('Project: %r' % project_arn)
    device_pool_arn = get_device_pool(project_arn, DEVICE_POOL_NAME)
    logger.info('Device pool: %r' % device_pool_arn)
    app_arn = create_upload(
        project_arn,
        'ANDROID_APP',
        'my-app.apk',
        '/tmp/my-app.apk',
    )
    wait_for_upload(app_arn)
    logger.info('App: %s' % app_arn)
    test_package_arn = create_upload(
        project_arn,
        'APPIUM_PYTHON_TEST_PACKAGE',
        'test_bundle.zip',
        '/tmp/test_bundle.zip',
    )
    wait_for_upload(test_package_arn)
    logger.info('Test package: %s' % test_package_arn)
    test_run_arn = schedule_run(
        project_arn,
        name='Test Run 1',
        device_pool_arn=device_pool_arn,
        app_arn=app_arn,
        test_package_arn=test_package_arn,
    )
    logger.info('Scheduled test run %r' % test_run_arn)
    logger.info('View scheduled run at %s' % get_run_web_url(project_arn, test_run_arn))
    success = wait_for_run(test_run_arn)
    logger.info('Success')
```

The only tricky parts here are using the pre-signed URLs from the `create_upload`
step to make a subsequent `PUT` call with the file contents, and setting the
`ContentType` correctly for that to work. Also, we need to poll for both uploads
to be processed before we kick off the test run.
