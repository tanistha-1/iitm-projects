import sys
import csv
import matplotlib.pyplot as plt
from jinja2 import Template
HEADER = """<!DOCTYPE html>
<html>
<head>
    <title>Output</title>
</head>
<body>
"""
FOOTER = """
</body>
</html>
"""
def generate_student_html(data, student_id):
    student_id = student_id.strip()
    student_data = [row for row in data if row.get('studentid', '').strip() == student_id]
    if not student_data:
        return generate_error_html()

    total_marks = 0
    table_rows = []
    for row in student_data:
        try:
            marks = int(row.get('marks', '0').strip())
            total_marks += marks
            table_rows.append({
                'Student ID': row.get('studentid', ''),
                'Course ID': row.get('courseid', ''),
                'Marks': marks
            })
        except (ValueError, TypeError):
            continue

    template = Template(HEADER + """
<h2>Student Details</h2>
<table border="2">
    <tr><th>Student ID</th><th>Course ID</th><th>Marks</th></tr>
    {% for row in rows %}
    <tr><td>{{ row['Student ID'] }}</td><td>{{ row['Course ID'] }}</td><td>{{ row['Marks'] }}</td></tr>
    {% endfor %}
    <tr><td colspan="2"><b>Total Marks</b></td><td><b>{{ total }}</b></td></tr>
</table>
""" + FOOTER)
    return template.render(rows=table_rows, total=total_marks)

def generate_course_html(data, course_id):
    course_id = course_id.strip()
    course_marks = []

    for row in data:
        if row.get('courseid', '').strip() == course_id:
            try:
                course_marks.append(int(row.get('marks', '0').strip()))
            except (ValueError, TypeError):
                continue

    if not course_marks:
        return generate_error_html()

    avg_marks = round(sum(course_marks) / len(course_marks), 2)
    max_marks = max(course_marks)

    plt.figure()
    plt.hist(course_marks, bins=10, edgecolor='black')
    plt.xlabel("Marks")
    plt.ylabel("Frequency")
    plt.savefig("histogram.png")
    plt.close()

    template = Template(HEADER + """
<h2>Course Details</h2>
<table border="2">
    <tr><th>Average Marks</th><th>Maximum Marks</th></tr>
    <tr><td>{{ avg }}</td><td>{{ max }}</td></tr>
</table>
<img src="histogram.png" alt="Histogram">
""" + FOOTER)
    return template.render(avg=avg_marks, max=max_marks)

def generate_error_html():
    return HEADER + """
<h2>Wrong Inputs</h2>
<p>Something went wrong</p>
""" + FOOTER

def read_csv_file():
    data = []
    try:
        with open("data.csv", newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                n_row = {}
                for k, v in row.items():
                    if k is None or v is None:
                        continue
                    key = k.replace('\ufeff', '').strip().lower().replace(" ", "")
                    n_row[key] = v.strip()
                data.append(n_row)
    except Exception as e:
        print("Error reading CSV:", e)
        return None
    return data

def main():
    if len(sys.argv) != 3:
        with open("output.html", "w") as f:
            f.write(generate_error_html())
        return

    option, identifier = sys.argv[1].strip(), sys.argv[2].strip()
    data = read_csv_file()
    if data is None:
        with open("output.html", "w") as f:
            f.write(generate_error_html())
        return

    if option == "-s":
        html = generate_student_html(data, identifier)
    elif option == "-c":
        html = generate_course_html(data, identifier)
    else:
        html = generate_error_html()

    with open("output.html", "w") as f:
        f.write(html)

if __name__ == '__main__':
    main()