"""
AI Resume Analyzer
==================
A real working AI tool that analyzes resumes using Claude API.
Extracts skills, experience, and gives job match recommendations.

Author: Pradeep B | AI Engineer
"""

import anthropic
import json
from pathlib import Path


def analyze_resume(resume_text: str, job_description: str = None) -> dict:
    """
    Analyze a resume using Claude API.
    
    Args:
        resume_text: The full text of the resume
        job_description: Optional job description to match against
        
    Returns:
        dict with skills, experience, strengths, gaps, and score
    """
    client = anthropic.Anthropic()

    # Build the prompt
    job_section = ""
    if job_description:
        job_section = f"""
JOB DESCRIPTION TO MATCH AGAINST:
{job_description}
"""

    prompt = f"""You are an expert AI resume analyzer and career coach.
Analyze the following resume and return a JSON response only.

RESUME:
{resume_text}
{job_section}

Return ONLY a JSON object with this exact structure:
{{
  "candidate_name": "extracted name",
  "experience_years": 0,
  "top_skills": ["skill1", "skill2", "skill3", "skill4", "skill5"],
  "technical_skills": ["skill1", "skill2"],
  "soft_skills": ["skill1", "skill2"],
  "strengths": ["strength1", "strength2", "strength3"],
  "improvements": ["improvement1", "improvement2"],
  "job_match_score": 85,
  "job_match_reason": "explanation of score",
  "recommended_roles": ["role1", "role2", "role3"],
  "summary": "2-3 sentence professional summary"
}}"""

    message = client.messages.create(
        model="claude-3-5-sonnet-20241022",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}]
    )

    # Parse the JSON response
    response_text = message.content[0].text
    
    # Clean response if needed
    if "```json" in response_text:
        response_text = response_text.split("```json")[1].split("```")[0]
    elif "```" in response_text:
        response_text = response_text.split("```")[1].split("```")[0]

    return json.loads(response_text.strip())


def print_analysis(result: dict) -> None:
    """Pretty print the resume analysis results."""
    print("\n" + "="*60)
    print("        🤖 AI RESUME ANALYZER — RESULTS")
    print("="*60)
    print(f"\n👤 Candidate    : {result.get('candidate_name', 'N/A')}")
    print(f"📅 Experience   : {result.get('experience_years', 0)} years")
    print(f"🎯 Job Match    : {result.get('job_match_score', 'N/A')}%")
    
    print(f"\n⭐ Top Skills:")
    for skill in result.get("top_skills", []):
        print(f"   • {skill}")

    print(f"\n💪 Strengths:")
    for s in result.get("strengths", []):
        print(f"   ✅ {s}")

    print(f"\n📈 Areas to Improve:")
    for i in result.get("improvements", []):
        print(f"   📌 {i}")

    print(f"\n🚀 Recommended Roles:")
    for role in result.get("recommended_roles", []):
        print(f"   → {role}")

    print(f"\n📝 Summary:\n   {result.get('summary', 'N/A')}")

    if result.get("job_match_score"):
        print(f"\n🎯 Match Reason:\n   {result.get('job_match_reason', 'N/A')}")

    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    # ── SAMPLE RESUME ──
    sample_resume = """
    John Smith
    AI Engineer | john.smith@email.com | LinkedIn: linkedin.com/in/johnsmith

    EXPERIENCE
    Senior AI Engineer — TechCorp (2022–Present)
    - Built LLM-powered applications using LangChain and OpenAI
    - Developed RAG pipelines for enterprise document search
    - Led team of 3 engineers on agentic AI projects

    Data Scientist — DataCo (2020–2022)
    - Built ML models for customer churn prediction
    - Created dashboards using Power BI and Tableau
    - Worked with Python, SQL, Spark

    EDUCATION
    M.S. Computer Science — Stanford University

    SKILLS
    Python, SQL, LangChain, LangGraph, AWS, GCP, RAG, NLP, Power BI
    """

    # ── SAMPLE JOB DESCRIPTION ──
    sample_job = """
    We are looking for an AI Engineer with experience in:
    - LLM applications and prompt engineering
    - RAG pipelines and vector databases
    - AWS or GCP cloud platforms
    - Python and SQL
    - Multi-agent systems
    """

    print("🔍 Analyzing resume with Claude AI...")
    result = analyze_resume(sample_resume, sample_job)
    print_analysis(result)
