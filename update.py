import requests
from tabulate import tabulate
from datetime import datetime
import json


API_DOMAIN = 'api.cuiiliste.de'
JSON_API_FILE = 'api/history/{date}.json'
LATEST_JSON_API_FILE = 'api/latest.json'


def update(json_block_list: list[dict[str, str]]) -> None:
    """
    Update the data in the BLOCKLIST.md file.
    :param json_block_list: The list of dictionaries containing the data.
    :return:
    """

    print('Updating data...')

    header = list(json_block_list[0].keys())
    header.insert(1, 'Check Link')

    rows = []
    for d in json_block_list:
        entry= tuple(d.values())

        domain = entry[0]

        check = f'[Check](https://{API_DOMAIN}/test_domain?domain={domain})'
        domain = f'[{domain}](https://{domain}/)'

        rows.append([domain, check, *entry[1:]])

    table = tabulate(rows, headers=header, tablefmt='pipe')

    with open('BLOCKLIST.md', 'w') as f:
        f.write(table)

    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    json_data = {
        'date': current_date,
        'list': json_block_list
    }

    formatted_json = json.dumps(json_data, indent=4)

    with open(JSON_API_FILE.format(date=current_date), 'w') as f:
        f.write(formatted_json)

    with open(LATEST_JSON_API_FILE, 'w') as f:
        f.write(formatted_json)

    print('Data updated!')


if __name__ == '__main__':
    update(json_block_list=requests.get(f'https://{API_DOMAIN}/blocked_domains').json())
