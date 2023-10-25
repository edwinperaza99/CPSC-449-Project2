enrollments: uvicorn --port $PORT api.enrollments:app
users: uvicorn --port $PORT api.users:app
krakend: echo ./api/etc/krakend.json | entr -nrz krakend run --config ./api/etc/krakend.json
