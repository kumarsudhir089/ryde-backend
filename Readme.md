# Ryde Backend

## Setup Instructions

### 1. Create a Virtual Environment

```sh
python3 -m venv venv
```

### 2. Activate the Virtual Environment
```sh
source venv/bin/activate
```

### 3. Install the dependecies(make sure your venv is activated before you do this)
```sh
pip install -r requirements.txt
```

### 4. create .env file in project root and copy paste this content, make sure to provide there values before running the server
```sh
MONGO_URL=<mongo-url>
AUTH_SECRET=<secret>
ALGORITHM=<algorithm>
```


### 5. If the above steps are complete, We can spin up the server using below command:
```sh
uvicorn app.main:app --reload
```

Server will start at `8000` port


### 6. For documentation please visit:
```sh
http://localhost:8000/docs
```