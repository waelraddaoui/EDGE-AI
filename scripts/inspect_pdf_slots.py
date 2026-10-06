import PyPDF2

pdf_path = r"C:\Users\marie\.gemini\antigravity\brain\1ba22b9c-a45e-477d-93ff-5bd8da06d09f\.user_uploaded\media_1790102723474.pdf"
reader = PyPDF2.PdfReader(pdf_path)

print(f"Total pages: {len(reader.pages)}")

# Extract text line positions on page 2 (Programme & Evaluation)
for p_idx in [0, 1, 2, 3, 4]:
    print(f"\n================ PAGE {p_idx+1} ================")
    items = []
    def visitor(text, cm, tm, fontDict, fontSize):
        t = text.strip()
        if t and t not in ['..', '...', '....']:
            items.append((t, tm[4], tm[5], fontSize))
    reader.pages[p_idx].extract_text(visitor_text=visitor)
    for t, x, y, s in items[:15]:
        print(f"  {t[:35]:35s} | x={x:6.1f} | y={y:6.1f} | size={s}")
