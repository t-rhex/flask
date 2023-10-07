# Portfolio Development 

Development tech stack: Python Flask, HTML, CSS, JS
Deployment: Docker 

## Development 

Installing pyenv in MacOS -> https://www.freecodecamp.org/news/python-version-on-mac-update/
Virtualenv: https://www.freecodecamp.org/news/how-to-setup-virtual-environments-in-python/


## Deployment 

### Docker build 
https://blog.logrocket.com/build-deploy-flask-app-using-docker/

docker image build -t <image_name> .
e.g : docker image build -t andrew_portfolio .

docker run -p 5000:5000 -d <image_name>

### Served through portainer and reverse proxied by nginx proxy manager 


<img width="1122" alt="image" src="https://github.com/t-rhex/flask/assets/44456213/03f65d2f-5872-4853-aa12-1e32378dc986">
