import json
import os
import re
from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from utils import ImageProcessor  # Image processing utility

app = Flask(__name__)
app.secret_key = 'a-secure-random-secret-key'

# --- Configuration ---
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(APP_ROOT, 'static', 'images')
AUDIO_DIR = os.path.join(APP_ROOT, 'static', 'audio')
BUTTONS_JSON = os.path.join(APP_ROOT, 'buttons.json')

ALLOWED_IMAGE_EXTENSIONS = {'png', 'jpg', 'jpeg'}
ALLOWED_AUDIO_EXTENSIONS = {'mp3', 'wav', 'ogg'}

os.makedirs(IMAGES_DIR, exist_ok=True)
os.makedirs(AUDIO_DIR, exist_ok=True)

# --- Helper Functions ---

def load_buttons():
    if os.path.exists(BUTTONS_JSON):
        with open(BUTTONS_JSON, 'r') as f:
            return json.load(f)
    return []

def save_buttons(buttons_data):
    try:
        with open(BUTTONS_JSON, 'w') as f:
            json.dump(buttons_data, f, indent=4)
    except IOError as e:
        flash(f"ERROR: Could not write to buttons.json: {e}", 'danger')

def is_allowed_file(filename, allowed_extensions):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def sanitize_filename(name):
    """Sanitize user input to create a safe filename."""
    name = name.strip().lower().replace(' ', '_')
    return re.sub(r'[^a-z0-9_\-]', '', name)

# --- Routes ---

@app.route('/')
def main_menu():
    return render_template('main_menu.html')

@app.route('/app')
def button_grid():
    buttons = load_buttons()
    return render_template('app.html', buttons=buttons)

@app.route('/config', methods=['GET', 'POST'])
def config():
    buttons = load_buttons()

    if request.method == 'POST':
        try:
            button_id = int(request.form.get('button_id'))
            new_text = request.form.get('button_text', '').strip()
            image_file = request.files.get('image_file')
            audio_file = request.files.get('audio_file')

            button = next((b for b in buttons if b['id'] == button_id), None)
            if not button:
                flash('Error: Button ID not found.', 'danger')
                return redirect(url_for('config'))

            if new_text:
                if not re.match(r'^[a-zA-Z0-9 _-]+$', new_text):
                    flash("Invalid name: Only letters, numbers, spaces, underscores, and dashes are allowed.", "danger")
                    return redirect(url_for('config'))
                button['text'] = new_text

            sanitized_name = sanitize_filename(button['text'])

            # Process image
            if image_file and image_file.filename:
                if is_allowed_file(image_file.filename, ALLOWED_IMAGE_EXTENSIONS):
                    image_filename = f"{sanitized_name}.png"
                    image_path = os.path.join(IMAGES_DIR, image_filename)
                    ImageProcessor.process_and_save(image_file, image_path)
                    button['image'] = image_filename
                else:
                    flash("Unsupported image format.", "danger")

            # Process audio
            if audio_file and audio_file.filename:
                if is_allowed_file(audio_file.filename, ALLOWED_AUDIO_EXTENSIONS):
                    ext = os.path.splitext(secure_filename(audio_file.filename))[1]
                    audio_filename = f"{sanitized_name}{ext}"
                    audio_path = os.path.join(AUDIO_DIR, audio_filename)
                    audio_file.save(audio_path)
                    button['audio'] = audio_filename
                else:
                    flash("Unsupported audio format.", "danger")

            save_buttons(buttons)
            flash(f"Button '{button['text']}' updated successfully!", 'success')

        except Exception as e:
            flash(f"Unexpected error: {e}", 'danger')

        return redirect(url_for('config'))

    return render_template('config.html', buttons=buttons)

@app.route('/create', methods=['GET', 'POST'])
def create_button():
    if request.method == 'POST':
        buttons = load_buttons()

        new_text = request.form.get('button_text', '').strip()
        image_file = request.files.get('image_file')
        audio_file = request.files.get('audio_file')

        if not new_text or not image_file or not audio_file or not image_file.filename or not audio_file.filename:
            flash('All fields (Name, Image, Audio) are required.', 'danger')
            return redirect(url_for('create_button'))

        if not re.match(r'^[a-zA-Z0-9 _-]+$', new_text):
            flash("Invalid name: Only letters, numbers, spaces, underscores, and dashes are allowed.", "danger")
            return redirect(url_for('create_button'))

        if not is_allowed_file(image_file.filename, ALLOWED_IMAGE_EXTENSIONS):
            flash('Invalid image format.', 'danger')
            return redirect(url_for('create_button'))

        if not is_allowed_file(audio_file.filename, ALLOWED_AUDIO_EXTENSIONS):
            flash('Invalid audio format.', 'danger')
            return redirect(url_for('create_button'))

        new_id = (max((b['id'] for b in buttons), default=0) + 1)
        sanitized_name = sanitize_filename(new_text)

        try:
            image_filename = f"{sanitized_name}.png"
            image_path = os.path.join(IMAGES_DIR, image_filename)
            ImageProcessor.process_and_save(image_file, image_path)

            ext = os.path.splitext(secure_filename(audio_file.filename))[1]
            audio_filename = f"{sanitized_name}{ext}"
            audio_path = os.path.join(AUDIO_DIR, audio_filename)
            audio_file.save(audio_path)

            new_button = {
                "id": new_id,
                "text": new_text,
                "image": image_filename,
                "audio": audio_filename
            }

            buttons.append(new_button)
            save_buttons(buttons)

            flash(f"New button '{new_text}' created successfully!", 'success')
            return redirect(url_for('config'))

        except Exception as e:
            flash(f"Error during file processing: {e}", 'danger')
            return redirect(url_for('create_button'))

    return render_template('create.html')

@app.route('/delete/<int:button_id>', methods=['POST'])
def delete_button(button_id):
    buttons = load_buttons()
    button = next((b for b in buttons if b['id'] == button_id), None)

    if button:
        try:
            image_path = os.path.join(IMAGES_DIR, button['image'])
            audio_path = os.path.join(AUDIO_DIR, button['audio'])

            for path in (image_path, audio_path):
                if os.path.exists(path):
                    os.remove(path)

            buttons = [b for b in buttons if b['id'] != button_id]
            save_buttons(buttons)
            flash(f"Button '{button['text']}' was deleted.", 'success')
        except Exception as e:
            flash(f"Error deleting files: {e}", 'danger')
    else:
        flash('Button not found.', 'danger')

    return redirect(url_for('config'))

if __name__ == '__main__':
    app.run(debug=True)
