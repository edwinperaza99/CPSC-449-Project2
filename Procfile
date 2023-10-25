enrollments: uvicorn --port 0 api.enrollments:app
users: uvicorn --port 0 api.users:app
krakend: echo ./api/etc/krakend.json | entr -nrz krakend run --config ./api/etc/krakend.json
