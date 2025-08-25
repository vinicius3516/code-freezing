import datetime
import logging
import sys
import os


import yaml


CONFIG_FILE = 'config.yaml'
GITHUB_ACTOR = os.getenv('GITHUB_ACTOR')


logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def get_config(filename: str) -> dict: 
    with open(filename) as f:
        return yaml.safe_load(f)
    

def is_user_in_bypass_group(user: str, bypass_group: list) -> bool:
    return user in bypass_group
 

def is_today_in_freezing_period(date_from, date_to) -> bool:
    now = datetime.date.today()
    return now >= date_from and now <= date_to

   
def unpack_config(config: dict) -> tuple:
    try:       
        bypass_group = config['bypass_group']
        freezing_dates = config['freezing_dates']
    except KeyError:
        logging.error(f"One of the fields are not present : 'bypass_group' or 'freezing_dates' on config file {CONFIG_FILE}")
        sys.exit(1)
    return (bypass_group, freezing_dates)


def main():
    config = get_config(CONFIG_FILE)
    bypass_group, freezing_dates = unpack_config(config)


    if is_user_in_bypass_group(GITHUB_ACTOR, bypass_group):
        logging.info(f"User {GITHUB_ACTOR} is in the bypass group, skipping code freezing.")
        sys.exit(0)

    else:
        for period, dates in freezing_dates.items():
            from_date = dates.get('from')
            to_date = dates.get('to')

            
            if is_today_in_freezing_period(from_date, to_date):
                logging.warning(f"The current date falls under the '{period}', blocked due to code freezing period.")
                sys.exit(1)

if __name__ == '__main__':
    main()