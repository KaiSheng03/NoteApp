from flask import Blueprint, request, flash, render_template, jsonify
from flask_login import login_required, current_user
from .models import Note, User  # Import your PyMongo models
from . import mongo  # Import the PyMongo instance
import json
from bson import ObjectId

views = Blueprint('views', __name__)

@views.route('/', methods=["GET", "POST"])
@login_required
def home():
    # Load the notes
    if request.method == "POST":
        note = request.form.get("note")

        if len(note) < 1:
            flash("Note is too short!", category='error')
        else:
            new_note = Note(note, current_user._id)  # Use the user's _id
            new_note.save()  # Save the note to MongoDB
            flash("Note is added", category='success')

    return render_template("home.html", user_note=Note.find_notes_by_user_id(current_user._id), user=current_user)

@views.route('/delete-note', methods=["POST"])
def delete_note():
    note = json.loads(request.data)
    noteId = note['noteId']
    note = Note.find_and_delete(ObjectId(noteId))  # Find and delete the note by _id
    return jsonify({})

@views.route('/share-note', methods=["POST"])
def share_note():
    data = json.loads(request.data)
    noteId = data['noteId']
    shareEmail = data['shareEmail']

    note = Note.find_note(ObjectId(noteId))  # Find the note to share
    if note:
        shareNote = note['data']  # Access the 'data' field from the note document
        userShare = User.find_by_email(shareEmail)  # Find the user to share with
        if userShare:
            share_new_note = Note(shareNote, userShare['_id'])  # Create a new shared note
            share_new_note.save()  # Save the shared note to MongoDB
            flash("Note is shared", category='success')

        else:
            flash("User with this email is not found", category='error')
    else:
        flash("Not found", category='error')
    return jsonify({})

@views.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        firstName = request.form.get('firstName')
        lastName = request.form.get('lastName')
        age = request.form.get('age')
        address = request.form.get('address')
        
        # Update the user's profile data in MongoDB
        User.find_and_update(current_user._id, firstName, lastName, age, address)
        flash("Profile updated successfully. Please refresh.", category='success')

    return render_template('profile.html', user=current_user)
