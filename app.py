from flask import Flask, render_template, request, send_file, redirect, url_for
import qrcode
from io import BytesIO
import base64

app = Flask(__name__)

# Function to generate QR code
def generate_qr_code(text):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(text)
    qr.make(fit=True)
    img = qr.make_image(fill_color="black", back_color="white")
    
    # Save image in memory
    byte_io = BytesIO()
    img.save(byte_io, 'PNG')
    byte_io.seek(0)
    
    return byte_io

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['qrtext']
        if text:
            img_io = generate_qr_code(text)
            
            # Encode image to display inline
            img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
            return render_template('index.html', img_data=img_base64, text=text)
    return render_template('index.html')

@app.route('/download', methods=['POST'])
def download():
    text = request.form['qrtext']
    if text:
        img_io = generate_qr_code(text)
        return send_file(img_io, mimetype='image/png', as_attachment=True, download_name='qrcode.png')

# if __name__ == '__main__':
#     app.run(debug=True)
