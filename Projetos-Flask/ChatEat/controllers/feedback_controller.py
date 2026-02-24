from flask import render_template, request, session, redirect, url_for, flash
from models.feedback_class import FeedbackService


def feedback():
    return render_template("feedback.html")


def enviar():
    user = session.get("usuario_id")
    comentario = request.form.get("comentario", "")
    nota = request.form.get("nota", "")
    result = FeedbackService.enviar(user, comentario, nota)
    if result["ok"]:
        flash(result["msg"], "success")
    else:
        flash(result["msg"], "danger")
    return redirect(url_for("home.index"))
