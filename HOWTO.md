#Hot to run and config the app

## initial config

1. edit settings in backend_test/

add to the env var the slack token and SITE_URL

```bash
export SLACK_TOKEN=token_here
export SITE_URL=site_url_here
```

by default the notification in the slack notification will be send until 10 and will block lunch until 11, if you want 
to change this you can set the following en vars

```bash
export SLACK_SEND_MENU_HOUR=10
export SLACK_BLOCK_MENU_HOUR=11
```

2. config data

for create the basic user run the following command

```bash
python manage.py create_user 'slack_key_here' 
```

the slack_key_here must be the id in slack than point to the channel

3. run the app

for run the app you must run the following

3.1 Django

```bash
python manage.py runserver 
```

3.2 Celery (this will be required to send the menu to slack)

```bash
celery -A backend_test worker -l info
```

3.3 Celery beat (this will be required run periodically the task)

```bash
celery -A backend_test beat
```

3.4 Docker

if you are using the docker container you must connect to the base and run the following

```bash
dev run
```
```bash
dev celery
```
```bash
dev cbeat
```