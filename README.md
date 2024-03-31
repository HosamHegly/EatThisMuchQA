# EatThisMuch Selenium Grid Automation Testing
Overview
This project provides a comprehensive automation testing framework for the EatThisMuch web application using Selenium Grid. Designed with the Page Object Model (POM) pattern, the framework aims to facilitate the creation, maintenance, and readability of test scripts. The project is structured into four main sections: Infrastructure, Logic, Tests, and Utils, along with a configuration file that offers flexible test execution options.

## Features
Selenium Grid Integration: Leverages Selenium Grid for running tests on multiple browsers and platforms simultaneously.
Page Object Model (POM): Implements POM for efficient test case management and to minimize code duplication.
Configurable Test Execution: Users can customize test runs in terms of browser choice, platform, and execution mode (parallel or serial).
Support for Multiple Browsers: Configurations allow for testing across different web browsers, enhancing cross-browser compatibility checks.
## Project Structure
Infrastructure: Contains the setup for Selenium WebDriver and Grid, including driver initialization and grid configuration.
Logic: Holds the business logic for interacting with the web application, abstracting complex actions into reusable methods.
Tests: Comprises test cases written using the POM to interact with the web application through the methods defined in the Logic section.
Utils: Includes utility functions and helpers that support test execution, such as data generators or custom wait methods.
config.json: A configuration file that allows users to specify browsers, platforms, and other test run preferences.

## Getting Started
### Prerequisites
Java (for Selenium Grid)
Python 3.6 or higher
Selenium WebDriver
A running instance of Selenium Grid

### Setup
Clone the repository:

* git clone https://github.com/HosamHegly/EatThisMuch_SeleniumGrid_Automation_Testing.git

* Install required Python packages:

* pip install -r requirements.txt

* Ensure Selenium Grid is up and running. For instructions on setting up Selenium Grid, visit Selenium's official documentation.

### Configuration
* Edit the config.json file to specify your desired testing environment. Available options include:
  
* browser: The web browser to use for tests (e.g., "chrome", "firefox").
  
* platform: The operating system platform (e.g., "WINDOWS", "LINUX").

* execution_mode: Run tests in "parallel" or "serial".

* driver: Choose between "grid" for Selenium Grid or "regular" for local WebDriver.

### Running Tests
To execute tests, run the following command from the project Test directory:

<img width="207" alt="image" src="https://github.com/HosamHegly/EatThisMuch_SeleniumGrid_Automation_Testing/assets/57544654/7da7716f-814d-40bd-8a54-58babf9941c0">

hih
