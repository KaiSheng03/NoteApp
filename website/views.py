from flask import Blueprint, request, flash,render_template, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import db
import json
from .models import User

views = Blueprint('views',__name__)

@views.route('/', methods=["GET","POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")
        
        if(len(note)<1):
            flash("Note is too short!", category='error')
        else:
            new_note = Note(data=note, user_id=current_user.id)
            db.session.add(new_note)
            db.session.commit()
            flash("Note is added", category='success')
    
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.query.get(noteId)
    if note:
        if note.user_id == current_user.id:
            db.session.delete(note)
            db.session.commit()
    return jsonify({})

@views.route('/share-note', methods=["POST"])
def share_note():
    data = json.loads(request.data)
    noteId = data.get('noteId')
    shareEmail = data.get('shareEmail')
    note = Note.query.get(noteId)
    if note:
        shareNote = note.data
        userShare = User.query.filter_by(email=shareEmail).first()
        if userShare:
            shareId = userShare.id
            share_new_note = Note(data=shareNote, user_id = shareId)
            db.session.add(share_new_note)
            db.session.commit()
            flash("Note is shared", category='success')
        else:
            flash("User with this email is not found", category='error')
    return jsonify({})
        
@views.route('/profile', methods=['GET','POST'])
def profile():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        age = request.form.get('age')
        address = request.form.get('address')
        user = User.query.filter_by(id = current_user.id).first()
        if user:
            user.first_name = firstName
            db.session.commit()

            user.last_name = lastName
            db.session.commit()

            user.age = age
            db.session.commit()

            user.address = address
            db.session.commit()
            flash("Profile updated successfully", category='success')

    return render_template('profile.html', user = current_user)