# Steps to build and run this docker application

- Open the command line and `cd` into the parent directory.
- Ensure docker is running.
- Execute `docker build -t task-clarity-frontend .`
  - It will download all the required dependencies and build the angular application. It will take some time.
- Execute `docker run -d --rm -p 8080:8080 --name ng-app task-clarity-frontend`
- Open browser and navigate to http://localhost:8080/
- You should see the study instruction page. If the backend application is running locally, then you can start using it.
