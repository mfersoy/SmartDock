import re

with open("app/main.py", "r") as f:
    content = f.read()

fallback_logic_pattern = r'        # Generate robust mock fallback.*?doc_type = random\.choice\(\["CEK", "NOTER_SATIS_SOZLESMESI", "DOVIZ_KREDISI_TALIMATI"\]\)'
fallback_logic_replacement = """        # Generate robust mock fallback to maintain visual workflow interactivity
        filename_lower = file.filename.lower()
        if any(keyword in filename_lower for keyword in ["doviz", "talimat", "kuveytturk"]):
            doc_type = "DOVIZ_KREDISI_TALIMATI"
        else:
            doc_type = random.choice(["CEK", "NOTER_SATIS_SOZLESMESI", "DOVIZ_KREDISI_TALIMATI"])"""

content = re.sub(fallback_logic_pattern, fallback_logic_replacement, content, flags=re.DOTALL)

with open("app/main.py", "w") as f:
    f.write(content)

