import cv2
import sqlite3
from pyzbar.pyzbar import decode

# Function to connect to the SQLite database
def connect_db():
    conn = sqlite3.connect("instance/attendees.db")  # Ensure the correct path
    cursor = conn.cursor()
    return conn, cursor

# Function to check if the ID exists in the database and mark them as checked in
def check_and_checkin_person(person_id):
    conn, cursor = connect_db()
    
    # Check if the person exists
    cursor.execute("SELECT * FROM attendee WHERE id = ?", (person_id,))
    person = cursor.fetchone()
    
    if person:
        # If the person is found, update the checked_in status to True
        cursor.execute("UPDATE attendee SET checked_in = ? WHERE id = ?", (True, person_id))
        conn.commit()
        conn.close()
        return person  # Return the person's details
    else:
        conn.close()
        return None  # Return None if the person is not found

# Function to process the QR code and scan for the person ID in real-time
def scan_qrcode():
    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)  # Use DirectShow backend for Windows
    
    while True:
        ret, frame = cap.read()
        if not ret:
            print("Failed to grab frame")
            break
        
        qr_codes = decode(frame)
        
        for qr in qr_codes:
            qr_data = qr.data.decode("utf-8")
            print(f"QR Code Data: {qr_data}")
            
            person = check_and_checkin_person(qr_data)
            if person:
                print(f"Person Found and Checked In: {person}")
                cv2.putText(frame, f"Checked In: {person[1]}", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv2.LINE_AA)
            else:
                print("Person not invited.")
                cv2.putText(frame, "Person Not Invited", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        
        cv2.imshow("QR Code Scanner - Real Time", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

# Run the QR code scanning in real-time
scan_qrcode()
