from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Booking
from datetime import date, timedelta

bookings_bp = Blueprint("bookings", __name__)


@bookings_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_booking():
    if request.method == "POST":
        service = request.form.get("service")
        booking_date = request.form.get("date")
        time_slot = request.form.get("time_slot")
        address = request.form.get("address")
        details = request.form.get("details")
        phone = request.form.get("phone")


        if not (service and booking_date and time_slot and address and details and phone):
            flash("Please complete all required fields.", "danger")
            return redirect(url_for("bookings.new_booking"))

        selected_day = date.fromisoformat(booking_date)


        if selected_day <= date.today():
            flash("You can only book starting tomorrow.", "danger")
            return redirect(url_for("bookings.new_booking"))


        conflict = Booking.query.filter_by(date=selected_day, time_slot=time_slot).first()
        if conflict:
            flash("This time slot is already taken. Please choose another.", "danger")
            return redirect(url_for("bookings.new_booking"))


        booking = Booking(
            service=service,
            date=selected_day,
            time_slot=time_slot,
            address=address,
            details=details,
            phone=phone,
            user_id=current_user.id,
            status="Booked"
        )

        db.session.add(booking)
        db.session.commit()
        flash("Booking created successfully!", "success")
        return redirect(url_for("bookings.my_bookings"))


    min_date = (date.today() + timedelta(days=1)).isoformat()
    return render_template("booking.html", min_date=min_date)



@bookings_bp.route("/my")
@login_required
def my_bookings():

    if hasattr(current_user, 'role') and current_user.role == "admin":
        bookings = Booking.query.order_by(Booking.date.asc()).all()
    else:
        bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.date.asc()).all()

    return render_template("dashboard.html", bookings=bookings, today=date.today())


@bookings_bp.route("/cancel/<int:booking_id>", methods=["POST"])
@login_required
def cancel(booking_id):
    booking = Booking.query.get_or_404(booking_id)


    if hasattr(current_user, 'role') and current_user.role != "admin" and booking.user_id != current_user.id:
        flash("You cannot cancel this booking.", "danger")
        return redirect(url_for("bookings.my_bookings"))

    booking.status = "Canceled"
    db.session.commit()
    flash("Booking canceled successfully.", "success")
    return redirect(url_for("bookings.my_bookings"))
