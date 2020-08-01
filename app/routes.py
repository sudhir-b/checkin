from flask import render_template, redirect, flash, url_for, request
from app import app, db
from app.nmap import get_mac_address
from app.models import User, Device
from app.forms import RegistrationForm


@app.route("/")
@app.route("/home")
def home():
    active_devices = Device.query.filter_by(is_active=True).all()

    print(active_devices)

    active_users = set()
    for active_device in active_devices:
        active_users.add(User.query.get(active_device.user_id))

    print(active_users)

    return render_template("home.html", title="Home", users=active_users)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        mac_address = get_mac_address(request.remote_addr)
        if not mac_address:
            flash("Error: could not get device MAC address")
            return redirect(url_for("register"))
        
        assert len(mac_address) == 1
        mac_address = mac_address[0]

        devices = Device.query.all()
        for device in devices:
            if device.mac_addr == mac_address:
                flash("Device MAC address already registered")
                return redirect(url_for("register"))

        user = User.query.filter_by(name=form.name.data).first()
        if user is None:
            user = User(name=form.name.data)
            db.session.add(user)
            db.session.commit()

        new_device = Device(
            name=form.device_name.data,
            mac_addr=mac_address,
            user_id=user.id,
            is_active=True,
            last_known_ip=request.remote_addr,
        )

        db.session.add(new_device)
        db.session.commit()

        return redirect(url_for("home"))

    return render_template("register.html", title="Register", form=form)

