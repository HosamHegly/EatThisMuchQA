from Utils.json_reader import get_config_data


class NutritionalTargetEndPoint:
    def __init__(self, api_object):
        self.my_api = api_object
        self.config = get_config_data()
        self.url = self.config['api_url'] + '/api/v1/nutritionprofile'
        self.backend = self.config['backend_version']
        self.headers = self.config['api_cookie']

    def create_nutritional_target(self, body=None):
        response = self.my_api.api_post_request(url=f"{self.url}/?{self.backend}", body=body, header=self.headers)
        # Check if the response was successful
        if response.status_code == 201:
            # Parse the response data
            return response  # Or process the data as needed
        else:
            # Handle errors
            error_message = f"Failed to create nutritional target: {response.status_code} {response.text}"
            # Log the error, raise an exception, or handle it as needed
            raise Exception(error_message)

    def delete_nutritional_target(self, target_id):
        response = self.my_api.api_delete_request(url=f"{self.url}/{target_id}/?{self.backend}", header=self.headers)
        # Check if the response was successful
        if response.status_code == 204:
            return response.status_code  # Or process the data as needed
        else:
            # Handle errors
            error_message = f"Failed to delete nutritional target: {response.status_code}"
            # Log the error, raise an exception, or handle it as needed
            raise Exception(error_message)
