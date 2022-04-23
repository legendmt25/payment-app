### Payment app
```
python -m virtualenv venv
./venv/Scripts/activate
pip install -r requirements.txt
python server.py
```
or
```
docker build -t payment-app .
docker run payment-app
```