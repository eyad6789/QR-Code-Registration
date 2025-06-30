from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from PIL import Image, ImageDraw, ImageFont
import qrcode
import os

app = Flask(__name__)
app.secret_key = '2001@EYad'  # Replace with a strong secret key
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///attendees.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# --------------------------------------------------------------------
# Database Model
# --------------------------------------------------------------------
class Attendee(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # Auto-generated numeric ID
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    qr_code = db.Column(db.String(255), unique=True, nullable=False)
    checked_in = db.Column(db.Boolean, default=False)

with app.app_context():
    db.create_all()

# --------------------------------------------------------------------
# Helper Functions
# --------------------------------------------------------------------
def generate_qr_code(data, path):
    """Generate a QR code image from the given data and save it to the specified path."""
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    img.save(path)

def create_id_card_image(attendee_id, name, email):
    """
    Create an ID card image for an attendee using Pillow.
    The card contains the attendee's ID, name, email, and a QR code.
    """
    # Generate QR code image from attendee_id
    qr_data = str(attendee_id)
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(qr_data)
    qr.make(fit=True)
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Create a blank ID card image
    card_width = 600
    card_height = 300
    card = Image.new('RGB', (card_width, card_height), color='white')
    draw = ImageDraw.Draw(card)
    
    # Setup font (using Arial if available)
    try:
        font = ImageFont.truetype("arial.ttf", size=24)
    except IOError:
        font = ImageFont.load_default()
    
    margin = 20
    y_text = margin
    draw.text((margin, y_text), "Conference ID Card", fill="black", font=font)
    y_text += 40
    draw.text((margin, y_text), f"ID: {attendee_id}", fill="black", font=font)
    y_text += 40
    draw.text((margin, y_text), f"Name: {name}", fill="black", font=font)
    y_text += 40
    draw.text((margin, y_text), f"Email: {email}", fill="black", font=font)
    
    # Resize and paste the QR code onto the card
    qr_size = 150
    qr_img = qr_img.resize((qr_size, qr_size))
    qr_position = (card_width - qr_size - margin, margin)
    card.paste(qr_img, qr_position)
    
    # Ensure the idcards folder exists
    idcards_folder = os.path.join(app.static_folder, 'idcards')
    if not os.path.exists(idcards_folder):
        os.makedirs(idcards_folder)
    
    # Save the ID card image
    filename = f"id_card_{attendee_id}.png"
    card_path = os.path.join(idcards_folder, filename)
    card.save(card_path)
    return filename

# --------------------------------------------------------------------
# Routes
# --------------------------------------------------------------------

# Registration Route
@app.route('/', methods=['GET', 'POST'])
def register():
    qr_code_image = None
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        if not name or not email:
            flash("Name and Email are required", "error")
            return redirect(url_for('register'))
        
        # Check if attendee is already registered
        if Attendee.query.filter_by(email=email).first():
            flash("Attendee already registered", "error")
            return redirect(url_for('register'))
        
        # Create new attendee record (temporary empty QR code field)
        new_attendee = Attendee(name=name, email=email, qr_code="")
        db.session.add(new_attendee)
        db.session.commit()
        
        # Generate QR code using the attendee's numeric ID
        qrcodes_folder = os.path.join(app.static_folder, 'qrcodes')
        if not os.path.exists(qrcodes_folder):
            os.makedirs(qrcodes_folder)
        qr_filename = f"{new_attendee.id}.png"
        qr_path = os.path.join(qrcodes_folder, qr_filename)
        generate_qr_code(str(new_attendee.id), qr_path)
        
        # Update attendee record with the QR code file path
        new_attendee.qr_code = f"qrcodes/{qr_filename}"
        db.session.commit()
        
        flash("Registered successfully", "success")
        qr_code_image = new_attendee.qr_code
        
    return render_template("register.html", qr_code=qr_code_image)

# Route to view attendees in the database
@app.route('/view_attendees')
def view_attendees():
    attendees = Attendee.query.all()
    return render_template('view_attendees.html', attendees=attendees)


# QR Code Scanning Route
import cv2
from pyzbar.pyzbar import decode
from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy


# QR Code Scanning and Check-in
@app.route('/scan', methods=['GET', 'POST'])
def scan():
    if request.method == 'POST':
        # Check if file is uploaded
        if 'qr_code_image' not in request.files:
            flash('No file part', 'error')
            return redirect(url_for('scan'))
        
        file = request.files['qr_code_image']
        if file.filename == '':
            flash('No selected file', 'error')
            return redirect(url_for('scan'))

        # Save the uploaded image temporarily
        qr_code_image_path = 'scanned_qrcode.png'
        file.save(qr_code_image_path)

        # Read the image using OpenCV
        img = cv2.imread(qr_code_image_path)
        decoded_objects = decode(img)

        if decoded_objects:
            # Get the ID from the QR code
            attendee_id = int(decoded_objects[0].data.decode('utf-8'))

            # Check if the attendee exists in the database
            attendee = Attendee.query.get(attendee_id)
            if attendee:
                if not attendee.checked_in:
                    attendee.checked_in = True
                    db.session.commit()
                    flash(f"Welcome {attendee.name}, you've been checked in!", 'success')
                else:
                    flash(f"{attendee.name} has already checked in.", 'info')
            else:
                flash("Attendee not found. This ID is not registered.", 'error')
        else:
            flash("Invalid QR code or no QR code detected.", 'error')

        return redirect(url_for('scan'))

    return render_template("scan.html")

if __name__ == '__main__':
    app.run(debug=True)
