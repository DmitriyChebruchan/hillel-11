# hillel-11

Following are the steps to turn on Celery:

<ol>
  <li>Install all requirements.<br>
    ```
    pip install -r requirements.txt
    ```
  </li>

  <li>Open the Docker container<br>
    ```
    docker run -d -p 5672:5672 rabbitmq
    ```
  </li>

  <li>To collect rates, run Celery<br>
    ```
    celery -A exchange beat
    ```
  </li>

  <li>Turn on the worker</li>
    ```
    celery -A exchange worker -B
    ```
</ol>
