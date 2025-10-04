import os
import re
from datetime import datetime

course_files = ['math208_ND.md', 'cs161_OSU.md']
summary_file = 'coursework_dashboard.md'

course_map = {
    "cs161 osu": "CS 161 (OSU)",
    "math208 nd": "Math 208 (UND)"
}

def count_progress_and_next(file_path):
    total = 0
    completed = 0
    next_due = None

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # Match table rows with: | Date | Task | [ ] |
            match = re.match(r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*(\[\s?x?\s?\])\s*\|', line, re.IGNORECASE)
            if match:
                total += 1
                date_str, task, status = match.groups()

                if 'x' in status.lower():
                    completed += 1
                else:
                    # Try to parse date in format like "Oct 5", "Nov 19", "Dec 3"
                    try:
                        # Add current year (adjust if rolling year is needed)
                        due_date = datetime.strptime(date_str.strip() + " 2025", "%b %d %Y")
                    except ValueError:
                        # If can't parse, just skip this row for next due
                        continue

                    if next_due is None or due_date < next_due[0]:
                        next_due = (due_date, task.strip())

    percent = round((completed / total) * 100, 1) if total > 0 else 0.0
    return total, completed, percent, next_due

progress_data = []
for course_file in course_files:
    if os.path.exists(course_file):
        total, completed, percent, next_due = count_progress_and_next(course_file)
        base_name = os.path.splitext(os.path.basename(course_file))[0].replace('_', ' ')
        course_name = course_map.get(base_name.lower(), base_name.title())

        next_due_str = "All done! 🎉" if not next_due else f"{next_due[1]} — {next_due[0].strftime('%b %d, %Y')}"
        progress_data.append((course_name, total, completed, f"{percent}%", next_due_str))

with open(summary_file, 'w', encoding='utf-8') as f:
    f.write("# Coursework Dashboard\n\n")
    f.write("| Course | Total Tasks | Completed | Progress | Next Due |\n")
    f.write("|--------|-------------|-----------|----------|----------|\n")
    for course_name, total, completed, percent, next_due in progress_data:
        f.write(f"| {course_name} | {total} | {completed} | {percent} | {next_due} |\n")
