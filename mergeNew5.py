import re
from difflib import SequenceMatcher

def has_overlap(line1, line2, threshold=0.5):
    """Check if there's a significant overlap between the middle portions of line1 and line2."""
    if not line1.strip() or not line2.strip():  # Skip empty lines
        return False
    
    middle1 = line1[len(line1) // 4 : -len(line1) // 4]  # Take the middle half
    middle2 = line2[len(line2) // 4 : -len(line2) // 4]
    
    match_ratio = SequenceMatcher(None, middle1, middle2).ratio()
    return match_ratio >= threshold

def merge_lines(line1, line2):
    """Merge two lines by finding overlap, ignoring the first few words of line2 during matching, but including them in the result."""
    # Split line2 into words and exclude the first few for matching
    words_line2 = line2.split()
    start_offset = min(2, len(words_line2))  # Ignore the first 2 words (or fewer if line2 is very short)
    trimmed_line2 = " ".join(words_line2[start_offset:])

    # Find overlap between trimmed_line2 and line1
    overlap_start = max(0, min(len(line1), len(trimmed_line2)) // 2)
    while not trimmed_line2.startswith(line1[overlap_start:]) and overlap_start < len(line1):
        overlap_start += 1

    # Merge lines, including the original line2 content
    if overlap_start < len(line1):
        merged_line = line1[:overlap_start] + " " + line2
    else:
        merged_line = line1 + " " + line2

    return merged_line.strip()

def clean_line(line):
    """Remove unnecessary newline characters within a line."""
    return re.sub(r'\n+', ' ', line).strip()

def process_file(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()

    merged_lines = []
    current_line = None  # Start with no active line

    for next_line in lines:
        next_line = clean_line(next_line)
        
        # If next_line is empty, treat it as a paragraph break
        if not next_line.strip():
            if current_line:  # Save the current line before breaking the paragraph
                merged_lines.append(current_line)
                current_line = None
            merged_lines.append("")  # Add an empty line to preserve the paragraph break
            continue

        # If there's no current line, initialize it
        if current_line is None:
            current_line = next_line
            continue

        # Compare and merge lines if overlapping
        if has_overlap(current_line, next_line):
            current_line = merge_lines(current_line, next_line)
        else:
            merged_lines.append(current_line)
            current_line = next_line

    # Add the last processed line
    if current_line:
        merged_lines.append(current_line)

    # Write the final output with double newlines between entries
    with open(output_file, 'w') as f:
        f.write("\n\n".join(merged_lines) + "\n\n")

    print(f"Merged file saved as {output_file}")

# Run the function
process_file('output_texts.txt', 'merged_output_texts.txt')
