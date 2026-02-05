from flask import Flask, request, send_from_directory
import os
app = Flask(__name__)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "storage")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
@app.route("/")
@app.route("/")
def home():
    files = os.listdir(UPLOAD_FOLDER)
    file_items = ""
    for f in files:
        file_size = os.path.getsize(os.path.join(UPLOAD_FOLDER, f))
        size_str = f"{file_size / 1024:.1f} KB" if file_size < 1024*1024 else f"{file_size / (1024*1024):.1f} MB"
        file_items += f"""
        <div class="file-item">
            <div class="file-info">
                <div class="file-icon"></div>
                <div class="file-details">
                    <div class="file-name">{f}</div>
                    <div class="file-size">{size_str}</div>
                </div>
            </div>
            <a href="/files/{f}" class="download-btn">Download</a>
        </div>
        """
    
    empty_message = '<div class="empty-state"><p> No files yet. Upload one to get started!</p></div>' if not files else ''
    
    return f"""
<!DOCTYPE html>
<html>
<head>
<title>Mini Cloud Storage</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #001f3f 0%, #003d66 25%, #005580 50%, #1a1a4d 75%, #0a0a2e 100%);
    color: #e2e8f0;
    display: flex;
    justify-content: center;
    align-items: flex-start;
    min-height: 100vh;
    padding: 20px;
    cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><circle cx="16" cy="16" r="6" fill="%23ff6b9d"/><path stroke="%23ff6b9d" stroke-width="2" d="M16 2 v28 M2 16 h28" stroke-linecap="round"/></svg>') 16 16, auto;
    position: relative;
    overflow-x: hidden;
}}

html {{
    scroll-behavior: smooth;
}}

.cloud {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    pointer-events: none;
    z-index: 0;
}}

.cloud::before {{
    content: '';
    position: absolute;
    width: 200px;
    height: 80px;
    background: radial-gradient(ellipse at 30% 40%, rgba(255, 255, 255, 0.3), rgba(200, 220, 255, 0.15));
    border-radius: 100px;
    animation: floatCloud 20s infinite linear;
    top: 10%;
}}

.cloud::after {{
    content: '';
    position: absolute;
    width: 300px;
    height: 120px;
    background: radial-gradient(ellipse at 40% 50%, rgba(100, 200, 255, 0.2), rgba(150, 180, 255, 0.1));
    border-radius: 150px;
    animation: floatCloud2 30s infinite linear;
    top: 30%;
}}

@keyframes floatCloud {{
    from {{
        left: -200px;
    }}
    to {{
        left: 100%;
    }}
}}

@keyframes floatCloud2 {{
    from {{
        right: -300px;
    }}
    to {{
        right: 100%;
    }}
}}

.cloud-2::before {{
    animation: floatCloud3 25s infinite linear;
    top: 50%;
}}

.cloud-2::after {{
    animation: floatCloud4 35s infinite linear;
    top: 70%;
}}

@keyframes floatCloud3 {{
    from {{
        left: -250px;
    }}
    to {{
        left: 100%;
    }}
}}

@keyframes floatCloud4 {{
    from {{
        right: -280px;
    }}
    to {{
        right: 100%;
    }}
}}

.container {{
    width: 100%;
    max-width: 900px;
    margin-top: 40px;
    animation: slideDown 0.6s ease-out;
    position: relative;
    z-index: 1;
}}

@keyframes slideDown {{
    from {{
        opacity: 0;
        transform: translateY(-30px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

.header {{
    text-align: center;
    margin-bottom: 50px;
}}

.header h1 {{
    font-size: 48px;
    background: linear-gradient(135deg, #ff6b9d 0%, #c44569 25%, #f8b500 50%, #00d9ff 75%, #ff6b9d 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 10px;
    font-weight: 700;
    letter-spacing: -1px;
    animation: gradientShift 6s ease infinite;
}}

@keyframes gradientShift {{
    0% {{
        background-position: 0% 50%;
    }}
    50% {{
        background-position: 100% 50%;
    }}
    100% {{
        background-position: 0% 50%;
    }}
}}

.header p {{
    color: #94a3b8;
    font-size: 16px;
}}

.upload-section {{
    background: linear-gradient(135deg, rgba(51, 65, 85, 0.5), rgba(30, 41, 59, 0.5));
    backdrop-filter: blur(20px);
    border: 1px solid rgba(148, 163, 184, 0.2);
    padding: 40px;
    border-radius: 20px;
    margin-bottom: 40px;
    transition: all 0.3s ease;
}}

.upload-section:hover {{
    border-color: rgba(56, 189, 248, 0.4);
    background: linear-gradient(135deg, rgba(51, 65, 85, 0.6), rgba(30, 41, 59, 0.6));
}}

.upload-section h2 {{
    font-size: 24px;
    margin-bottom: 25px;
    color: #f1f5f9;
}}

.upload-form {{
    display: flex;
    gap: 15px;
    flex-wrap: wrap;
    align-items: center;
}}

.file-input-wrapper {{
    position: relative;
    flex: 1;
    min-width: 200px;
}}

.file-input-wrapper input[type="file"] {{
    display: none;
}}

.file-input-label {{
    display: flex;
    align-items: center;
    justify-content: center;
    padding: 16px 24px;
    background: linear-gradient(135deg, #1e293b, #0f172a);
    border: 2px dashed #38bdf8;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    color: #38bdf8;
    font-weight: 600;
    min-height: 50px;
}}

.file-input-label:hover {{
    border-color: #0ea5e9;
    background: linear-gradient(135deg, #0f172a, #020617);
    color: #0ea5e9;
    box-shadow: 0 0 20px rgba(14, 165, 233, 0.3);
    cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><circle cx="16" cy="16" r="6" fill="%230ea5e9"/><path stroke="%230ea5e9" stroke-width="2" d="M16 2 v28 M2 16 h28" stroke-linecap="round"/></svg>') 16 16, auto;
}}

.file-input-label:active {{
    transform: scale(0.98);
}}

.file-name-display {{
    color: #94a3b8;
    font-size: 14px;
    margin-top: 8px;
}}

.upload-btn {{
    padding: 16px 48px;
    background: linear-gradient(135deg, #38bdf8, #06b6d4);
    border: none;
    border-radius: 12px;
    color: white;
    font-weight: 600;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 8px 16px rgba(56, 189, 248, 0.3);
    min-height: 50px;
}}

.upload-btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 12px 24px rgba(56, 189, 248, 0.5);
    background: linear-gradient(135deg, #0ea5e9, #06b6d4);
    cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><circle cx="16" cy="16" r="5" fill="%23ffffff"/><path stroke="%23ffffff" stroke-width="1.5" d="M16 4 v24 M4 16 h24" stroke-linecap="round"/></svg>') 16 16, auto;
}}

.upload-btn:active {{
    transform: translateY(0);
}}

.files-section {{
    background: linear-gradient(135deg, rgba(51, 65, 85, 0.5), rgba(30, 41, 59, 0.5));
    backdrop-filter: blur(20px);
    border: 1px solid rgba(148, 163, 184, 0.2);
    padding: 40px;
    border-radius: 20px;
    transition: all 0.3s ease;
}}

.files-section h2 {{
    font-size: 24px;
    margin-bottom: 25px;
    color: #f1f5f9;
    display: flex;
    align-items: center;
    gap: 10px;
}}

.file-item {{
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 18px 20px;
    background: linear-gradient(135deg, rgba(51, 65, 85, 0.4), rgba(30, 41, 59, 0.4));
    border: 1px solid rgba(148, 163, 184, 0.1);
    border-radius: 12px;
    margin-bottom: 12px;
    transition: all 0.3s ease;
    animation: fadeIn 0.4s ease-out;
}}

@keyframes fadeIn {{
    from {{
        opacity: 0;
        transform: translateX(-10px);
    }}
    to {{
        opacity: 1;
        transform: translateX(0);
    }}
}}

.file-item:hover {{
    background: linear-gradient(135deg, rgba(51, 65, 85, 0.6), rgba(30, 41, 59, 0.6));
    border-color: rgba(56, 189, 248, 0.3);
    transform: translateX(5px);
    box-shadow: 0 8px 16px rgba(56, 189, 248, 0.2);
}}

.file-info {{
    display: flex;
    align-items: center;
    gap: 15px;
    flex: 1;
}}

.file-icon {{
    font-size: 28px;
}}

.file-details {{
    flex: 1;
}}

.file-name {{
    font-weight: 600;
    color: #f1f5f9;
    word-break: break-all;
    margin-bottom: 4px;
}}

.file-size {{
    font-size: 13px;
    color: #64748b;
}}

.download-btn {{
    padding: 10px 24px;
    background: linear-gradient(135deg, #38bdf8, #06b6d4);
    color: white;
    text-decoration: none;
    border-radius: 8px;
    font-weight: 600;
    transition: all 0.3s ease;
    white-space: nowrap;
    display: inline-block;
    box-shadow: 0 4px 12px rgba(56, 189, 248, 0.2);
}}

.download-btn:hover {{
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(56, 189, 248, 0.4);
    background: linear-gradient(135deg, #0ea5e9, #06b6d4);
    cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><circle cx="16" cy="16" r="5" fill="%23ffffff"/><path stroke="%23ffffff" stroke-width="1.5" d="M16 10 v12 M12 14 l4 4 l4 -4" stroke-linecap="round" stroke-linejoin="round"/></svg>') 16 16, auto;
}}

.empty-state {{
    text-align: center;
    padding: 60px 20px;
    color: #64748b;
}}

.empty-state p {{
    font-size: 18px;
}}

@media (max-width: 600px) {{
    .header h1 {{
        font-size: 36px;
    }}
    
    .upload-form {{
        flex-direction: column;
    }}
    
    .upload-btn {{
        width: 100%;
    }}
    
    .file-item {{
        flex-direction: column;
        align-items: flex-start;
    }}
    
    .download-btn {{
        margin-top: 12px;
        width: 100%;
        text-align: center;
    }}
}}
</style>
</head>

<body>

<div class="container">
    <div class="header">
        <h1>☁️ Cloud Storage</h1>
        <p>Simple, secure, and speedy file management</p>
    </div>

    <div class="upload-section">
        <h2> Upload a File</h2>
        <form action="/upload" method="post" enctype="multipart/form-data" class="upload-form">
            <div class="file-input-wrapper">
                <input type="file" id="fileInput" name="file">
                <label for="fileInput" class="file-input-label">
                    <span>Choose File or Drag & Drop</span>
                </label>
                <div class="file-name-display" id="fileName"></div>
            </div>
            <button type="submit" class="upload-btn">Upload Now</button>
        </form>
    </div>

    <div class="files-section">
        <h2> Your Files</h2>
        {file_items}
        {empty_message}
    </div>
</div>

<script>
    const fileInput = document.getElementById('fileInput');
    const fileNameDisplay = document.getElementById('fileName');
    
    fileInput.addEventListener('change', function() {{
        if (this.files && this.files[0]) {{
            fileNameDisplay.textContent = '✓ Selected: ' + this.files[0].name;
        }}
    }});
    
    // Drag and drop
    const fileLabel = document.querySelector('.file-input-label');
    
    fileLabel.addEventListener('dragover', function(e) {{
        e.preventDefault();
        this.style.borderColor = '#0ea5e9';
        this.style.background = 'rgba(14, 165, 233, 0.1)';
    }});
    
    fileLabel.addEventListener('dragleave', function(e) {{
        e.preventDefault();
        this.style.borderColor = '#38bdf8';
        this.style.background = 'linear-gradient(135deg, #1e293b, #0f172a)';
    }});
    
    fileLabel.addEventListener('drop', function(e) {{
        e.preventDefault();
        this.style.borderColor = '#38bdf8';
        this.style.background = 'linear-gradient(135deg, #1e293b, #0f172a)';
        
        const files = e.dataTransfer.files;
        if (files.length > 0) {{
            fileInput.files = files;
            fileNameDisplay.textContent = '✓ Selected: ' + files[0].name;
        }}
    }});
</script>

</body>
</html>
"""
@app.route("/upload", methods=["POST"])
def upload():
    f = request.files["file"]
    filename = ""
    if f.filename:
        f.save(os.path.join(UPLOAD_FOLDER, f.filename))
        filename = f.filename

    return f"""
<!DOCTYPE html>
<html>
<head>
<title>Upload Successful - Cloud Storage</title>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">

<style>
* {{
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    color: #e2e8f0;
    display: flex;
    justify-content: center;
    align-items: center;
    min-height: 100vh;
    padding: 20px;
    cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><circle cx="16" cy="16" r="6" fill="%2338bdf8"/><path stroke="%2338bdf8" stroke-width="2" d="M16 2 v28 M2 16 h28" stroke-linecap="round"/></svg>') 16 16, auto;
}}

.container {{
    width: 100%;
    max-width: 500px;
    animation: slideDown 0.6s ease-out;
}}

@keyframes slideDown {{
    from {{
        opacity: 0;
        transform: translateY(-30px);
    }}
    to {{
        opacity: 1;
        transform: translateY(0);
    }}
}}

.success-box {{
    background: linear-gradient(135deg, rgba(51, 65, 85, 0.5), rgba(30, 41, 59, 0.5));
    backdrop-filter: blur(20px);
    border: 1px solid rgba(148, 163, 184, 0.2);
    padding: 50px 40px;
    border-radius: 20px;
    text-align: center;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
}}

.success-icon {{
    font-size: 80px;
    margin-bottom: 25px;
    animation: bounce 0.6s ease-out;
}}

@keyframes bounce {{
    0% {{
        transform: scale(0);
        opacity: 0;
    }}
    50% {{
        transform: scale(1.1);
    }}
    100% {{
        transform: scale(1);
        opacity: 1;
    }}
}}

.success-box h1 {{
    font-size: 32px;
    margin-bottom: 15px;
    background: linear-gradient(135deg, #38bdf8, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    font-weight: 700;
}}

.success-box p {{
    color: #94a3b8;
    font-size: 16px;
    margin-bottom: 10px;
}}

.file-name {{
    color: #38bdf8;
    font-weight: 600;
    margin: 20px 0;
    padding: 15px;
    background: linear-gradient(135deg, rgba(56, 189, 248, 0.1), rgba(6, 182, 212, 0.1));
    border-left: 3px solid #38bdf8;
    border-radius: 8px;
    word-break: break-all;
}}

.button-group {{
    display: flex;
    gap: 15px;
    margin-top: 35px;
}}

.btn {{
    flex: 1;
    padding: 14px 28px;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    font-size: 16px;
    cursor: pointer;
    transition: all 0.3s ease;
    text-decoration: none;
    display: inline-block;
}}

.btn-primary {{
    background: linear-gradient(135deg, #38bdf8, #06b6d4);
    color: white;
    box-shadow: 0 8px 16px rgba(56, 189, 248, 0.3);
}}

.btn-primary:hover {{
    transform: translateY(-3px);
    box-shadow: 0 12px 24px rgba(56, 189, 248, 0.5);
    background: linear-gradient(135deg, #0ea5e9, #06b6d4);
    cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><circle cx="16" cy="16" r="5" fill="%23ffffff"/><path stroke="%23ffffff" stroke-width="1.5" d="M16 4 v24 M4 16 h24" stroke-linecap="round"/></svg>') 16 16, auto;
}}

.btn-secondary {{
    background: linear-gradient(135deg, rgba(51, 65, 85, 0.5), rgba(30, 41, 59, 0.5));
    color: #38bdf8;
    border: 1px solid rgba(56, 189, 248, 0.3);
}}

.btn-secondary:hover {{
    transform: translateY(-3px);
    background: linear-gradient(135deg, rgba(51, 65, 85, 0.7), rgba(30, 41, 59, 0.7));
    border-color: rgba(56, 189, 248, 0.6);
    cursor: url('data:image/svg+xml;utf8,<svg xmlns="http://www.w3.org/2000/svg" width="32" height="32" viewBox="0 0 32 32"><circle cx="16" cy="16" r="5" fill="%2338bdf8"/><path stroke="%2338bdf8" stroke-width="1.5" d="M16 4 v24 M4 16 h24" stroke-linecap="round"/></svg>') 16 16, auto;
}}

.btn-secondary:active,
.btn-primary:active {{
    transform: translateY(0);
}}

@media (max-width: 480px) {{
    .success-box {{
        padding: 40px 30px;
    }}
    
    .success-box h1 {{
        font-size: 28px;
    }}
    
    .button-group {{
        flex-direction: column;
    }}
}}
</style>
</head>

<body>

<div class="container">
    <div class="success-box">
        <div class="success-icon"></div>
        <h1>Upload Successful!</h1>
        <p>Your file has been uploaded to the cloud.</p>
        <div class="file-name"> {filename}</div>
        <p style="color: #64748b; font-size: 14px; margin-top: 15px;">Ready to download whenever you need it.</p>
        
        <div class="button-group">
            <a href="/" class="btn btn-primary"> Back to Storage</a>
            <a href="/" class="btn btn-secondary">Upload More</a>
        </div>
    </div>
</div>

</body>
</html>
"""
@app.route("/files/<name>")
def files(name):
    return send_from_directory(UPLOAD_FOLDER, name, as_attachment=True)
app.run(host="0.0.0.0", port=8000)