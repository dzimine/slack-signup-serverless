import unittest
import mock
import os
from httmock import all_requests, HTTMock

from record_ac import handler


event = {
    'email': 'dmitri.zimine+yuri.gagarin1@gmail.com',
    'first_name': 'Yuri',
    'last_name': 'Gagarin'
}

context = {}

env = {
    'URL': 'https://stackstorm.api-usa.com',
    'API_KEY': '9042624c1641a25936c93fa2fae9986f8b1af950de876485c785dbdb75f0b9af01fc08f4'
}


class RecordACTest(unittest.TestCase):
    def test_handler_no_env(self):
        with self.assertRaises(KeyError):
            handler.endpoint(event, context)

    def test_handler_bad_input(self):
        with self.assertRaises(ValueError):
            handler.endpoint("misformatted {} json", context)

    @all_requests
    @mock.patch.dict(os.environ, env)
    def test_handler_ok(self):
        def ok_mock(url, request):
            return ('{"subscriber_id":5970,"sendlast_should":0,"sendlast_did":0,'
                    '"result_code":1,"result_message":"Contact updated","result_output":"json"}')

        with HTTMock(ok_mock):
            res = handler.endpoint(event, context)
        self.assertEqual(res['statusCode'], 200)
        print res

    @all_requests
    @mock.patch.dict(os.environ, env)
    def test_handler_not_auth(self):
        def ok_mock(url, request):
            return ('{"subscriber_id":5970,"sendlast_should":0,"sendlast_did":0,'
                    '"result_code":0,"result_message":"Not authorized...","result_output":"json"}')

        with HTTMock(ok_mock):
            with self.assertRaises(Exception) as c:
                handler.endpoint(event, context)

        self.assertTrue('Failed' in str(c.exception))
