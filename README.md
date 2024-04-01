

# EatThisMuch Selenium Grid Automation Testing

## Overview
This project provides a comprehensive automation testing framework for the EatThisMuch web application, utilizing Selenium Grid and the requests library. Designed around the Page Object Model (POM) pattern, it aims to improve the creation, maintenance, and readability of test scripts. The project is structured into Infrastructure, Logic, Tests, Utils, and a configuration file for flexible test execution.

## Features
- **Selenium Grid Integration**: Facilitates running tests across multiple browsers and platforms simultaneously.
- **Page Object Model (POM)**: Enhances test case management and reduces code duplication.
- **Configurable Test Execution**: Allows customization of test runs by browser, platform, and execution mode (parallel or serial).
- **Support for Multiple Browsers**: Ensures cross-browser compatibility.
- **Integration with Jira and Slack**: Automatically updates test statuses in Jira and sends notifications to Slack, enhancing team collaboration and project management.
- **Jenkins Pipeline**: Implements a CI/CD pipeline for automated test execution, making the testing process more efficient and scalable.

## Project Structure
- **Infrastructure**: Setup for Selenium WebDriver and requests framework, including driver initialization and grid configuration.
- **Logic**: Business logic for interacting with the web application, abstracting complex actions into reusable methods.
- **Tests**: API and UI test cases using POM to interact with the web application.
- **Utils**: Utility functions and helpers supporting test execution, such as data generators or custom wait methods.
- **config.json**: Configuration file to specify browsers, platforms, and other test run preferences.

## Getting Started

### Prerequisites
- Java (for Selenium Grid)
- Python 3.6 or higher
- Selenium WebDriver
- requests
- pytest
- A running instance of Selenium Grid

### Setup
1. Clone the repository: `git clone https://github.com/HosamHegly/EatThisMuchQA.git`
2. Install required Python packages: `pip install -r requirements.txt`
3. Ensure Selenium Grid is up and running. For setup instructions, visit Selenium's official documentation.

### Configuration
Edit the `config.json` file to specify your testing environment. Options include:
- `browser`: The web browser for tests (e.g., "chrome", "firefox").
- `platform`: The operating system platform (e.g., "WINDOWS", "LINUX").
- `execution_mode`: Run tests in "parallel" or "serial".
- `driver`: Choose "grid" for Selenium Grid or "regular" for local WebDriver.

## Running Tests
Execute test runner from the project Test directory:

<img width="650" alt="image" src="https://github.com/HosamHegly/EatThisMuchQA/assets/57544654/7b29044a-9772-427e-bbb9-44efd5844e48">

## Continuous Integration
- **Jenkins Pipeline**: A Jenkinsfile is included to define the pipeline for automated testing. Configure this in your Jenkins setup to run tests automatically on code push or at scheduled intervals.
- **Jira Integration**: Ensure your Jira project is connected via the API to update issues based on test outcomes.
- **Slack Notifications**: Configure Slack Webhooks to receive notifications about test runs, making it easier to track the progress and outcomes of testing.


## Jira snippets:

![Screenshot 2024-04-01 005126](https://github.com/HosamHegly/EatThisMuchQA/assets/57544654/1ff259da-47a7-4f56-a7d2-f2568090ab8a)


![Screenshot 2024-04-01 005158](https://github.com/HosamHegly/EatThisMuchQA/assets/57544654/ef5a9d0f-14c0-405c-b9ab-1b30be740ffd)


## Slack snippets:

<img width="497" alt="image" src="https://github.com/HosamHegly/EatThisMuchQA/assets/57544654/08ce9e4f-ddcb-444e-8799-bb7fd37b4d9a">

<img width="512" alt="image" src="https://github.com/HosamHegly/EatThisMuchQA/assets/57544654/f670745a-9f83-482e-907b-e174485c5d19">

## Jenkins Pipline snippets

<img width="1230" alt="image" src="https://github.com/HosamHegly/EatThisMuchQA/assets/57544654/a5e93e09-0519-4460-b81b-12a89314bf01">

## HTML Test Report

<img width="1246" alt="image" src="https://github.com/HosamHegly/EatThisMuchQA/assets/57544654/e05040a0-c5c8-45b6-9345-2ac752612639">





