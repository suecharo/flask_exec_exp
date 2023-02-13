# flask_exec_exp

Experimenting using Flask and [Flask-Executor](https://flask-executor.readthedocs.io/en/latest/).

## Environment

```bash
$ docker compose up -d --build
$ docker compose exec app bash
```

## Example

```bash
$ python3 ./flask_exec_exp/app.py
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:8080
 * Running on http://172.19.0.2:8080
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 679-794-273
```

### Running and complete

```bash
$ curl -X POST localhost:8080/validate -H "Content-Type: application/json" -d '{"arg1": "foo", "arg2": "bar"}'
{
  "requestId": "721a6ef3-7872-454e-ae5b-3be6ecb2e815"
}

$ curl -X GET localhost:8080/721a6ef3-7872-454e-ae5b-3be6ecb2e815
{
  "request": {
    "arg1": "foo",
    "arg2": "bar"
  },
  "requestId": "721a6ef3-7872-454e-ae5b-3be6ecb2e815",
  "results": [],
  "status": "RUNNING"
}

$ curl -X GET localhost:8080/721a6ef3-7872-454e-ae5b-3be6ecb2e815
{
  "request": {
    "arg1": "foo",
    "arg2": "bar"
  },
  "requestId": "721a6ef3-7872-454e-ae5b-3be6ecb2e815",
  "results": [
    {
      "key": "arg1",
      "val": "foo"
    },
    {
      "key": "arg2",
      "val": "bar"
    }
  ],
  "status": "COMPLETE"
}
```

### Cancel

```bash
$ curl -X POST localhost:8080/validate -H "Content-Type: application/json" -d '{"arg1": "foo", "arg2": "bar"}'
{
  "requestId": "ba66637c-3ec7-4e96-afa8-f79b757d18d8"
}
$ curl -X GET localhost:8080/ba66637c-3ec7-4e96-afa8-f79b757d18d8
{
  "request": {
    "arg1": "foo",
    "arg2": "bar"
  },
  "requestId": "ba66637c-3ec7-4e96-afa8-f79b757d18d8",
  "results": [],
  "status": "RUNNING"
}
$ curl -X POST localhost:8080/ba66637c-3ec7-4e96-afa8-f79b757d18d8/cancel
<!doctype html>
<html lang=en>
<title>400 Bad Request</title>
<h1>Bad Request</h1>
<p>Failed to cancel</p>
```

### Error

```bash
$ curl -X POST localhost:8080/validate -H "Content-Type: application/json" -d '{"error": "foobar"}'
{
  "requestId": "3b4f97f2-02a3-4b9c-92eb-388cb662c2cd"
}

$ curl -X GET localhost:8080/3b4f97f2-02a3-4b9c-92eb-388cb662c2cd
{
  "request": {
    "error": "foobar"
  },
  "requestId": "3b4f97f2-02a3-4b9c-92eb-388cb662c2cd",
  "results": [
    {
      "err_msg": "This is our implemented error: foobar"
    }
  ],
  "status": "FAILED"
}
```
