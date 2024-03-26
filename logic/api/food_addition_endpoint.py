from Utils.json_reader import get_config_data


class FoodAdditionEndpoint:
    def __init__(self, api_object):
        self.my_api = api_object
        self.config = get_config_data()
        self.url = self.config['api_url'] + '/api/v1/foodobject'
        self.backend = self.config['backend_version']
        self.headers = self.config['api_cookie']

    def add_food_to_breakfast(self, food_api):
        body = {
            "eaten": False,
            "food": food_api,
            "meal": "/api/v1/meal/558981041/",
            "scaled_amount": 1,
            "units": 1,
            "user_chosen": True
        }
        response = self.my_api.api_post_request(url=f"{self.url}/?{self.config['backend_version']}", body=body, header=self.headers)
        # Check if the response was successful
        if response.status_code == 201:
            return response
        else:
            # Handle errors
            error_message = f"Failed to add food to breakfast: {response.status_code} {response.text}"
            # Log the error, raise an exception, or handle it as needed
            raise Exception(error_message)

    def remove_food_from_breakfast(self, food_id):
        print(f"{self.url}/{food_id}/?{self.config['backend_version']}")

        response = self.my_api.api_delete_request(url=f"{self.url}/{food_id}/?{self.config['backend_version']}", header=self.headers)
        # Check if the response was successful
        if response.status_code == 204:
            return response.status_code  # Or process the data as needed
        else:
            # Handle errors
            error_message = f"Failed to remove food from breakfast: {response.status_code} {response.text}"
            # Log the error, raise an exception, or handle it as needed
            raise Exception(error_message)