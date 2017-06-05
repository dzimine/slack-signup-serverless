import json
import datetime


def endpoint(event, context):
    print "event={}, context={}".format(event, context)

    current_time = datetime.datetime.now().time()
    body = {
        "event": str(event),
        "context": str(context),
        "time": str(current_time)
    }

    response = {
        "statusCode": 200,
        "body": json.dumps(body)
    }
    return response


if __name__ == '__main__':
    # Poor man's testing

    test_event = {
        'email': 'dmitri.zimine+gagarin@gmail.com',
        'first_name': 'Yuri',
        'last_name': 'Gagarin'
    }

    test_context = {}

    print endpoint(test_event, test_context)
