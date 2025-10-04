import os
import re

course_files = ['math208_ND.md', 'cs161_OSU.md']
summary_file = 'coursework_dashboard.md'

def count_progress(file_path):
    total = 0
    completed = 0
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            match = re.match(r'\|.*\|.*\|\s*(\[\s?x?\s?\])\s*\|', line, re.IGNORECASE)
            if match:
                total += 1
                if match.group(1).lower() == '[x]':
                    completed += 1
    return total, completed

progress_data = []
for course_file in course_files:
    if os.path.exists(course_file):
        total, completed = count_progress(course_file)
        percent = round((completed / total) * 100, 1) if total > 0 else 0.0
        course_name = os.path.splitext(os.path.basename(course_file))[0].replace('_', ' ').title()
        progress_data.append((course_name, total, completed, f"{percent}%"))

with open(summary_file, 'w', encoding='utf-8') as f:
    f.write("# Coursework Summary Dashboard\n\n")
    f.write("| Course | Total Lessons | Completed | Progress |\n")
    f.write("|--------|---------------|-----------|----------|\n")
    for course_name, total, completed, percent in progress_data:
        f.write(f"| {course_name} | {total} | {completed} | {percent} |\n")
