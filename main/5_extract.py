import json

def extract_matches(input_path="predicted_matches.json", output_path="top_matches.json", threshold=0.5):
    with open(input_path, "r") as f:
        data = json.load(f)

    top_matches = []
    for entry in data:
        if entry["score"] >= threshold:
            top_matches.append({
                "source": entry["fragment_A"],
                "target": entry["fragment_B"],
                "score": entry["score"]
            })

    print(f"Extracted {len(top_matches)} matches with score >= {threshold}")
    
    with open(output_path, "w") as f:
        json.dump(top_matches, f, indent=2)
    print(f"Saved top matches to {output_path}")

# Run the extraction directly
extract_matches()
