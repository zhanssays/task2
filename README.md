# Chat


## Installation

Create virtual environment

```bash
python3 -m venv /path/to/new/virtual/environment
```

Activate virtual environment
```bash
source /path/to/new/virtual/environment/bin/activate
```

Install dependencies
```bash
pip install requirements.txt
```

Run application
```bash
python manage.py runserver
```

## Usage
Let's say Alice and Bob want to chat with each other:

On first browser Alice opens login page and enter her username `alice`:
http://localhost:8000/chat/login/

To chat with Bob she opens:
http://localhost:8000/chat/bob/

On second browser Bob opens login page and enter his username `bob`:
http://localhost:8000/chat/login/

To chat with Alice he opens:
http://localhost:8000/chat/alice/

## API endpoints

To view all messages:
GET http://localhost:8000/api/chat/messages/

To send a message
POST http://localhost:8000/api/chat/messages/
```
{
    "sender": "alice",
    "recipient": "bob",
    "text": "message sent from api"
}
```


