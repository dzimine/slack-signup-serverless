#!/usr/bin/python
import sys
import os

# Import installed packages (in site-packages)
site_pkgs = os.path.join(os.path.dirname(os.path.realpath(__file__)), "site-packages")
sys.path.append(site_pkgs)

import urllib
import json
import requests


def endpoint(event, context):

    try:
        if isinstance(event, basestring):
            event = json.loads(event)

        print("Received event: " + json.dumps(event, indent=2))

        TOKEN = os.environ['SLACK_TOKEN']
        CHANNEL_IDS = os.environ.get('CHANNEL_IDS', '')
        TEAM = os.environ['SLACK_TEAM']
    except KeyError:
        failure = "ERROR: Environment variables SLACK_TOKEN and SLACK_TEAM must be set."
        print failure
        raise KeyError(failure)
    except ValueError as e:
        failure = "ERROR: Can not parse `event`: '{}'\n{}".format(str(event), str(e))
        print failure
        raise ValueError(failure)
    invite(event.get('email'),
           token=TOKEN,
           team=TEAM,
           first_name=event.get('first_name'),
           last_name=event.get('last_name', ''),
           channel_ids=CHANNEL_IDS)
    return {
        "statusCode": 200,
        "body": "Invite sent"
    }


def invite(email, token, team, first_name, last_name,
           channel_ids=[], set_active=True, resend=True):
    """
        Invite a new user to slack organization.

        Part of Slack undocumented API, documented here:
        https://github.com/ErikKalkoken/slackApiDoc/blob/master/users.admin.invite.md
    """

    url = "https://%s.slack.com/api/users.admin.invite" % team
    headers = {}
    headers['Content-Type'] = 'application/x-www-form-urlencoded'
    body = {
        'email': email.encode('utf-8'),
        'channels': ",".join(channel_ids),
        'token': token,
        'set_active': set_active,
        'resend': resend,
        '_attempts': 1
    }
    if first_name is not None:
        body['first_name'] = first_name.encode('utf-8')

    data = urllib.urlencode(body)
    response = requests.get(url=url,
                            headers=headers, params=data)
    results = response.json()

    if results['ok'] is True:
        print "Invite successfully sent to %s. RESPONSE: %s" % \
            (email, results)
    else:
        failure_reason = ('Failed to send invite to %s: %s \
                          (status code: %s)' % (email, response.text,
                          response.status_code))
        print failure_reason
        raise Exception(failure_reason)
