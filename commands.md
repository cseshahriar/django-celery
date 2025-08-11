.env
DEBUG=True
SECRET_KEY=dfods087fsdf8df9dfd9f

pip freeze > requirements.txt
chmod +x ./entrypoint.sh
docker compose up -d --build

$ celery start
celery -A config worker -l INFO

python manage.py shell
from newapp.tasks import add
add.delay(5, 6)
<AsyncResult: 8d17b72b-ca6d-4e8c-ada0-ef963faf04d8>


# celery task routine
- improved scalability
- load balancing
- granular control

celery -A config worker -l INFO -Q queue1
celery -A config worker -l INFO -Q celery,celery:1,celery:2,celery:3

# task priority 0 to 9

# task group: from celery import group
tasks_group = group(add.s(), mul.s())
tasks_group.apply_async()

# task chaining
from celery import chain
from newapp.tasks import tp1, tp2, tp3
task_chain = chain(tp1.s(), tp2.s(), tp3.s())
task_chain.apply_async()
<AsyncResult: 4c88fdc7-d2ac-4f4d-8ceb-d429960a3adb>
task_chain = chain(tp3.s(), tp1.s(), tp2.s())
task_chain.apply_async()

# task rate limit


celery inspect active
celery inspect active_queues

celery -A config flower

http://localhost:15672/
http://0.0.0.0:5555/tasks
http://127.0.0.1:8000/admin/django_celery_results/taskresult/


Types of Scheduling Mechanisms:
* Time-based Scheduling
* Event-based Scheduling
* Dependency-based Scheduling

Benefits of Automated Task Scheduling:
* Increased Efficiency
* Optimal Resource Utilization
* Improved Scalability
* Enhanced Reliability

Understanding Periodic Tasks:
* Time base recurring tasks

Configuring Celery for Periodic Tasks:
* Celery beat scheduler configuration
* Defining Periodic Tasks
* Customizing Periodic Tasks


celery -A worker -l INFO -Q tasks,dead_letter -E -B