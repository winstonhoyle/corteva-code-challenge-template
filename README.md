# Code Challenge Template

#### Challengee:
Winston Hoyle

#### Time Spent
~2 hours

#### Comments
Input works but only when `bulk_upload` is disabled. If I worked on this longer I would fix bulk upload with new files. I would also implement storing results and unit tests. I only give myself ~2 hours per challenge. I have other code that is _production_, including an account I post daily maps:
* [VineMapper](https://github.com/winstonhoyle/VineMapper)
* [Mapping-WMATA-Fares](https://github.com/winstonhoyle/Mapping-WMATA-Fares) [http://wmatafares.com/](http://wmatafares.com/)
* [Sample-CRUD-app](https://github.com/winstonhoyle/Sample-CRUD-app)

## How to run

```
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
uvicorn src.app.main:app --reload
```

## Challenge Checklist:

### Problem 1 - Data Modeling
- [x] [Choose a database to use for this coding exercise (SQLite, Postgres, etc.)](src/app/database.py)
- [x] [Design a data model to represent the weather data records.](src/app/models.py)
- [x] [If you use an ORM, your answer should be in the form of that ORM's data definition format. If you use pure SQL, your answer should be in the form of DDL statements.](src/app/models.py)

### Problem 2 - Ingestion

- [x] [Write code to ingest the weather data from the raw text files supplied into your database, using the model you designed.](https://github.com/winstonhoyle/corteva-code-challenge-template/blob/main/src/app/main.py#L41)
- [ ] [Check for duplicates: if your code is run twice, you should not end up with multiple rows with the same data in your database.](https://github.com/winstonhoyle/corteva-code-challenge-template/blob/main/src/app/main.py#L41)
- [x] [Your code should also produce log output indicating start and end times and number of records ingested.](https://github.com/winstonhoyle/corteva-code-challenge-template/blob/main/src/app/main.py#L23)

### Problem 3 - Data Analysis

#### For every year, for every weather station, calculate:
- [x] [Average maximum temperature (in degrees Celsius)](https://github.com/winstonhoyle/corteva-code-challenge-template/blob/main/src/app/crud.py#L229)
- [x] [Average minimum temperature (in degrees Celsius)](https://github.com/winstonhoyle/corteva-code-challenge-template/blob/main/src/app/crud.py#L232)
- [x] [Total accumulated precipitation (in centimeters)](https://github.com/winstonhoyle/corteva-code-challenge-template/blob/main/src/app/crud.py#L238)
- [x] [Ignore missing data when calculating these statistics.](https://github.com/winstonhoyle/corteva-code-challenge-template/blob/main/src/app/main.py#L184)
- [ ] Design a new data model to store the results.
- [x] [Use NULL for statistics that cannot be calculated.](https://github.com/winstonhoyle/corteva-code-challenge-template/blob/main/src/app/main.py#L202)
- [x] [Your answer should include the new model definition as well as the code used to calculate the new values and store them in the database.](https://github.com/winstonhoyle/corteva-code-challenge-template/blob/main/src/app/schemas.py#L68)

### Problem 4 - REST API

- [x] [Choose a web framework (e.g. Flask, Django REST Framework). Create a REST API with the following GET endpoints](https://github.com/winstonhoyle/corteva-code-challenge-template/blob/main/src/app/schemas.py#L68)
#### Create a REST API with the following GET endpoints:
- [x] [/api/weather](https://github.com/winstonhoyle/corteva-code-challenge-template/blob/main/src/app/main.py#L116)
- [x] [/api/weather/stats](https://github.com/winstonhoyle/corteva-code-challenge-template/blob/main/src/app/main.py#L209)
- [x] [Both](https://github.com/winstonhoyle/corteva-code-challenge-template/blob/main/src/app/main.py#L262) [endpoints](https://github.com/winstonhoyle/corteva-code-challenge-template/blob/main/src/app/main.py#L145) should return a JSON-formatted response with a representation of the ingested/calculated data in your database.
- [x] [Allow clients to filter the response by date and station ID (where present) using the query string.](https://github.com/winstonhoyle/corteva-code-challenge-template/blob/main/src/app/main.py#L121) [Data should be paginated.](https://github.com/winstonhoyle/corteva-code-challenge-template/blob/main/src/app/main.py#L145)
- [x] Include a Swagger/OpenAPI endpoint that provides automatic documentation of your API.
- [x] [Your answer should include all files necessary to run your API locally](https://github.com/winstonhoyle/corteva-code-challenge-template/blob/main/src/app/main.py#L19)
- [ ]along with any unit tests.

### Extra Credit - Deployment
- [ ] (Optional.) Assume you are asked to get your code running in the cloud using AWS. What tools and AWS services would you use to deploy the API, database, and a scheduled version of your data ingestion code? Write up a description of your approach.