# summarizer.py
import os
import openai
import requests
import subprocess
import json
from typing import Optional, Dict, Any, Tuple
import re
from dataclasses import dataclass
from datetime import datetime

@dataclass
class SummaryResult:
    """Structured output for summaries"""
    introduction: str
    methods: str
    results: str
    conclusion: str
    key_findings: list[str]
    relevance_score: float
    generated_at: datetime
    model_used: str
    error: Optional[str] = None

def extract_sections(text: str) -> Dict[str, str]:
    """Extract structured sections from text using regex"""
    sections = {
        'introduction': '',
        'methods': '',
        'results': '',
        'conclusion': '',
    }
    
    # Patterns for section headers
    patterns = {
        'introduction': r'(?i)introduction:|background:|overview:',
        'methods': r'(?i)methods:|methodology:|materials and methods:',
        'results': r'(?i)results:|findings:|outcomes:',
        'conclusion': r'(?i)conclusion:|discussion:|summary:'
    }
    
    # Find all section starts
    section_starts = []
    for section, pattern in patterns.items():
        matches = list(re.finditer(pattern, text))
        for match in matches:
            section_starts.append((match.start(), section))
    
    # Sort by position in text
    section_starts.sort()
    
    # Extract content between sections
    for i, (start, section) in enumerate(section_starts):
        end = section_starts[i + 1][0] if i < len(section_starts) - 1 else len(text)
        content = text[start:end].strip()
        # Remove the header
        content = re.sub(patterns[section], '', content, flags=re.IGNORECASE).strip()
        sections[section] = content
    
    return sections

def prepare_prompt(title: str, abstract: str, 
                  results: Optional[str] = None, 
                  conclusion: Optional[str] = None) -> str:
    """Prepare a structured prompt for the AI model"""
    prompt = f"""Analyze the following space biology research publication:

Title: {title}

Please provide a comprehensive yet concise summary in the following format:

1. Introduction: Key background and objectives
2. Methods: Main experimental approach
3. Results: Key findings and data
4. Conclusion: Main implications and impact
5. Key Findings: List 3-5 bullet points
6. Space Mission Relevance: How this research applies to future space missions

Content to analyze:
{abstract}

"""
    if results:
        prompt += f"\nDetailed Results:\n{results}\n"
    if conclusion:
        prompt += f"\nDetailed Conclusion:\n{conclusion}\n"
    
    return prompt

def calculate_space_relevance(summary: str) -> float:
    """Calculate relevance score for space missions"""
    relevance_terms = {
        'space': 2.0, 'microgravity': 2.0, 'astronaut': 2.0,
        'mission': 1.5, 'lunar': 1.5, 'mars': 1.5,
        'zero gravity': 1.5, 'radiation': 1.5,
        'cosmic': 1.0, 'weightlessness': 1.0,
        'spaceflight': 2.0, 'space station': 1.5,
        'iss': 1.5, 'space travel': 1.5
    }
    
    score = 0.0
    text = summary.lower()
    
    for term, weight in relevance_terms.items():
        if term in text:
            score += weight
    
    # Normalize to 0-1 range
    return min(score / 10.0, 1.0)

async def summarize_with_openai(title: str, abstract: str, 
                              results: Optional[str] = None, 
                              conclusion: Optional[str] = None) -> SummaryResult:
    """Generate summary using OpenAI's GPT-4"""
    try:
        prompt = prepare_prompt(title, abstract, results, conclusion)
        
        response = await openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a space biology research expert."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1000
        )
        
        summary_text = response.choices[0].message.content
        sections = extract_sections(summary_text)
        
        # Extract key findings
        key_findings = re.findall(r'(?<=•)(.*?)(?=(?:•|\n|$))', summary_text)
        key_findings = [finding.strip() for finding in key_findings if finding.strip()]
        
        relevance = calculate_space_relevance(summary_text)
        
        return SummaryResult(
            introduction=sections['introduction'],
            methods=sections['methods'],
            results=sections['results'],
            conclusion=sections['conclusion'],
            key_findings=key_findings,
            relevance_score=relevance,
            generated_at=datetime.now(),
            model_used="gpt-4"
        )
        
    except Exception as e:
        return SummaryResult(
            introduction="",
            methods="",
            results="",
            conclusion="",
            key_findings=[],
            relevance_score=0.0,
            generated_at=datetime.now(),
            model_used="gpt-4",
            error=str(e)
        )

def summarize_with_ollama(title: str, abstract: str,
                         results: Optional[str] = None,
                         conclusion: Optional[str] = None,
                         model: str = "gpt-oss:20b-cloud") -> SummaryResult:
    """Generate summary using local Ollama model"""
    try:
        prompt = prepare_prompt(title, abstract, results, conclusion)
        
        result = subprocess.run(
            ["ollama", "run", model, prompt],
            capture_output=True,
            text=True,
            check=True,
            timeout=45
        )
        
        summary_text = result.stdout.strip()
        sections = extract_sections(summary_text)
        
        # Extract key findings
        key_findings = re.findall(r'(?<=•)(.*?)(?=(?:•|\n|$))', summary_text)
        key_findings = [finding.strip() for finding in key_findings if finding.strip()]
        
        relevance = calculate_space_relevance(summary_text)
        
        return SummaryResult(
            introduction=sections['introduction'],
            methods=sections['methods'],
            results=sections['results'],
            conclusion=sections['conclusion'],
            key_findings=key_findings,
            relevance_score=relevance,
            generated_at=datetime.now(),
            model_used=model
        )
        
    except subprocess.TimeoutExpired:
        return SummaryResult(
            introduction="",
            methods="",
            results="",
            conclusion="",
            key_findings=[],
            relevance_score=0.0,
            generated_at=datetime.now(),
            model_used=model,
            error="Model timeout error"
        )
    except subprocess.CalledProcessError as e:
        return SummaryResult(
            introduction="",
            methods="",
            results="",
            conclusion="",
            key_findings=[],
            relevance_score=0.0,
            generated_at=datetime.now(),
            model_used=model,
            error=str(e)
        )

async def summarize(title: str, abstract: str, 
             method: str = "openai",
             results: Optional[str] = None,
             conclusion: Optional[str] = None) -> SummaryResult:
    """Main summary function that handles different AI methods"""
    if method == "openai":
        return await summarize_with_openai(title, abstract, results, conclusion)
    elif method == "ollama":
        # Ollama function is synchronous, so no need for await
        return summarize_with_ollama(title, abstract, results, conclusion)
    else:
        return SummaryResult(
            introduction="",
            methods="",
            results="",
            conclusion="",
            key_findings=[],
            relevance_score=0.0,
            generated_at=datetime.now(),
            model_used=method,
            error=f"Unknown method '{method}'. Choose 'openai' or 'ollama'."
        )