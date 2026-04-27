from flask import Flask, request, jsonify, send_file
from PIL import Image
import io, os, time

app = Flask(__name__)

def process_image(input_bytes, action, params):
    img = Image.open(io.BytesIO(input_bytes))
    buf = io.BytesIO()
    fmt = params.get('format', 'PNG').upper()
    if fmt == 'JPG': fmt = 'JPEG'
    
    if action == 'compress':
        quality = int(params.get('quality', 75))
        if img.mode in ('RGBA', 'P'): img = img.convert('RGB')
        img.save(buf, format='JPEG', quality=quality, optimize=True)
    elif action == 'resize':
        w = int(params.get('width', img.width))
        h = int(params.get('height', img.height))
        img = img.resize((w, h), Image.LANCZOS)
        img.save(buf, format=fmt)
    elif action == 'convert':
        if img.mode in ('RGBA', 'P') and fmt == 'JPEG': img = img.convert('RGB')
        img.save(buf, format=fmt, quality=int(params.get('quality', 90)))
    elif action == 'watermark':
        pass  # placeholder
    else:
        img.save(buf, format=fmt)
    
    buf.seek(0)
    return buf

@app.route('/')
def index():
    return jsonify({
        "service": "Image Tools API",
        "version": "1.0",
        "endpoints": {
            "/compress": "POST - Compress image (quality: 1-100)",
            "/resize": "POST - Resize image (width, height)",
            "/convert": "POST - Convert format (format: PNG/JPEG/WEBP)"
        },
        "usage": "Send image as multipart/form-data file field"
    })

@app.route('/compress', methods=['POST'])
def compress():
    try:
        f = request.files.get('file')
        if not f: return jsonify({"error": "No file provided"}), 400
        buf = process_image(f.read(), 'compress', {
            'quality': request.form.get('quality', 75)
        })
        orig_size = len(f.read()) if hasattr(f, 'read') else 0
        return send_file(buf, mimetype='image/jpeg')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/resize', methods=['POST'])
def resize():
    try:
        f = request.files.get('file')
        if not f: return jsonify({"error": "No file provided"}), 400
        data = f.read()
        img = Image.open(io.BytesIO(data))
        w = int(request.form.get('width', img.width))
        h = int(request.form.get('height', img.height))
        buf = process_image(data, 'resize', {'width': w, 'height': h, 'format': img.format or 'PNG'})
        return send_file(buf, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/convert', methods=['POST'])
def convert():
    try:
        f = request.files.get('file')
        if not f: return jsonify({"error": "No file provided"}), 400
        target = request.form.get('format', 'WEBP').upper()
        if target == 'JPG': target = 'JPEG'
        buf = process_image(f.read(), 'convert', {'format': target})
        mime = {'PNG':'image/png','JPEG':'image/jpeg','WEBP':'image/webp'}.get(target, 'image/png')
        return send_file(buf, mimetype=mime)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
