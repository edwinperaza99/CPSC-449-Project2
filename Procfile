api: uvicorn --port $PORT api.__main__:app --reload
krakend: echo ./api/etc/krakend.json | entr -nrz krakend run --config ./api/etc/krakend.json
