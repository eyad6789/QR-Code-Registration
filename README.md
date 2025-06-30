# QR Code Conference Check-in System 🎫
This project is a simple Flask-based web application designed to generate unique QR codes for conference attendees. Each attendee receives a personalized QR code upon registration, which can later be scanned at the event entrance to mark their attendance.

## 🛠 Features
- ✅ Attendee registration with name and email
- ✅ Automatic generation of a unique QR code for each attendee
- ✅ Generation of personalized ID cards with QR codes
- ✅ Simple interface for scanning attendee QR codes and marking attendance
- ✅ Admin view to see the list of all registered attendees
- ✅ Attendance status management (checked-in flag)

## 📦 Technologies Used
- Flask - Web framework
- SQLite - Lightweight database
- SQLAlchemy - ORM for database interaction
- Pillow (PIL) - For ID card image generation
- qrcode - For QR code generation
- OpenCV & pyzbar - For QR code scanning

📁 Project Structure
```
/static/
├── idcards/       
├── qrcodes/       

/templates/
├── register.html  
├── view_attendees.html 
├── scan.html      

app.py            
attendees.db      
```
## 🚀 How It Works
Register Attendees:
Users fill in their name and email on the registration page.
A unique QR code and an ID card image are generated for them.

- Check-in Process:
At the event, attendees present their QR code at the check-in station.
The system scans the QR code and marks them as 'checked-in' if valid.

- Admin View:
Admins can view a list of all attendees along with their check-in status.

## 🖥️ Installation & Running
Clone the Repository
```
git clone https://github.com/eyad6789/QR-Code-Conference-Check-in-System.git
cd QR-Code-Conference-Check-in-System
Install Dependencies
```
```
pip install -r requirements.txt
```
Run the Application
```
python app.py
```
Visit http://127.0.0.1:5000 in your browser.

## ⚡ Requirements
- Python 3.x
- Flask
- Flask SQLAlchemy
- Pillow
- qrcode
- OpenCV
- pyzbar
##📌 Notes
- Generated QR codes and ID cards are stored in the /static/qrcodes/ and /static/idcards/ folders respectively.
- Attendance data is stored in an SQLite database file attendees.db.
- You can modify the HTML templates to fit your conference branding.
- For QR scanning, the current implementation uses image upload. It can be extended to use a live camera feed if needed.

##📷 Screenshots
(You can add screenshots of the registration form, ID card example, and the check-in interface here.)

## 💡 Future Improvements
- Live camera-based QR scanning
- Admin authentication
- Email notifications with QR codes
- CSV export of attendee data

## 👤 Author
Developed by Eyad Qasim
