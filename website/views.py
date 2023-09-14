from flask import Blueprint, request, flash,render_template, jsonify
from flask_login import login_required, current_user
from .models import Note
from . import mongo
import json
from .models import User
from bson import ObjectId

views = Blueprint('views',__name__)

@views.route('/', methods=["GET","POST"])
@login_required
def home():
    if request.method == "POST":
        note = request.form.get("note")
        
        if(len(note)<1):
            flash("Note is too short!", category='error')
        else:
            new_note = {"Id": current_user["id"], "Note": note}
            mongo.database.insert_one(new_note)
            flash("Note is added", category='success')
    
    return render_template("home.html", user=current_user)

@views.route('/delete-note', methods=["POST"])
def delete_note():
    data = request.get_json()  # Get JSON data from the request

    if 'noteId' in data:
        note_id = data['noteId']

        # Convert the note_id from string to ObjectId
        note_id = ObjectId(note_id)

        # Find the note in the 'notes' collection
        note = mongo.database.notes.find_one({'_id': note_id})

        if note:
            # Check if the note belongs to the current user
            if note['user_id'] == current_user.id:
                # Delete the note from the 'notes' collection
                mongo.database.notes.delete_one({'_id': note_id})

    return jsonify({})  # Return an empty JSON response
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