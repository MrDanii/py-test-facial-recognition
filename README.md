### Quick Start with Docker
1. Clone Repository
2. Create Docker containers:
```
docker compose -f docker-compose.yml up --build
```

### Development Environment

#### 1. Creating Project
1. Intalling virtual environment
```
pip3 install virtualenv
```

2. Create virtual environment in your project directory (this creates a folder called venv)
``` 
virtualenv venv 
```

3. activate virtual envrionment
```
# Windows: 
.\venv\Scripts\activate
# Unix or macOS:
source venv/bin/activate
```

#### 2. Set up Flask Server
1. Create requirements.txt file with following content
```
flask
requests
```
2. Install dependencies
```
pip install -r requirements.txt
```
3. Install face_recognition_models
```
pip install git+https://github.com/ageitgey/face_recognition_models
```

#### 3. Test the Microservice
1. Run Microservice with following command
```
flask --app services/products run
```
- This makes the server publicly available ``` --host=0.0.0.0 ```
  - Example: ``` flask --app services/products run --host=0.0.0.0 ```
- As a shortcut, if the file is named app.py or wsgi.py, you don’t have to use --app
- to enable debugging we use the option **--debug**
``` 
flask run --host=0.0.0.0 --debug
```

#### Notes about Libraries
https://cmake.org/download/
not sure why do i need cmake (sad face)
but it gives error when intalling "face-recognition" python library
