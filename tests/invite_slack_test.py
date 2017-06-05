import unittest
import os
import json
from httmock import urlmatch, HTTMock

from invite_slack import handler


event = json.dumps({
    'email': 'yuri.gagarin@gmail.com',
    'first_name': 'Yuri',
    'last_name': 'Gagarin'
})

context = json.dumps({})


class InviteSlackTest(unittest.TestCase):
    def test_handler_no_env(self):
        res = handler.endpoint(event, context)

        self.assertEqual(res['statusCode'], 500)

    def test_handler_bad_input(self):
        # TODO: pass strings, as event comes as string!
        res = handler.endpoint("unformatted {} json", context)

        self.assertEqual(res['statusCode'], 400)

    def test_handler_ok(self):
        os.environ['SLACK_TOKEN'] = 'xxxx-111111100111-111111111111-111000111000-111eeeaa11'
        os.environ['CHANNEL_IDS'] = ""
        os.environ['SLACK_TEAM'] = "my-team"

        # @all_requests
        @urlmatch(netloc=r'(.*\.)?slack\.com$')
        def slack_ok_mock(url, request):
            return '{"ok": true}'

        with HTTMock(slack_ok_mock):
            res = handler.endpoint(event, context)
        self.assertEqual(res['statusCode'], 200)
