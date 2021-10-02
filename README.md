# Leclerc Order parser

Small project which analyses the HTML page of an order on the Leclerc Chez Moi service, and
generates a CSV with all the products and relevant information from the page.

## Installation

This project uses Poetry as the package manager, to install the dependencies, simply run:

```bash
poetry install
```

## Running the Python program

The program accepts command line arguments, you can run this to get details on the necessary arguments:

```bash
poetry run python -m leclerc-parser --help
```

## Uploading the data to Google

There is a google sheet with a custom action which is designed to ingest the CSV files this program creates.
In order to use it, the CSV file needs to be uploaded to Google Drive. You then only need to pass the name of the CSV file to the app script to load the contents of the order into a new page of the Google Sheet.
