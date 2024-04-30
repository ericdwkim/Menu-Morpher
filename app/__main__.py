import argparse
import os
import json
import logging
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from utils.get_ids import get_credentials, get_account_and_location_ids
from utils.logger_config import setup_logger
class App:

    SCOPES = ['https://www.googleapis.com/auth/business.manage']
    discovery_service_url = 'https://developers.google.com/static/my-business/samples/mybusiness_google_rest_v4p9.json'

    def __init__(self):
        setup_logger()
        self.credentials = get_credentials()
        self.account_id, self.location_id = get_account_and_location_ids()
        logging.info(f'\n--------------------------------------------\nAccount ID: {self.account_id}\nLocation ID: {self.location_id}\n--------------------------------------------\n')

        # Create GMB API service
        self.service = build(
            serviceName='mybusiness',
            version='v4',
            credentials=self.credentials,
            discoveryServiceUrl=self.discovery_service_url,
            cache_discovery=False
        )
        # Google identifier for your restaurant location to call updateFoodMenus()  with specific format
        self.food_menus_id = f'{self.account_id}/{self.location_id}/foodMenus'

    # GET request
    def download_food_menu(self):
        logging.info('Getting food menu...')
        food_menu = self.service.accounts().locations().getFoodMenus(
            name=self.food_menus_id
        ).execute()

        json.dump(food_menu, open('../food_menu.json', 'w', encoding='utf-8'), indent=4, ensure_ascii=False)

        if isinstance(food_menu, dict):
            logging.info('Successfully downloaded food menu!')
        else:
            logging.error('Failed to download food menu')

    # TODO - test getter & cmd flag
    def get_canHaveFoodMenus(self):
        logging.info('Checking `canHaveFoodMenus` flag in FoodMenus.Metadata object...')
        service_mbbi = build('mybusinessbusinessinformation', 'v1', credentials=self.credentials)

        location_metadata = service_mbbi.locations().get(
            name=self.location_id,
            readMask='metadata'
        ).execute()

        canHaveFoodMenus_flag = location_metadata['metadata']['canHaveFoodMenus']
        # if flag is true, inform user to proceed with jsons to menu.json to then update()
        if canHaveFoodMenus_flag:
            logging.info(f'Based on your location ID: "{self.location_id}", you can call update_food_menu via comamnd line flag `--update`\nEnsure that you\ve made all the appropriate changes to your menu.json prior to calling update.')
        else:
            logging.error(f'Based on your provided location ID: {self.location_id}, you will not be able to update food menus via updateFoodMenus API\ncanHaveFoodMenus_flag:{canHaveFoodMenus_flag}. See "https://developers.google.com/my-business/reference/rest/v4/accounts.locations" for more details')

    # PATCH request
    def update_food_menu(self):
        logging.info('Updating food menu...')
        with open('menu.json', 'r', encoding='utf-8') as file:
            food_menu_body = json.load(file)

        try:
            response = self.service.accounts().locations().updateFoodMenus(
                name=self.food_menus_id,
                body=food_menu_body
            ).execute()

            if isinstance(response, dict):
                logging.info('Successfully updated food menu!')
            else:
                logging.error('Failed to update food menu')
        except Exception:
            logging.exception('An error occurred while updating food menu')



if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='GMB API Python Client')
    parser.add_argument('--download', required=False, action='store_true', help='Downloads food menu via getFoodMenus API')
    parser.add_argument('--update', required=False, action='store_true', help='Updates food menu via updateFoodMenus API')
    args = parser.parse_args()

    app = App()
    if args.download:
        app.download_food_menu()
    if args.update:
        app.update_food_menu()
    # TODO: add new flag
    if args.canHaveFoodMenus:
        app.get_canHaveFoodMenus()
