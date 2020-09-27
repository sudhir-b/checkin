from flask import render_template, redirect, flash, url_for, request
from app import app, db
from app.nmap import get_mac_address
from app.models import User, Device
from app import forms


@app.route("/")
@app.route("/home")
def home():
    active_users = User.query.join(Device).filter(Device.is_active == True).all()
    return render_template("home.html", title="Home", users=active_users)


@app.route("/register", methods=["GET", "POST"])
def register():
    form = forms.RegistrationForm()
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

        # TODO: should this be case insensitive?
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


@app.route("/unregister", methods=["GET", "POST"])
def unregister():
    form = forms.UnregisterForm()

    if form.validate_on_submit():
        for row in form.rows:
            if row.select.data:
                # TODO: look at using bulk deletion here
                to_delete = Device.query.filter_by(id=row.device_id.data).first()
                if to_delete is not None:
                    db.session.delete(to_delete)

        db.session.commit()
        return redirect(url_for("unregister"))

    users = User.query.all()
    user_info = {}
    for user in users:
        for device in user.devices:
            form_row = forms.UnregisterFormRow()
            form_row.device_id = device.id
            form.rows.append_entry(form_row)

            user_info[device.id] = {
                "user_name": user.name,
                "device_name": device.name,
                "is_active": device.is_active,
            }

    return render_template(
        "unregister.html", title="Unregister", form=form, user_info=user_info
    )

