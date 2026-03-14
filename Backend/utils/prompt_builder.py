def build_prompt(project_name: str, analysis: dict) -> str:
    return f"""
You are a senior software architect and code reviewer.

Analyze the provided project analysis data and generate PROFESSIONAL technical documentation.

IMPORTANT RULES:
- Do NOT guess.
- Do NOT use words like: appears, might, likely, possibly, suggests.
- If something is not found in analysis, write: "Not implemented in code".
- Return ONLY valid JSON.
- Do NOT include explanations.
- Do NOT include markdown.

JSON FORMAT:

{{
  "system_purpose": "",
  "tech_stack": {{
    "backend": [],
    "frontend": [],
    "database": [],
    "libraries": []
  }},
  "modules": [
    {{
      "name": "",
      "responsibility": "",
      "files": []
    }}
  ],
  "api_routes": [
    {{
      "route": "",
      "method": "",
      "description": ""
    }}
  ],
  "data_flow": [],
  "architecture": "",
  "security": [],
  "improvements": []
}}

PROJECT NAME:
{project_name}

ANALYSIS DATA:
{analysis}
"""
