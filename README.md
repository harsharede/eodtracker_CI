# EOD Tracker
## _Implementing CI/CD using Azure DevOps & Azure Webapp_

This project contains code for a web service that tracks end of day (EOD) stock data for a given symbol/Ticker. It uses the [Marketstack API](http://api.marketstack.com/v1/) to retrieve stock data and stores it in a database. It also provides an endpoint for clients to query the live and stored data.


## Prerequisites
Before you begin, ensure you have the following:
- A local development environment with Git, Python, Virtual env, Docker (for local testing) and the necessary libraries installed (such as Flask and SQLAlchemy)
- An API key for the [Marketstack API](http://api.marketstack.com/v1/)
- Azure DevOps and Azure cloud Account.
- A PostgreSQL database set up to store the EOD and user data.
- And Azure resources like ACR (Azure container registry), APP service plan and web app.


## Endpoints
The following endpoints are available:

> POST /register
Registers a new user and generates an access token.

+ Request Body
    + username: string
    + password: string
+ Response
    + access_token: string

>POST /login
Logs in an existing user and generates an access token.

+ Request Body
    + username: string
    + password: string
+ Response
    + access_token: string

> GET /eod: 

A GET request to this endpoint retrieves EOD data for a given stock symbol and date range. Query parameters include symbol, from_date, and to_date. The from_date and to_date parameters should be in the format YYYY-MM-DD. An auth_key parameter should be included for authentication.

+ ## Request

    | Parameters | Required |Description |
    | ------ | ------ |------ |
    | symbol | Yes | stock symbols (tickers) for your request, e.g. AAPL, MSFT.  |
    | from_date | No |Filter results based on a specific timeframe by passing a from-date in YYYY-MM-DD format..  |
    | to_date | No | Filter results based on a specific timeframe by passing a from-date in YYYY-MM-DD format.  |
    | Authorization(Bearer) | Yes | Access token generated during user registration process should be used  |
+ ## Response(JSON)
    ```JSON
    {
        "data": [
            {
                "close": 176.65,
                "date": "2022-12-30T00:00:00+0000",
                "high": 177.77,
                "low": 175.4,
                "open": 177.49,
                "symbol": "JNJ",
                "volume": 4216656.0
            },
            {
                "close": 177.56,
                "date": "2022-12-29T00:00:00+0000",
                "high": 178.3,
                "low": 177.07,
                "open": 177.55,
                "symbol": "JNJ",
                "volume": 2828500.0
            },
            {
                "close": 176.66,
                "date": "2022-12-28T00:00:00+0000",
                "high": 178.45,
                "low": 176.65,
                "open": 177.76,
                "symbol": "JNJ",
                "volume": 2645400.0
            },
            {
                "close": 177.43,
                "date": "2022-12-27T00:00:00+0000",
                "high": 178.35,
                "low": 176.99,
                "open": 178.11,
                "symbol": "JNJ",
                "volume": 3066300.0
            }}
        
> GET /change-in-price:

A secondary API endpoint to calculate the change in price from X number of days, where X is provided by the user in the API request as num_days. This endpoint is not be available in production, i.e., is a part way through your deployment pipeline.
- Note: Difference calculation is only for the data of symbols available in only database. 
+ ## Request
    | Parameters | Required |Description |
    | ------ | ------ |------ |
    | symbol | Yes | stock symbols (tickers) for your request, e.g., AAPL, MSFT.  |

+ ## Response (Str)

## CI/CD implementation
----------
----------

## Continuous Integration 
_____________
## To setup & modify code on local environment, follow these steps:


## Fork this repository

+ Clone this repository to your local machine using git clone 
    ```
  git clone <git https url>
  ```

+    Create a new branch and checkout for your contribution.

    ```
    git checkout -b <branch name>

+ Make your changes and commit them using.
    ```
    git commit -am "Added XYZ functionality"
    ```
- Push the branch to your forked repository using git push origin my-contribution
    ```
    git push origin my-contribution
    ```
- Create a pull request from your forked repository to the original repository

## RUN Falsk setup 
- Navigate to the cloned repository
- Create a file called .env and add the following variables:
    + ACCESS_KEY: Your Alpha Vantage API key
    + DB_USERNAME: The username for your PostgreSQL database
    + DB_PASSWORD: The password for your PostgreSQL database
    + DB_SERVER: The server URL for your PostgreSQL database
- Run the command pip install -r requirements.txt to install the necessary libraries
    ```sh
    $ pip install -r requirements.txt`
- Expose app.py file
    ```sh
    export FLASK_APP=app.py`
- Run the command flask run to start the web service. Optional - Defining port and host will expose the webapp on local network.
    ```sh
    flask run --host=0.0.0.0 --port=80
    ```



## continuous delivery 
----
## Run/Trigger - Azure DevOps pipe line 
This Azure DevOps pipeline is used to build and deploy a Docker image on azure devops environment . The pipeline will be triggered when changes are made to the dev, release/*, or main branches.

The pipeline is used to run tasks like build docker image, push image to ACR and deploy image to Azure WebApp.

- The build task is used to build the Docker image and tag it with the build ID.
- The push task is then used to push the image to an Azure Container Registry.
- The Container Deploy: Prod task is used to deploy the Docker image to a web app in production. This task will only run if the changes are accepted and merged with main branch.
- The Container Deploy: Dev task is used to deploy the Docker image to a web app in development. This task will run for any commits to dev.



