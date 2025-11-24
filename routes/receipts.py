from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models import db, Receipt

receipts_bp = Blueprint("receipts", __name__)


def admin_only():
    return current_user.is_authenticated and current_user.role == "admin"



@receipts_bp.route("/")
@login_required
def list_receipts():
    if not admin_only():
        flash("Access denied.")
        return redirect(url_for("main.index"))

    all_receipts = Receipt.query.order_by(Receipt.id.desc()).all()
    return render_template("receipts_list.html", receipts=all_receipts)



@receipts_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_receipt():
    if not admin_only():
        flash("Access denied.")
        return redirect(url_for("main.index"))

    if request.method == "POST":
        r = Receipt(
            date=request.form.get("date"),
            to=request.form.get("to"),
            phone=request.form.get("phone"),
            work_performed_at=request.form.get("work_performed_at"),
            address=request.form.get("address"),
            description=request.form.get("description"),
            price=float(request.form.get("price") or 0),
            total=float(request.form.get("total") or 0),
            terms=request.form.get("terms"),
            signature_name=request.form.get("signature_name"),
            signature_date=request.form.get("signature_date"),
            created_by=current_user.id
        )

        db.session.add(r)
        db.session.commit()
        flash("Receipt created.")
        return redirect(url_for("receipts.view_receipt", receipt_id=r.id))

    return render_template("receipt_form.html")



@receipts_bp.route("/<int:receipt_id>")
@login_required
def view_receipt(receipt_id):
    if not admin_only():
        flash("Access denied.")
        return redirect(url_for("main.index"))

    receipt = Receipt.query.get_or_404(receipt_id)
    return render_template("receipt_view.html", r=receipt)
