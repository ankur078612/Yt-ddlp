from flask import Flask, request, jsonify, render_template_string
import yt_dlp
import uuid
import os

app = Flask(__name__)

# HTML template
HTML_TEMPLATE = '''
<!DOCTYPE html>
<html>
<head>
    <title>YouTube Downloader</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container {
            max-width: 700px;
            margin: 0 auto;
            background: white;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            overflow: hidden;
        }
        .header {
            background: #ff0000;
            color: white;
            padding: 25px;
            text-align: center;
        }
        .content {
            padding: 30px;
        }
        .input-group {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        input {
            flex: 1;
            padding: 15px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
        }
        button {
            background: #ff0000;
            color: white;
            border: none;
            padding: 15px 25px;
            border-radius: 8px;
            cursor: pointer;
            font-size: 16px;
            font-weight: bold;
            transition: background 0.3s;
        }
        button:hover {
            background: #cc0000;
        }
        #loading {
            display: none;
            text-align: center;
            padding: 15px;
            color: #666;
        }
        #result {
            margin-top: 20px;
            padding: 20px;
            border-radius: 8px;
            min-height: 20px;
        }
        .success {
            background: #d4edda;
            border: 1px solid #c3e6cb;
            color: #155724;
        }
        .error {
            background: #f8d7da;
            border: 1px solid #f5c6cb;
            color: #721c24;
        }
        .info {
            background: #d1ecf1;
            border: 1px solid #bee5eb;
            color: #0c5460;
        }
        @media (max-width: 600px) {
            .input-group {
                flex-direction: column;
            }
            button {
                width: 100%;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>YouTube Video Downloader</h1>
            <p>Download YouTube videos for offline viewing</p>
        </div>
        <div class="content">
            <div class="input-group">
                <input type="text" id="url" placeholder="Paste YouTube URL here...">
                <button onclick="downloadVideo()">Download</button>
            </div>
            <div id="loading">Processing your request...</div>
            <div id="result"></div>
        </div>
    </div>

    <script>
        async function downloadVideo() {
            const urlInput = document.getElementById('url');
            const url = urlInput.value.trim();
            const resultDiv = document.getElementById('result');
            const loadingDiv = document.getElementById('loading');
            
            if (!url) {
                showResult('Please enter a YouTube URL', 'error');
                return;
            }
            
            if (!url.includes('youtube.com') && !url.includes('youtu.be')) {
                showResult('Please enter a valid YouTube URL', 'error');
                return;
            }
            
            loadingDiv.style.display = 'block';
            resultDiv.innerHTML = '';
            
            try {
                const response = await fetch('/api/download', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({ url: url })
                });
                
                const data = await response.json();
                loadingDiv.style.display = 'none';
                
                if (response.ok && data.status === 'success') {
                    showResult(`✓ Success! Video downloaded: ${data.title}`, 'success');
                } else {
                    showResult(`✗ Error: ${data.error || 'Download failed'}`, 'error');
                }
            } catch (error) {
                loadingDiv.style.display = 'none';
                showResult(`✗ Network error: ${error.message}`, 'error');
            }
        }
        
        function showResult(message, type) {
            const resultDiv = document.getElementById('result');
            resultDiv.innerHTML = `<div class="${type}">${message}</div>`;
        }
        
        // Allow Enter key to trigger download
        document.getElementById('url').addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                downloadVideo();
            }
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/api/download', methods=['POST'])
def download_video():
    try:
        # Get URL from request
        data = request.get_json()
        video_url = data.get('url', '').strip()
        
        # Input validation (important for pentest)
        if not video_url:
            return jsonify({'error': 'URL is required'}), 400
            
        if 'youtube.com' not in video_url and 'youtu.be' not in video_url:
            return jsonify({'error': 'Invalid YouTube URL'}), 400
            
        # For pentesting: test this parameter for injection
        download_id = uuid.uuid4().hex[:12]
        
        # YouTube-DL options - pentest point: check format options
        ydl_opts = {
            'format': 'best[height<=720]',  # Limit to 720p for testing
            'outtmpl': f'/tmp/yt_{download_id}.%(ext)s',
            'quiet': True,
            'no_warnings': True
        }
        
        # Process download - pentest area: resource consumption
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract video info (pentest: check what metadata is exposed)
            info_dict = ydl.extract_info(video_url, download=False)
            title = info_dict.get('title', 'Unknown Video')
            
            # Perform actual download
            ydl.download([video_url])
            
        # For pentesting: check file handling and cleanup
        return jsonify({
            'status': 'success',
            'title': title,
            'id': download_id
        })
        
    except yt_dlp.DownloadError as e:
        # Error handling for pentest - check information disclosure
        return jsonify({'error': f'Download error: {str(e)}'}), 400
    except Exception as e:
        # Generic error for pentest
        return jsonify({'error': f'Server error: {str(e)}'}), 500

# Health check endpoint for deployment
@app.route('/health')
def health():
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    print("=" * 50)
    print("YouTube Downloader Server Starting...")
    print("For authorized penetration testing only")
    print("=" * 50)
    print("Server running on: http://localhost:5000")
    print("Health check: http://localhost:5000/health")
    print("=" * 50)
    app.run(debug=True, host='0.0.0.0', port=5000)