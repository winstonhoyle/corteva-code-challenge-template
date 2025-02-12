# Code Challenge Template

## Challenge Checklist:

### Problem 1 - Data Modeling
- [x] [Choose a database to use for this coding exercise (SQLite, Postgres, etc.)](src/app/database.py)
- [x] [Design a data model to represent the weather data records.](src/app/models.py)
- [x] [If you use an ORM, your answer should be in the form of that ORM's data definition format. If you use pure SQL, your answer should be in the form of DDL statements.](src/app/models.py)

### Problem 2 - Ingestion

- [x] Write code to ingest the weather data from the raw text files supplied into your database, using the model you designed.
- [ ] Check for duplicates: if your code is run twice, you should not end up with multiple rows with the same data in your database.
- [x] Your code should also produce log output indicating start and end times and number of records ingested.

### Problem 3 - Data Analysis

#### For every year, for every weather station, calculate:
- [x] Average maximum temperature (in degrees Celsius)
- [x] Average minimum temperature (in degrees Celsius)
- [x] Total accumulated precipitation (in centimeters)
- [x] Ignore missing data when calculating these statistics.
- [ ] Design a new data model to store the results.
- [ ] Use NULL for statistics that cannot be calculated.
- [ ] Your answer should include the new model definition as well as the code used to calculate the new values and store them in the database.

### Problem 4 - REST API

- [x] Choose a web framework (e.g. Flask, Django REST Framework). Create a REST API with the following GET endpoints
#### Create a REST API with the following GET endpoints:
- [ ] /api/weather
- [ ] /api/weather/stats
- [ ] Both endpoints should return a JSON-formatted response with a representation of the ingested/calculated data in your database.
- [ ] Allow clients to filter the response by date and station ID (where present) using the query string. Data should be paginated.
- [x] Include a Swagger/OpenAPI endpoint that provides automatic documentation of your API.
- [ ] ~~Your answer should include all files necessary to run your API locally, along with any unit tests.~~

### Extra Credit - Deployment
- [ ] ~~(Optional.) Assume you are asked to get your code running in the cloud using AWS. What tools and AWS services would you use to deploy the API, database, and a scheduled version of your data ingestion code? Write up a description of your approach.~~