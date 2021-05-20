import json
import urllib3

def handler(event, context):
    records = event.get('Records')
    emails = []
    
    http = urllib3.PoolManager()
    
    for record in records:
        emails.append(
            sendmail(
                http=http,
                data=json.loads(record.get('body'))
            )
        )
    
    return {
        'success': len(records) == len(emails),
        'event': emails
    }
    
def sendmail(http, data):
    headers = urllib3.make_headers(basic_auth='api:{}'.format(data.get('api_key')))
    
    request = http.request(
        'POST',
        data.get('endpoint'),
        headers=headers,
        fields={
            'from': data.get('from'),
            'to': data.get('to'),
            'subject': data.get('subject'),
            'template': data.get('template') or 'blank-testing',
            'h:X-Mailgun-Variables': json.dumps(data.get('params'))
        }
    )

    respone = json.loads(
        request.data.decode('utf-8')
    )

    if request.status == 200:
        print(response)
    
    return response