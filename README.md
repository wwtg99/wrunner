# wwu_runner

Distributed Task Queue based on Celery.

## Definition
- celery_app.py: main celery application
- runner_config.py: config module
- tasks.py: default task module, extend function here
- runner-cli.py: client

## Usage

#### Worker
Start worker
```
python runner-cli.py worker
```

#### Send
```
python runner-cli.py task <module> <function>
//run task cmd to run 'ls'
python runner-cli.py task tasks cmd -p ls
```

#### Inspect
Inspect worker
```
python runner-cli.py inspect active
```
