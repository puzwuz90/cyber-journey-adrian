import os
import re

course_files = ['math208_ND.md', 'cs161_OSU.md']
summary_file = 'coursework_dashboard.md'

course_map = {
    "cs161 osu": "CS 161 (OSU)",
    "math208 nd": "Math 208 (UND)"
}

def count_progress(file_path):
    total = 0
    completed = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.search(r'\|\s*(\[\s?x?\s?\])\s*\|', line, re.IGNORECASE)
            if match:
                total += 1
                if 'x' in match.group(1).lower():
                    completed += 1
    return total, completed

progress_data = []
for course_file in course_files:
    if os.path.exists(course_file):
        total, completed = count_progress(course_file)
        percent = round((completed / total) * 100, 1) if total > 0 else 0.0
        base_name = os.path.splitext(os.path.basename(course_file))[0].replace('_', ' ')
        course_name = course_map.get(base_name.lower(), base_name.title())
        progress_data.append((course_name, total, completed, f"{percent}%"))

with open(summary_file, 'w', encoding='utf-8') as f:
    f.write("# Coursework Dashboard\n\n")
    f.write("| Course | Total Tasks | Completed | Progress |\n")
    f.write("|--------|-------------|-----------|----------|\n")
    for course_name, total, completed, percent in progress_data:
        f.write(f"| {course_name} | {total} | {completed} | {percent} |\n")
