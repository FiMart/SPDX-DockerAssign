## Command to Run Docker-Compose

### Run using flask API
`python app/app.py`

### Build Docker-Compose spdx/api 
`docker build -t sdpx/api ./api`

### Pull MySQL to Use
`docker pull mysql:5.7`

### Pull MySQL to Use for spdx/db
`docker tag mysql:5.7 sdpx/db`

### Merge Docker Compose between spdx/api and spdx/db
`docker-compose -f compose.yaml up`


