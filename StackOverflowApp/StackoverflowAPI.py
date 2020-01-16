import requests
import datetime
from ratelimit import limits

BASEURL = "https://api.stackexchange.com/2.2/search/advanced"

PER_MIN_SEARCHES = 5
PER_DAY_SEARCHES = 100
SESSION_MINUTES = 1 * 60
SESSION_DAY_MINUTES = 24 * 60 * 60


@limits(calls=PER_MIN_SEARCHES, period=SESSION_MINUTES)
@limits(calls=PER_DAY_SEARCHES, period=SESSION_DAY_MINUTES)
def get_questions(params):
    params = {k: v for k, v in params.items() if v != '' and v is not None}
    params['site'] = 'stackoverflow'
    print('Calling API')
    r = requests.get(BASEURL, params=params)
    if 'items' not in r.json():
        print(r.json)
        return r.json()
    op = r.json()['items']
    output_dict = {}
    for i in range(len(op)):
        inner_dict = {}
        key = op[i]['question_id']
        output_dict[key] = inner_dict
        inner_dict['link'] = op[i]['link']
        inner_dict['title'] = op[i]['title']
        inner_dict['created_by'] = op[i]['owner']['display_name']
        if 'profile_image' in op[i]['owner']:
            inner_dict['image'] = op[i]['owner']['profile_image']
        else:
            inner_dict['image'] = None
    return output_dict


def dateConverter(input_date):
    if input_date is None:
        return None
    input_date = datetime.datetime.combine(input_date, datetime.time.min)
    timestamp = (input_date - datetime.datetime(1970, 1, 1)).total_seconds()
    return int(timestamp)