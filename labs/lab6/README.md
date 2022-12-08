### To start `tasks.py`, you will need:

1. [Windows Subsystem for Linux](https://learn.microsoft.com/ru-ru/windows/wsl/install)
2. [RabbitMQ Server **for Windows**](https://github.com/rabbitmq/rabbitmq-server/releases)

### After installing WSL and RabbitMQ, execute following lines:

1. **In PowerShell**: `rabbitmq-server.bat`
2. **In WSL**: `celery -A tasks worker -B -l INFO -E`
