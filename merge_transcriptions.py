import json
from difflib import SequenceMatcher

# Define function to check if two strings overlap at their core
def is_core_overlap(text1, text2, threshold=0.5):
    match_ratio = SequenceMatcher(None, text1, text2).ratio()
    return match_ratio >= threshold

def merge_transcriptions(input_file, output_file):
    # Load JSON data
    with open(input_file, 'r') as file:
        data = json.load(file)

    merged_entries = {}
    processed_keys = set()

    # Iterate over each item in the JSON
    for key1, text1 in data.items():
        if key1 in processed_keys:
            continue

        # Initialize merged text with current entry
        merged_text = text1
        overlaps = [key1]

        # Check for overlapping entries
        for key2, text2 in data.items():
            if key1 != key2 and key2 not in processed_keys and is_core_overlap(text1, text2):
                overlaps.append(key2)
                processed_keys.add(key2)
                
                # Add non-overlapping start/end text
                overlap_start = text2 if text2 in merged_text else ""
                merged_text = f"{merged_text} {overlap_start}".strip()

        # Add merged entry to results
        merged_entries[key1] = {
            'text': merged_text,
            'overlaps': overlaps
        }
        processed_keys.add(key1)

    # Save merged entries
    with open(output_file, 'w') as file:
        json.dump(merged_entries, file, indent=4)
    
    print(f"Merged transcriptions saved to {output_file}")

# Run the function (adjust 'input_file.json' and 'output_file.json' paths as needed)
merge_transcriptions('transcribed_notes_sorted_by_numeric_keys.json', 'merged_transcriptions.json')
