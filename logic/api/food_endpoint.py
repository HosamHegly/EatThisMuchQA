from Utils.json_reader import get_config_data


class FoodEndPoint:
    def __init__(self, api_object):
        self.my_api = api_object
        self.config = get_config_data()
        self.url = self.config['api_url']
        self.backend = self.config['backend_version']
        self.headers = self.config['api_cookie']

    def get_food_details(self, food_api):

        response = self.my_api.api_get_request(url=f"{self.url}{food_api}?{self.backend}", header=self.headers)
        # Check if the response was successful
        if response.status_code == 200:
            # Parse the response data
            return response  # Or process the data as needed
        else:
            # Handle errors
            error_message = f"Failed to create nutritional target: {response.status_code} {response.text}"
            # Log the error, raise an exception, or handle it as needed
            raise Exception(error_message)
