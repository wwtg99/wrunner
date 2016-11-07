# wrunner

Distributed Task Queue and Scheduler based on Celery.

## Installation
1. Install celery first
2. Clone project files
3. Run python wrunner.py

## Definition
- celery_app.py: main celery application
- runner_config.py: global config module
- tasks.py: default task module
- wrunner.py: runner client

## Usage

#### Worker
Start worker
```
python wrunner.py worker
python wrunner.py worker --logfile=worker.log //use specific log file
python wrunner.py worker -B //also run beat scheduler
```

#### Schedule
Start schedule beat
```
python wrunner.py beat
python wrunner.py beat -s aaa //use aaa to name beat schedule file
```

#### Send Task
```
python wrunner.py task <module> <function>
//send task cmd to run 'ls'
python wrunner.py task tasks cmd -p ls
```

#### Inspect
Inspect worker
```
python wrunner.py inspect active //more command see celery inspect --help
```

#### Log
View log
```
python wrunner.py log
python wrunner.py log -f //follow log tail
```
