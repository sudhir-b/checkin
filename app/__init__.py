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

RESCAN_INTERVAL_SECONDS = 600
LOCAL_NETWORK_SEGMENT = "192.168.0.0/24"


def scan_local_network():
    from app.nmap import get_mac_address

    active_mac_addresses = set(get_mac_address(LOCAL_NETWORK_SEGMENT))
    devices = models.Device.query.all()

    for device in devices:
        device.is_active = device.mac_addr in active_mac_addresses
        db.session.add(device)

    db.session.commit()


scheduler = BackgroundScheduler()
scheduler.add_job(
    func=scan_local_network, trigger="interval", seconds=RESCAN_INTERVAL_SECONDS
)
scheduler.start()


# Shut down the scheduler when exiting the app
atexit.register(lambda: scheduler.shutdown())
