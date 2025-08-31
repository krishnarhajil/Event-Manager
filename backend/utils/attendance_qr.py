import qrcode
import os

def generate_attendance_qr(event_id: int) -> str:
    """
    Generate QR code for attendance marking.
    The QR encodes the attendance scan endpoint for a given event.
    """
    # What will be encoded in the QR
    qr_data = f"http://localhost:8000/attendance/scan/{event_id}"  

    # Where to save
    folder = "qrcodes/attendance"
    os.makedirs(folder, exist_ok=True)

    file_path = os.path.join(folder, f"attendance_event_{event_id}.png")

    # Generate QR
    img = qrcode.make(qr_data)
    img.save(file_path)

    return file_path
