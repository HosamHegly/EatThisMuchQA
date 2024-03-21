from Utils.json_reader import get_config_data


class MealSettingsEndPoint:
    def __init__(self, api_object):
        self.my_api = api_object
        self.config = get_config_data()
        self.url = self.config['api_url'] + 'diet/137887039'
        self.backend = self.config['backend_version']
        self.headers = self.config['api_cookie']

    def change_nutritional_target(self,target_id,body=None):
        body = {"nutrition_profile":f"/api/v1/nutritionprofile/{target_id}/"}

        response = self.my_api.api_patch_request(url=self.url + self.backend, body=body, header=self.headers)
        # Check if the response was successful
        if response.status_code == 202:
            return response.status_code
        else:
            # Handle errors
            error_message = f"Failed to change nutritional target in settings: {response.status_code}"
            # Log the error, raise an exception, or handle it as needed
            raise Exception(error_message)
