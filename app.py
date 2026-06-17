"""
AI Resume Analyzer — Web Interface
Simple web UI using Flask to upload and analyze resumes.

Author: Pradeep B | AI Engineer
"""

from flask import Flask, request, jsonify, render_template_string
from main import analyze_resume

app = Flask(__name__)

HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>AI Resume Analyzer</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { background: #0a192f; color: #ccd6f6; font-family: 'Segoe UI', sans-serif; padding: 40px 20px; }
        h1 { color: #64ffda; text-align: center; margin-bottom: 8px; font-size: 2rem; }
        p.sub { text-align: center; color: #8892b0; margin-bottom: 40px; }
        .container { max-width: 800px; margin: 0 auto; }
        textarea { width: 100%; background: #112240; border: 1px solid #233554; border-radius: 8px;
                   color: #ccd6f6; padding: 16px; font-size: 14px; resize: vertical; margin-bottom: 16px; }
        button { background: #64ffda; color: #0a192f; border: none; padding: 14px 32px;
                 border-radius: 6px; font-weight: 700; font-size: 16px; cursor: pointer; width: 100%; }
        button:hover { background: #4cd9b7; }
        #result { margin-top: 32px; background: #112240; border: 1px solid #233554;
                  border-radius: 8px; padding: 24px; display: none; }
        .score { font-size: 3rem; color: #64ffda; font-weight: 700; text-align: center; }
        .label { text-align: center; color: #8892b0; margin-bottom: 24px; }
        .section { margin-bottom: 20px; }
        .section h3 { color: #64ffda; margin-bottom: 8px; font-size: 1rem; }
        .tag { display: inline-block; background: rgba(100,255,218,0.1); border: 1px solid #64ffda;
               color: #64ffda; padding: 4px 12px; border-radius: 4px; font-size: 12px; margin: 3px; }
        .item { padding: 6px 0; color: #8892b0; border-bottom: 1px solid #1d3461; }
        .item::before { content: "→ "; color: #64ffda; }
        #loading { text-align: center; color: #64ffda; margin-top: 20px; display: none; }
    </style>
</head>
<body>
<div class="container">
    <h1>🤖 AI Resume Analyzer</h1>
    <p class="sub">Powered by Claude API · Built by Pradeep B</p>

    <textarea id="resume" rows="12" placeholder="Paste your resume text here..."></textarea>
    <textarea id="job" rows="6" placeholder="Paste job description here (optional)..."></textarea>
    <button onclick="analyze()">Analyze Resume with AI →</button>
    <div id="loading">⏳ Analyzing with Claude AI...</div>

    <div id="result">
        <div class="score" id="score"></div>
        <div class="label">Job Match Score</div>
        <div class="section">
            <h3>👤 Candidate</h3>
            <div class="item" id="name"></div>
            <div class="item" id="exp"></div>
        </div>
        <div class="section">
            <h3>⭐ Top Skills</h3>
            <div id="skills"></div>
        </div>
        <div class="section">
            <h3>💪 Strengths</h3>
            <div id="strengths"></div>
        </div>
        <div class="section">
            <h3>📈 Improvements</h3>
            <div id="improvements"></div>
        </div>
        <div class="section">
            <h3>🚀 Recommended Roles</h3>
            <div id="roles"></div>
        </div>
        <div class="section">
            <h3>📝 Summary</h3>
            <p id="summary" style="color:#8892b0;line-height:1.7"></p>
        </div>
    </div>
</div>

<script>
async function analyze() {
    const resume = document.getElementById('resume').value;
    if (!resume.trim()) { alert('Please paste your resume text!'); return; }
    document.getElementById('loading').style.display = 'block';
    document.getElementById('result').style.display = 'none';

    const res = await fetch('/analyze', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            resume: resume,
            job: document.getElementById('job').value
        })
    });
    const data = await res.json();
    document.getElementById('loading').style.display = 'none';

    document.getElementById('score').textContent = (data.job_match_score || 'N/A') + '%';
    document.getElementById('name').textContent = data.candidate_name || 'N/A';
    document.getElementById('exp').textContent = (data.experience_years || 0) + ' years experience';
    document.getElementById('skills').innerHTML = (data.top_skills||[]).map(s=>`<span class="tag">${s}</span>`).join('');
    document.getElementById('strengths').innerHTML = (data.strengths||[]).map(s=>`<div class="item">${s}</div>`).join('');
    document.getElementById('improvements').innerHTML = (data.improvements||[]).map(s=>`<div class="item">${s}</div>`).join('');
    document.getElementById('roles').innerHTML = (data.recommended_roles||[]).map(s=>`<div class="item">${s}</div>`).join('');
    document.getElementById('summary').textContent = data.summary || '';
    document.getElementById('result').style.display = 'block';
}
</script>
</body>
</html>
"""

@app.route("/")
def index():
    return render_template_string(HTML)

@app.route("/analyze", methods=["POST"])
def analyze():
    data = request.json
    result = analyze_resume(data.get("resume", ""), data.get("job", ""))
    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
