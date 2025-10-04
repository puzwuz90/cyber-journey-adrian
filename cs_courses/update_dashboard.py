import os
import re
from datetime import datetime, timedelta

# ==============================================================
# CONFIG
# ==============================================================

course_files = [
    'cs_courses/math208_ND.md',
    'cs_courses/cs161_OSU.md'
]
summary_file = 'cs_courses/coursework_dashboard.md'

course_map = {
    "cs161 osu": "CS 161 (OSU)",
    "math208 nd": "Math 208 (UND)"
}

# ==============================================================
# HELPERS
# ==============================================================

def make_bar(completed, total, bar_len=10):
    if total == 0:
        return "░" * bar_len
    filled = int(round((completed / total) * bar_len))
    return "█" * filled + "░" * (bar_len - filled)

def count_progress_and_next(file_path):
    total = 0
    completed = 0
    next_due = None

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            # | Date | Task | [ ] |
            match = re.search(r'\|\s*([^|]+)\s*\|\s*([^|]+)\s*\|\s*(\[[xX ]\])', line)
            if match:
                total += 1
                date_str, task, status = match.groups()

                if 'x' in status.lower():
                    completed += 1
                else:
                    try:
                        due_date = datetime.strptime(date_str.strip() + " 2025", "%b %d %Y")
                        if next_due is None or due_date < next_due[0]:
                            next_due = (due_date, task.strip())
                    except ValueError:
                        continue

    percent = round((completed / total) * 100, 1) if total > 0 else 0.0
    return total, completed, percent, next_due


# ==============================================================
# MAIN
# ==============================================================

progress_data = []
overall_total = 0
overall_completed = 0

for course_file in course_files:
    if os.path.exists(course_file):
        total, completed, percent, next_due = count_progress_and_next(course_file)
        base_name = os.path.splitext(os.path.basename(course_file))[0].replace('_', ' ')
        course_name = course_map.get(base_name.lower(), base_name.title())
        bar = make_bar(completed, total)

        # Highlight urgent tasks (due within 5 days)
        next_due_str = "🎉 All done!"
        if next_due:
            days_left = (next_due[0] - datetime.utcnow()).days
            if days_left <= 5:
                next_due_str = f"🔥 **{next_due[1]} — {next_due[0].strftime('%b %d, %Y')}**"
            else:
                next_due_str = f"{next_due[1]} — {next_due[0].strftime('%b %d, %Y')}"

        progress_data.append((course_name, total, completed, f"{percent}%", bar, next_due_str))
        overall_total += total
        overall_completed += completed

overall_percent = round((overall_completed / overall_total) * 100, 1) if overall_total > 0 else 0.0
timestamp = datetime.utcnow().strftime("%b %d, %Y at %H:%M UTC")

# ==============================================================
# WRITE DASHBOARD
# ==============================================================

with open(summary_file, 'w', encoding='utf-8') as f:
    f.write(f"# 📚 Coursework Dashboard (Fall 2025)\n")
    f.write(f"_Last updated: {timestamp}_\n\n")
    f.write(f"🧮 **Overall Progress:** {overall_completed} / {overall_total} tasks completed "
            f"({overall_percent}%)\n\n")

    f.write("| Course | Total | Completed | Progress | Visual | Next Due |\n")
    f.write("|--------|--------|------------|-----------|----------|-----------|\n")

    for course_name, total, completed, percent, bar, next_due in progress_data:
        f.write(f"| {course_name} | {total} | {completed} | {percent} | {bar} | {next_due} |\n")

print("Dashboard contents:\n")
with open(summary_file, 'r', encoding='utf-8') as f:
    print(f.read())
