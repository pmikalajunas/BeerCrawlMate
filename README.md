# Satalia Beer Test
<p align="center">
  <img src="https://i.ibb.co/BPkp6df/Screenshot-2020-03-04-at-23-43-36.png">
</p>
<br/>
Solution uses Django framework, due to ease in creation of database.<br/>
Solution implements 3 different algorithms: <br/><br/>
<li>Greedy Search (Nearest-neighbour heuristic)</li>
<li>Simulated Annealing</li>
<li>Christofides Algorithm</li>



## Running

First, we have to add Google Maps API key into api_key.py file located inside beer_test folder

```
MAPS_API_KEY = "<INSERT API KEY HERE>"
```

We have to install pipenv virtual environment:

```
pip install pipenv
```

Install project dependencies:
```
pipenv install
```

We have to activate Python virtual environment: <br/>

```
pipenv shell
```
Next, we have to run the Django server:
```
python manage.py runserver
```

## Tests
Once virtual environment is activated, we can run tests with the following command: <br/>

```
python manage.py test
```

## Docker
To build a Docker image you have to execute following command:

```
docker build -t satalia-beer-test -f Dockerfile .
```

Run Docker container:

```
docker run -it -p 80:8888 satalia-beer-test
```

Access system via following URL:

```
localhost
```
