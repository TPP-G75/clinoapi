# clinoapi
Web API for clinical notes analysis

## How to run
Run in the project's directory:
```
docker build -t clinoapi .
docker run -d --name test -p 8080:8080 clinoapi
```

Then go to [localhost:8080](http://localhost:8080)
