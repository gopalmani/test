# Swag Labs Automated Testing

This repository contains automated tests for the Swag Labs web application using Selenium WebDriver and Python. The tests cover login functionality, item sorting, adding items to the cart, and placing orders.

## Table of Contents

- [Features](#features)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
- [Usage](#usage)
- [Test Structure](#test-structure)
- [Contributing](#contributing)
- [License](#license)

## Features

- **Login Validations:** Verify successful login and logout for various user types.
- **Items Sort Order Validations:** Verify default sort order and the ability to change the sort order.
- **Add Items to Cart and Complete Order:** Verify items are retained in the cart after logout and test the order placement process.

## Prerequisites

To run the automated tests, ensure you have the following installed:

- [Python](https://www.python.org/downloads/)
- [Selenium WebDriver](https://www.selenium.dev/downloads/)
- [Chrome WebDriver](https://sites.google.com/a/chromium.org/chromedriver/)

## Setup

1. Clone this repository to your local machine.
2. Install the necessary Python packages using pip:

```bash
pip install -r requirements.txt
