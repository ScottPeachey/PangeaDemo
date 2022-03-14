# PangeaDemo

Example repository for Pangea Maps.

This is an example web page for viewing 3d points and fitting a plane to the data. 

## Python

Built using python 3.10, conda 4.10.3 (https://docs.conda.io/en/latest/miniconda.html)

## Running

When running the first time and not using an IDE:

```shell
conda create --name PangeaDemo --file requirments.txt python=3.10
pre-commit install
export FLASK_APP=wsgi.py
flask run
```

After the initial set-up set the environment variable
```shell
export FLASK_APP=wsgi.py
```
Then in the repository root directory run
```shell
flask run
```


## Contributing

When contributing to this repository please use the python package `pre-commit` with the configuration files present to 
ensure your code matches our coding style.