import unittest
import os
from httmock import urlmatch, HTTMock

from invite_slack import handler


event = {
    'email': 'yuri.gagarin@gmail.com',
    'first_name': 'Yuri',
    'last_name': 'Gagarin'
}

context = {}


class InviteSlackTest(unittest.TestCase):
    def test_handler_no_env(self):
        with self.assertRaises(KeyError) as e:
            handler.endpoint(event, context)
        self.assertTrue('ERROR: Environment variables' in str(e.exception))

    def test_handler_bad_input(self):
        with self.assertRaises(ValueError) as e:
            handler.endpoint("unformatted {} json", context)
        self.assertTrue('ERROR: Can not parse' in str(e.exception))

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
