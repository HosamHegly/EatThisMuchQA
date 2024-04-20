<p align="center">
    <img width="341" alt="image" src="https://github.com/HosamHegly/EatThisMuchQA/assets/57544654/97bd4e80-f358-4360-9f3a-d5f4ad75c060">
</p>
<p align="center">
    <h1 align="center">EATTHISMUCHQA</h1>
</p>
<p align="center">
    <em>API & UI Automation Project for EatThisMuch</em>
</p>
<p align="center">
	<img src="https://img.shields.io/github/license/HosamHegly/EatThisMuchQA?style=default&logo=opensourceinitiative&logoColor=white&color=orange" alt="license">
	<img src="https://img.shields.io/github/last-commit/HosamHegly/EatThisMuchQA?style=default&logo=git&logoColor=white&color=orange" alt="last-commit">
	<img src="https://img.shields.io/github/languages/top/HosamHegly/EatThisMuchQA?style=default&color=orange" alt="repo-top-language">
	
<p align="center">
	<!-- default option, no dependency badges. -->
</p>

<br><!-- TABLE OF CONTENTS -->
<details>
  <summary>Table of Contents</summary><br>

- [ Overview](#-overview)
- [ Features](#-features)
- [ Repository Structure](#-repository-structure)
- [ Getting Started](#-getting-started)
  - [ Installation](#-installation)
  - [ Usage](#-usage)
  - [ Tests](#-tests)
- [ Contributing](#-contributing)
- [ License](#-license)
- [ Acknowledgments](#-acknowledgments)
</details>
<hr>

##  Overview

The EatThisMuchQA project is designed to automate testing and ensure quality control for the EatThisMuch platform through API and UI automation. The project includes various scripts and testing frameworks to manage and execute tests efficiently. This enables faster development cycles and reliable application updates.

---

##  Features

##  Repository Structure

```sh
└── EatThisMuchQA/
    ├── infra
    │     ├── api_wrapper
    │     ├── ui_wrapper
    │     └── jira_client
    │
    ├ ── logic
    │     ├── ui_logic
    │     └── api_logic
    │   
    ├── tests
    │    ├── ui_tests
    │    └── api_tests
    │
    ├── config
    │     ├── json_reader.py
    │     ├── logging_setup.py
    │     ├── cookies.py
    │    └── helper_functions.py
    │
    ├── test_data
    └── Utils

```

---

##  Getting Started

**System Requirements:**

* **Python**: `version x.y.z`

###  Installation

<h4>From <code>source</code></h4>

> 1. Clone the Steam-Automation-Project repository:
>
> ```console
> $ git clone https://github.com/HosamHegly/EatThisMuchQA.git
> ```
>
> 2. Change to the project directory:
> ```console
> $ cd EatThisMuchQA
> ```
>
> 3. Install the dependencies:
> ```console
> $ pip install -r requirements.txt
> ```

###  Usage

> Run the test suite using the command below:
> ```console
> $ pytest
> ```

---

##  Contributing

Contributions are welcome! Here are several ways you can contribute:

- **[Report Issues](https://github.com/jameel978/Steam-Automation-Project/issues)**: Submit bugs found or log feature requests for the `Steam-Automation-Project` project.
- **[Submit Pull Requests](https://github.com/jameel978/Steam-Automation-Project/blob/main/CONTRIBUTING.md)**: Review open PRs, and submit your own PRs.
- **[Join the Discussions](https://github.com/jameel978/Steam-Automation-Project/discussions)**: Share your insights, provide feedback, or ask questions.

<details closed>
<summary>Contributing Guidelines</summary>

1. **Fork the Repository**: Start by forking the project repository to your github account.
2. **Clone Locally**: Clone the forked repository to your local machine using a git client.
   ```sh
   git clone https://github.com/HosamHegly/EatThisMuchQA.git
   ```
3. **Create a New Branch**: Always work on a new branch, giving it a descriptive name.
   ```sh
   git checkout -b new-feature-x
   ```
4. **Make Your Changes**: Develop and test your changes locally.
5. **Commit Your Changes**: Commit with a clear message describing your updates.
   ```sh
   git commit -m 'Implemented new feature x.'
   ```
6. **Push to github**: Push the changes to your forked repository.
   ```sh
   git push origin new-feature-x
   ```
7. **Submit a Pull Request**: Create a PR against the original project repository. Clearly describe the changes and their motivations.
8. **Review**: Once your PR is reviewed and approved, it will be merged into the main branch. Congratulations on your contribution!
</details>

<details closed>
<summary>Contributor Graph</summary>
<br>
<p align="center">
   <a href="https://github.com/HosamHegly/EatThisMuchQA/}graphs/contributors">
      <img src="https://contrib.rocks/image?repo=HosamHegly/EatThisMuchQA">
   </a>
</p>
</details>

---

##  License

This project is licensed under the [MIT License](LICENSE).

---


