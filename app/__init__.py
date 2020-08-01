import atexit

from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)


from app import routes, models


def scan_local_network():
    from app.nmap import get_mac_address
    print('Scanning local network')
    active_mac_addresses = set(get_mac_address('192.168.0.0/24')) 

    print(f"Found MAC addresses: {active_mac_addresses}")

    devices = models.Device.query.all()

    for device in devices:
        print(f"Device mac addr: {device.mac_addr}")
        print(f"Old is_active: {device.is_active}")
        device.is_active = (device.mac_addr in active_mac_addresses)
        print(f"New is_active: {device.is_active}")
        db.session.add(device)

    db.session.commit()

scheduler = BackgroundScheduler()
scheduler.add_job(func=scan_local_network, trigger="interval", seconds=600)
scheduler.start()


# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())