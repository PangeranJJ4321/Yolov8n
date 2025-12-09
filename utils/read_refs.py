import pandas as pd

file_path = r"d:\PANGERAN\rsic\Yolov8n\skripsi_docs\Pothole References.xlsx"
output_path = r"d:\PANGERAN\rsic\Yolov8n\references_output.txt"

try:
    df = pd.read_excel(file_path)
    
    refs = []
    for index, row in df.iterrows():
        val = row.iloc[1] 
        if pd.notna(val) and str(val).strip() != "Referensi (APA Style)":
            refs.append(str(val).strip())

    with open(output_path, "w", encoding="utf-8") as f:
        for i, ref in enumerate(refs):
            f.write(f"[{i+1}] {ref}\n")
    
    print(f"Saved {len(refs)} references to {output_path}")

except Exception as e:
    print(f"Error: {e}")
