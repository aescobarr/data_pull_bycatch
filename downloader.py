import requests
import json
from urllib.parse import urlencode, quote_plus
import settings

def auth():
    payload = {
        'grant_type' : 'password',
        'username': settings.api_credentials_user,
        'password': settings.api_credentials_password,
        'client_id': settings.api_credentials_client_id,
        'client_secret': settings.api_credentials_client_secret
    }
    auth_api_url = settings.api_auth_url + '?' + urlencode(payload)
    print('Authenticating to address {0}'.format(settings.api_auth_url))
    print('Making post request...')
    response = requests.post(auth_api_url)
    print('Server responded')
    if response.status_code == 200:
        print('Response successful! Returning auth data.')
        return json.loads(response.content.decode('utf-8'))
    else:
        print('Response not successful, code {0}'.format(response.status_code))
        return None


def get_project_observations(project_id, user_token):
    data = []
    endloop = False
    counter = 0
    while not endloop:
        page = counter + 1
        pagination_params = {
            'page': page
        }
        headers = {'Authorization': 'Bearer {0}'.format(user_token)}
        auth_observations_project = settings.api_base_url + '/observations/project/{0}.json'.format(project_id) + '?' + urlencode(pagination_params)
        response = requests.get(auth_observations_project, headers=headers)
        print("Obtaining page number " + str(page))
        if response.status_code == 200:
            print("Page " + str(page) + " obtained succesfully")
            counter = counter + 1
            pulled_data = json.loads(response.content.decode('utf-8'))
            if (len(pulled_data) == 0):
                print("Pulled no records, stopping download")
                endloop = True
            else:
                data = data + pulled_data
                print("Pulled 200 records, resuming download")
        else:
            print("Failed to obtain records from page " + str(page))
    return data