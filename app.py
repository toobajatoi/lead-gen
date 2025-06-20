from flask import Flask, request, jsonify, render_template_string, send_from_directory
from flask_cors import CORS
import subprocess
import json
import os
import threading
import time
import csv

app = Flask(__name__)
CORS(app)

scraping_status = {
    'is_running': False,
    'progress': 0,
    'message': 'Waiting to start...',
    'results': [],
    'error': None,
    'last_updated': time.time()
}

def run_scraper(query, max_results):
    """Run the scraper in a separate thread and provide real-time updates."""
    global scraping_status
    
    try:
        # Reset status for new run
        scraping_status.update({
            'is_running': True,
            'progress': 0,
            'message': 'Initializing scraper...',
            'results': [],
            'error': None
        })

        cmd = ['python', '-u', 'lead_generator.py']
        input_data = f"{query}\n{max_results}\n"
        
        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            stdin=subprocess.PIPE,
            text=True,
            encoding='utf-8',
            errors='replace',
            bufsize=1
        )
        
        # Write input to the process's stdin
        process.stdin.write(input_data)
        process.stdin.flush()
        process.stdin.close() # Important to close stdin

        # Real-time monitoring of stdout
        for line in iter(process.stdout.readline, ''):
            clean_line = line.strip()
            if not clean_line:
                continue

            scraping_status['message'] = clean_line
            scraping_status['last_updated'] = time.time()
            
            # Update progress based on output
            if 'Processing' in clean_line and '/' in clean_line:
                try:
                    parts = clean_line.replace(':', ' ').split()
                    current_total = [p for p in parts if '/' in p]
                    if current_total:
                        current, total = map(int, current_total[0].split('/'))
                        scraping_status['progress'] = int((current / total) * 100)
                except (ValueError, IndexError):
                    pass
        
        process.stdout.close()
        return_code = process.wait()

        if return_code == 0:
            scraping_status['message'] = 'Scraping completed successfully! Reading results...'
            scraping_status['progress'] = 100
            
            # Find the latest CSV file for the query
            clean_query_for_filename = "".join(c if c.isalnum() or c in " -" else "" for c in query).replace(' ', '_')
            expected_filename_part = f"leads_{clean_query_for_filename}"
            
            csv_files = [f for f in os.listdir('.') if f.startswith(expected_filename_part) and f.endswith('.csv')]
            
            if csv_files:
                latest_csv = max(csv_files, key=os.path.getctime)
                results = []
                with open(latest_csv, 'r', encoding='utf-8') as file:
                    reader = csv.DictReader(file)
                    for row in reader:
                        results.append(row)
                scraping_status['results'] = results
                scraping_status['message'] = f"Successfully loaded {len(results)} leads."
            else:
                scraping_status['message'] = "Scraping finished, but no results file was found."

        else:
            error_output = process.stderr.read()
            scraping_status['error'] = f'Scraping failed: {error_output}'
            
    except Exception as e:
        scraping_status['error'] = f'A critical error occurred: {str(e)}'
    finally:
        scraping_status['is_running'] = False
        scraping_status['last_updated'] = time.time()


@app.route('/')
def index():
    """Serve the main page"""
    with open('index.html', 'r', encoding='utf-8') as f:
        return f.read()

@app.route('/<path:filename>')
def serve_static(filename):
    """Serve static files (CSS, JS)"""
    if filename in ['style.css', 'script.js']:
        return send_from_directory('.', filename)
    return "File not found", 404

@app.route('/api/start-scraping', methods=['POST'])
def start_scraping():
    """Start the scraping process"""
    global scraping_status
    
    if scraping_status['is_running']:
        return jsonify({'error': 'Scraping is already running'}), 400
    
    data = request.get_json()
    query = data.get('query', '').strip()
    max_results = data.get('max_results', 50)
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400
    
    thread = threading.Thread(target=run_scraper, args=(query, max_results))
    thread.daemon = True
    thread.start()
    
    return jsonify({'message': 'Scraping started successfully'})

@app.route('/api/status')
def get_status():
    """Get the current scraping status"""
    return jsonify(scraping_status)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 