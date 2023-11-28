## Python Backend

### Setup dependencies with [`venv`](https://docs.python.org/3/library/venv.html)

```
# Create venv :
python3 -m venv .venv

# Activate venv:
. .venv/bin/activate

# Sync dependencies from `requirements.txt`:
pip install -r requirements.txt

# Update `requirements.txt`:
pip install <some-new-dependency>
pip freeze > requirements.txt
```

## Run Server

```
flask run [--debug]
```