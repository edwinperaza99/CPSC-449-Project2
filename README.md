# CPSC-449 Project 2

Users authentication service with read replication and load balancing thorugh an API gateway

## Project Members

- Edwin Peraza
- Harin Khalkhi
- Daniel Truong
- Anurag Ganji
- Arjit Saxena
- Chase Walsh

## GitHub Repository

You can find the project's source code and documentation on our GitHub repository:

[CPSC-449 Project 2 Repository](https://github.com/edwinperaza99/CPSC-449-Project2)

## Getting started

### Prerequisites

- Tuffix (Ubuntu Linux)
- Python (version 3.10.12)
- Foreman
- KrakenD

### Setup

Initialize virtual environment and install requirements. Run command:

```
make
```

### Running API

Use the following command to start the project using foreman and the specified process formation:

```
foreman start --formation "enrollments=3, users-primary=1, users-secondary-1=1, users-secondary-2=1, krakend=1"
```

- `enrollments=3`: This starts three instances of the `enrollments` service.
- `users-primary=1`: This starts one instance of the `users-primary` process which is the write database.
- `users-secondary-1=1`: This starts one instance of the `users-secondary-1` process which is a replica of `users-primary` for read only.
- `users-secondary-2=1`: This starts one instance of the `users-secondary-2` process which is a replica of `users-primary` for read only.
- `krakend=1`: This starts one instance of the `krakend` process.

### URLs and Ports

When using Foreman to manage your processes, the services will be available at the following URLs and ports:

- `enrollments.1`: [http://localhost:5000](http://localhost:5000)
- `enrollments.2`: [http://localhost:5001](http://localhost:5001)
- `enrollments.3`: [http://localhost:5002](http://localhost:5002)
- `users-primary`: [http://localhost:5100](http://localhost:5100)
- `krakend`: [http://localhost:8080](http://localhost:8080)
