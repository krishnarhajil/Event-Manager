import qrcode

def generate_event_qr(event_id : int):
    data = f"http://localhost:8000/attendance/scan/{event_id}"
    filename = f"event_{event_id}"
    return generate_qr_code(data, filename)

def generate_qr_code(data:str, filename: str):
    qr = qrcode.QRCode(
        version=1,
        box_size=10,
        border=4
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill = "black", back_color = "white")
    filepath = f"qrcodes/{filename}.png"
    img.save(filepath)
    return filepath