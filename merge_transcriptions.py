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
    total_items = len(data)

    # Convert data to a sorted list for sequential access
    data_items = list(data.items())

    # Iterate over each item
    for i in range(total_items):
        key1, text1 = data_items[i]
        if key1 in processed_keys:
            continue

        # Initialize merged text with current entry
        merged_text = text1
        overlaps = [key1]

        # Check only sequential previous entries for overlap
        for j in range(i - 1, max(i - 10, -1), -1):  # Look back up to 10 previous entries
            key2, text2 = data_items[j]
            if key2 not in processed_keys and is_core_overlap(text1, text2):
                overlaps.append(key2)
                processed_keys.add(key2)
                
                # Add non-overlapping start/end text from text2
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
    
def extract_texts(input_file, output_file):
    # Load the merged JSON data
    with open(input_file, 'r') as file:
        data = json.load(file)
    
    # Sort entries by key to maintain value order
    sorted_texts = [entry["text"] for key, entry in sorted(data.items(), key=lambda x: int(x[0]))]
    
    # Write the texts to a plain text file with a newline between each
    with open(output_file, 'w') as file:
        file.write("\n\n".join(sorted_texts))
    
    print(f"Extracted texts saved to {output_file}")

# Run the function
merge_transcriptions('transcribed_notes_sorted_by_numeric_keys.json', 'merged_transcriptions.json')

# Run the function (adjust 'merged_transcriptions.json' and 'output_texts.txt' as needed)
extract_texts('merged_transcriptions.json', 'output_texts.txt')