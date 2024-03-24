from Utils.json_reader import get_config_data


class SearchFoodEndpoint:
    def __init__(self, api_object):
        self.my_api = api_object
        self.config = get_config_data()
        self.url = self.config['api_url']+"/g/search/?limit=40"
        self.backend = self.config['backend_version']
        self.headers = self.config['api_cookie']

    def search_by_cals(self, min_cals,max_cals):
        response = self.my_api.api_get_request(url=f"{self.url}&min_calories={min_cals}&max_calories={max_cals}&{self.backend}", header=self.headers)
        # Check if the response was successful
        if response.status_code == 200:
            return response
        else:
            # Handle errors
            error_message = f"Failed to create nutritional target: {response.status_code} {response.text}"
            # Log the error, raise an exception, or handle it as needed
            raise Exception(error_message)

    def search_by_name(self, food_name):
        response = self.my_api.api_get_request(url=f"{self.url}&q={food_name}&{self.backend}", header=self.headers)
        # Check if the response was successful
        if response.status_code == 200:
            return response
        else:
            # Handle errors
            error_message = f"Failed to create nutritional target: {response.status_code} {response.text}"
            # Log the error, raise an exception, or handle it as needed
            raise Exception(error_message)
