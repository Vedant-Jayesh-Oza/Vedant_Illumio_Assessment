from flask import Flask, render_template, request, redirect, url_for
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.main import load_lookup_table, load_flow_logs, generate_summary

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method :
        lookup_file = request.files['lookup']
        flow_file = request.files['flow_logs']
        
        if lookup_file and flow_file:
            lookup_file.save('data/lookup.txt')
            flow_file.save('data/flow_logs.txt')
            
            lookup_table = load_lookup_table('data/lookup.txt')
            enriched_logs = load_flow_logs('data/flow_logs.txt')
            generate_summary(enriched_logs, 'output/summary.txt')
            
            return redirect(url_for('results'))
    
    return render_template('index.html')

@app.route('/results')
def results():
    try:
        with open('output/summary.txt', 'r') as f:
            summary = f.read()
    except:
        summary = "No results available yet."
    return render_template('results.html')

if __name__ == '__main__':
    os.makedirs('data', exist_ok=True)
    os.makedirs('output', exist_ok=True)
    app.run(debug=True)