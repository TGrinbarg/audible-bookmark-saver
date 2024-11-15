import re
from difflib import SequenceMatcher

def has_overlap(line1, line2, threshold=0.5):
    """Check if there's a significant overlap between the middle portions of line1 and line2."""
    # Skip if either line is empty
    if not line1.strip() or not line2.strip():
        return False
    
    middle1 = line1[len(line1) // 4 : -len(line1) // 4]  # Take the middle half
    middle2 = line2[len(line2) // 4 : -len(line2) // 4]
    
    # Compute similarity ratio between middle portions of the lines
    match_ratio = SequenceMatcher(None, middle1, middle2).ratio()
    return match_ratio >= threshold

def merge_lines(line1, line2):
    """Merge two lines by keeping the start of line1, middle overlap, and end of line2."""
    # Locate the overlap between the two lines
    overlap_start = max(0, min(len(line1), len(line2)) // 2)
    while not line2.startswith(line1[overlap_start:]) and overlap_start < len(line1):
        overlap_start += 1
    merged_line = line1[:overlap_start] + line2 if overlap_start < len(line1) else line1 + " " + line2
    return merged_line.strip()

def clean_line(line):
    """Remove unnecessary newline characters within a line."""
    return re.sub(r'\n+', ' ', line).strip()

def process_file(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    merged_lines = []
    i = 0
    while i < len(lines) - 1:
        # Clean up lines to remove internal newline characters
        line1, line2 = clean_line(lines[i]), clean_line(lines[i + 1])
        
        # Skip empty lines
        if not line1:
            i += 1
            continue

        if has_overlap(line1, line2):
            # Merge and skip the next line as it is merged into the current line
            merged_line = merge_lines(line1, line2)
            merged_lines.append(merged_line)
            i += 2  # Skip to the next pair
        else:
            merged_lines.append(line1)
            i += 1

    # Add any remaining line that wasn't processed
    if i == len(lines) - 1 and lines[-1].strip():
        merged_lines.append(clean_line(lines[-1]))

    # Add a blank line between each merged line
    with open(output_file, 'w') as f:
        f.write("\n\n".join(merged_lines) + "\n\n")  # Double newline for paragraph spacing

    print(f"Merged file saved as {output_file}")

# Run the function
process_file('output_texts.txt', 'merged_output_texts.txt')
