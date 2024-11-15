import re

def has_overlap(line1, line2, threshold=0.5):
    """Check if there's a significant overlap between the middle portions of line1 and line2."""
    middle1 = line1[len(line1) // 4 : -len(line1) // 4]  # Take the middle half
    middle2 = line2[len(line2) // 4 : -len(line2) // 4]
    
    # Compute the similarity by finding the common substring length over the length of the smaller string
    match_length = len(set(middle1.split()) & set(middle2.split()))
    min_length = min(len(middle1.split()), len(middle2.split()))
    
    return match_length / min_length >= threshold

def merge_lines(line1, line2):
    """Merge two lines by keeping the start of line1, middle overlap, and end of line2."""
    # Find overlap between the two lines
    overlap_start = max(0, min(len(line1), len(line2)) // 2)
    while not line2.startswith(line1[overlap_start:]):
        overlap_start += 1
    merged_line = line1[:overlap_start] + line2  # Combine the start of line1 and end of line2
    return merged_line

def process_file(input_file, output_file):
    with open(input_file, 'r') as f:
        lines = f.readlines()
    merged_lines = []
    i = 0
    while i < len(lines) - 1:
        line1, line2 = lines[i].strip(), lines[i + 1].strip()
        if has_overlap(line1, line2):
            # Merge and skip the next line as it is merged into the current line
            merged_line = merge_lines(line1, line2)
            merged_lines.append(merged_line)
            i += 2  # Skip to the next pair
        else:
            merged_lines.append(line1)
            i += 1

    # Add any remaining line that wasn't processed
    if i == len(lines) - 1:
        merged_lines.append(lines[-1].strip())

    with open(output_file, 'w') as f:
        f.write("\n".join(merged_lines))

    print(f"Merged file saved as {output_file}")

# Run the function
process_file('output_texts.txt', 'merged_output_texts.txt')