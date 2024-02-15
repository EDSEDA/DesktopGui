# DesktopGui

---
## About
App with PyQt5 and rabbitMQ listener

## Dependencies
- RabbitMQ
  - for init run command: `sudo docker run -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.12-management`

## Quiq start

Create venv:
- for Windows:
``` bash
python -m venv venv
.\venv\Scripts\activate
```
- for Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```

1. pip install -r requirements
2. python main.py