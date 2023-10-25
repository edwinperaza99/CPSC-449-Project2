enrollments: uvicorn --port $PORT api.enrollments:app
users-primary: ./api/bin/litefs mount -config api/etc/primary.yml
users-secondary-1: ./api/bin/litefs mount -config api/etc/secondary-1.yml
users-secondary-2: ./api/bin/litefs mount -config api/etc/secondary-2.yml
krakend: echo ./api/etc/krakend.json | entr -nrz krakend run --config ./api/etc/krakend.json
