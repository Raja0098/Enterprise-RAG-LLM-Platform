import json
from core.gemini_client import client
import os



def process_image(image, page):
    prompt = f"""
You are a high-precision OCR system designed for document parsing in a Retrieval-Augmented Generation (RAG) pipeline.

Your task is to extract ALL textual content from the given document page image with maximum fidelity.

---

### 🎯 OBJECTIVE

Extract text exactly as it appears, preserving structure, layout meaning, and relationships between elements.

---

### 🚨 STRICT REQUIREMENTS (MUST FOLLOW)

1. Output MUST be valid JSON only
   - No markdown
   - No comments
   - No backticks
   - No extra text before or after JSON

2. Do NOT summarize, interpret, or modify meaning
   - Extract text exactly as written

3. Preserve full document structure:
   - Paragraphs
   - Line breaks where meaningful
   - Bullet points and numbered lists
   - Section headings
   - Indentation where relevant

4. TABLE HANDLING (CRITICAL — STRICT MODE):

You MUST extract tables with exact structural fidelity.

TABLE EXTRACTION RULES:

        1. Preserve FULL table structure:
        - Maintain exact row-to-row relationships
        - Maintain column alignment across ALL rows
        - Do NOT shift, reorder, or merge columns

        2. Header Handling:
        - Keep header rows clearly separated from data rows
        - If header spans multiple lines, MERGE it into a single aligned header row
        - Ensure column headers align with their respective data columns

        3. Row Integrity:
        - Each row must remain a single logical unit
        - If a row spans multiple lines, MERGE it into ONE row
        - Do NOT break rows across multiple chunks

        4. Column Alignment (VERY IMPORTANT):
        - Use CONSISTENT spacing between columns
        - Ensure each column appears in the same position across all rows
        - Do NOT allow drifting or uneven spacing

        5. Numeric Tables (HIGH PRIORITY):
        - Preserve ALL numeric values EXACTLY
        - Do NOT drop trailing zeros or decimals
        - Keep consistent spacing between numeric columns

        6. Formatting Rules:
        - Represent tables as fixed-width aligned text (monospaced style)
        - Use spaces (NOT tabs, NOT commas, NOT JSON arrays)
        - Keep rows vertically aligned

        7. Do NOT:
        - Convert table into paragraph
        - Convert into JSON
        - Add separators like "|" unless clearly present
        - Compress or summarize

        8. If table is very wide:
        - Preserve ALL columns even if long
        - Do NOT truncate any part

        9. If unsure:
        - Prefer preserving alignment over readability
        - NEVER guess missing values

        10. CRITICAL OUTPUT RULE:
        - The table must look visually aligned when printed
        - All rows must match the same column structure

5. Fix OCR artifacts carefully:
   - Merge broken lines ONLY if they belong to the same sentence
   - Fix hyphenated words split across lines
   - Preserve original wording

6. Headers/Footers:
   - Remove ONLY if clearly repeated across pages
   - Otherwise keep them

7. Do NOT skip ANY content
   - Include small text, footnotes, labels, and annotations

8. If any part is unclear:
   - Return best possible readable extraction
   - Do NOT hallucinate or invent content

9. LINE MERGING FOR TABLES:

- If a table header or row is split across multiple lines, merge them correctly
- Ensure column count remains consistent across rows
- Do NOT allow header/data mismatch

---

### ⚠️ FAILURE CONDITIONS (AVOID)

- Converting tables into plain paragraphs
- Dropping lines or sections
- Adding explanations or formatting
- Changing wording or structure

---

### 📌 OUTPUT FORMAT

Return EXACTLY this JSON structure:

{{
  "page": {page},
  "text": "<FULL extracted text with preserved structure>"
}}
"""

    res = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[prompt, image]
    )

    raw = None

    if hasattr(res, "text") and res.text:
        raw = res.text
    else:
        try:
            raw = res.candidates[0].content.parts[0].text
        except:
            raw = ""

    if not raw:
        print(f"⚠️ Empty response for page {page}")
        return '{"page": %d, "text": ""}' % page
    
    
    with open(f"debug_outputs/raw_page_{page}.txt", "w") as f:
        f.write(raw if raw else "EMPTY")

    return raw


class GeminiPipeline:
    def run(self, images, source, base_url):
        chunks = []
        full_text = ""
        
        all_pages = []
        os.makedirs("debug_outputs", exist_ok=True)

        for i, img in enumerate(images):
            raw = process_image(img, i + 1)

            raw = raw.strip()

            try:
                data = json.loads(raw)
            except Exception:
                # fallback if Gemini returns bad JSON
                data = {
                    "page": i + 1,
                    "text": raw
                }
                
            all_pages.append(data)

            # 🛡️ Ensure text exists
            text = data.get("text") or ""

            # 🛡️ Avoid None crash
            if not isinstance(text, str):
                text = str(text)

            full_text += text

            chunks.append({
                "text": text,
                "metadata": {
                    "page": i + 1,
                    "source": source,
                    "url": f"{base_url}/{source}#page={i+1}",
                    "pipeline": "gemini"
                }
            })
        with open("debug_outputs/parsed_output.json", "w") as f:
            json.dump(all_pages, f, indent=2)

        return chunks, full_text