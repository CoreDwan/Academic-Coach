# Material Extraction Recipes

## Image-based Chinese PDF → text

Many Chinese technical textbook PDFs are scanned images (pypdf returns empty strings).

### Pipeline
```python
import pymupdf  # pip3 install pymupdf

doc = pymupdf.open("textbook.pdf")
for i, page in enumerate(doc):
    text = page.get_text()
    if text.strip():
        print(text)  # text-based page
    else:
        # image-based: convert to PNG for vision_analyze
        pix = page.get_pixmap(dpi=200)
        pix.save(f'/tmp/page_{i}.png')
```

Then use `vision_analyze(image_url=f'/tmp/page_{i}.png', question='提取所有文字内容')` on each image.

### Optimization for long PDFs
- Extract table of contents first (usually first few pages)
- Only extract exam-relevant chapters, skip appendices/index
- Pages with diagrams/figures: ask vision_analyze to describe both text AND diagrams
- For formula-heavy pages, ask specifically for LaTeX or formula extraction

## Pre-existing knowledge mapping detection

When a PPT directory has been converted to HTML (e.g., `Digital-Elec-PPT/`), check for:
- `knowledge_ppt_mapping.json` — maps knowledge point IDs to slide ranges
- `index.html` at root — may list all chapters
- `*.json` files in the directory root

If `knowledge_ppt_mapping.json` exists with structure like:
```json
{
  "ch1-1": { "ppt_path": "ch1/index.html#slide-4", "ppt_slides": "slides 4-12", "title": "数制基础" }
}
```

Then use it directly:
- `id` → key (e.g., "ch1-1")
- `knowledge_point` → `title` field
- `evidence_sources` → `ppt_path` + `ppt_slides`
- `chapter` → derive from key prefix (e.g., "ch1" → "Ch1 ...")
- `module` → `title` field

## PPT ↔ Textbook chapter mapping pattern

Chinese engineering textbooks commonly have PPTs that:
- Skip some textbook chapters (e.g., 绪论/intro not in PPT)
- Split one textbook chapter across multiple PPTs (e.g., textbook Ch5 → PPT ch5 + ch7)
- Merge multiple textbook chapters into one PPT
- Add chapters not in the textbook (e.g., review/practice sessions)

Always build the cross-reference early and record it in `SYLLABUS_ASSETS.md`.
