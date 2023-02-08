# Steps to build and run this docker application

- Open the command line and `cd` into the parent directory.
- Ensure docker is running.
- Execute `docker-compose up`
  - It will download all the required the dependencies to build the flask application and install MySQL server.
  - It will take significant amount of time during the first run. In the subsequent runs, it will utilize the cache.
  - Once the flask app is running, navigate to http://localhost:5000/ to check the application status.
  - To check if the database is running and connected properly with the application, you can use the frontend application. If the frontend works correctly => DB is connected!
