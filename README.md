# hillel-11

Following are the steps to turn on Celery:

<ol>
  <li>Install all requirements.

```pip install -r requirements.txt```
  </li>

  <li>Open the Docker container

```docker run -d -p 5672:5672 rabbitmq```
  </li>

  <li>To collect rates, run Celery

```celery -A exchange beat```
  </li>

  <li>Turn on the worker

```celery -A exchange worker -B ```
</li>
</ol>

To run Django project run following command<br>
```python manage.py runserver```