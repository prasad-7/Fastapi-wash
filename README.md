FASTAPI-WASH

__version__ = 0.1.0

This is an python-web API. It can be used to perform  authentication of the user.

The end point is secured with the JWT auth token , it validates the user before accessing certain endpoint. As the endpoint may store data into database for further process.

It schedules the given time of the user and check the availabiltiy of the time along with excluding the current appointment stored in the database.


It arrange slot according to the data provided by the admin, admin has the full access to the database. where as only users can do some sort of operations by authenticating the end point.


some endpoints doesnt need authentication as it is not arrested by Oauth2 it is pubically available.


Access the API : https://fastapi-wash.herokuapp.com/docs#/



![image](https://user-images.githubusercontent.com/91150388/199772966-a52349cb-0bb6-4f82-b23b-349b180429e4.png)

