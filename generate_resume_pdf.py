from fpdf import FPDF
from fpdf.enums import XPos, YPos
import os

class ResumePDF(FPDF):
    def normalize_text(self, text):
        # Replace common unicode characters that Latin-1 can't handle
        return text.replace('\u2013', '-').replace('\u2014', '--').replace('\u2019', "'").replace('\u2018', "'")

    def header(self):
        if self.page_no() == 1:
            self.set_font('Helvetica', 'B', 24)
            self.set_text_color(44, 62, 80)
            self.cell(0, 15, 'Sahil Rathee', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
            self.set_font('Helvetica', 'I', 10)
            self.set_text_color(127, 140, 141)
            self.cell(0, 5, self.normalize_text('(+91) 9992396866 | sahil.artits.rathee@gmail.com'), new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
            self.cell(0, 5, 'Linkedin | Github | Leetcode', new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L')
            self.ln(10)

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 14)
        self.set_text_color(52, 73, 94)
        self.set_fill_color(236, 240, 241)
        self.cell(0, 8, title, new_x=XPos.LMARGIN, new_y=YPos.NEXT, align='L', fill=True)
        self.ln(4)

    def chapter_body(self, body):
        self.set_font('Helvetica', '', 10)
        self.set_text_color(44, 62, 80)
        self.multi_cell(0, 5, self.normalize_text(body))
        self.ln()

    def job_header(self, title, company, dates):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(44, 62, 80)
        self.cell(0, 6, self.normalize_text(f"{title} @ {company}"), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.set_font('Helvetica', 'I', 10)
        self.set_text_color(127, 140, 141)
        self.cell(0, 6, self.normalize_text(dates), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
        self.ln(2)

    def bullet_point(self, text):
        if not text.strip():
            return
        text = self.normalize_text(text)
        self.set_font('Helvetica', '', 10)
        self.set_text_color(44, 62, 80)
        
        start_x = self.l_margin + 5
        self.set_x(start_x)
        self.cell(5, 5, '-', new_x=XPos.RIGHT, new_y=YPos.TOP)
        remaining_width = self.w - self.r_margin - self.get_x()
        
        link = ""
        if "http://" in text or "https://" in text:
            import re
            urls = re.findall(r'(https?://\S+)', text)
            if urls:
                link = urls[0]
                
        self.multi_cell(remaining_width, 5, text, link=link)
        self.set_x(self.l_margin)

pdf = ResumePDF()
pdf.add_page()
pdf.set_auto_page_break(auto=True, margin=15)

with open('_resume.txt', 'r') as f:
    lines = [line.strip() for line in f.readlines()]

# Find sections
education_idx = -1
skills_idx = -1
experience_idx = -1
hobbies_idx = -1

for i, line in enumerate(lines):
    if 'Education' in line: education_idx = i
    if 'Core Skills' in line: skills_idx = i
    if 'Relevant Experience' in line: experience_idx = i
    if 'Hobbies' in line: hobbies_idx = i

# Intro
first_section_idx = min(idx for idx in [education_idx, skills_idx, experience_idx, hobbies_idx] if idx != -1)
info_lines = [line for line in lines[3:first_section_idx] if line.strip()]

if info_lines:
    pdf.chapter_body(" ".join(info_lines))

# Core Skills
if skills_idx != -1:
    pdf.chapter_title('CORE SKILLS')
    end_idx = min(idx for idx in [experience_idx, education_idx, hobbies_idx] if idx > skills_idx)
    for i in range(skills_idx + 1, end_idx):
        line = lines[i]
        if line.startswith('-'):
            pdf.bullet_point(line[1:].strip())
    pdf.ln(5)

# Relevant Experience
if experience_idx != -1:
    pdf.chapter_title('RELEVANT EXPERIENCE')
    end_idx = min(idx for idx in [education_idx, hobbies_idx] if idx > experience_idx)
    for i in range(experience_idx + 1, end_idx):
        line = lines[i]
        if '@' in line and 'from' in line:
            parts = line.split('@')
            job_title = parts[0].strip()
            sub_parts = parts[1].split('from')
            company = sub_parts[0].strip()
            dates = "from " + sub_parts[1].strip()
            pdf.job_header(job_title, company, dates)
        elif line.startswith('-'):
            pdf.bullet_point(line[1:].strip())

# Education
if education_idx != -1:
    pdf.ln(5)
    pdf.chapter_title('EDUCATION')
    pdf.set_font('Helvetica', 'B', 11)
    pdf.cell(0, 6, pdf.normalize_text(lines[education_idx+1]), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', '', 10)
    pdf.cell(0, 6, pdf.normalize_text(lines[education_idx+2]), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.set_font('Helvetica', 'I', 10)
    pdf.cell(0, 6, pdf.normalize_text(lines[education_idx+3]), new_x=XPos.LMARGIN, new_y=YPos.NEXT)
    pdf.ln(5)

# Hobbies
if hobbies_idx != -1:
    pdf.ln(5)
    pdf.chapter_title('HOBBIES & INTERESTS')
    for i in range(hobbies_idx + 1, len(lines)):
        line = lines[i]
        if line.startswith('-'):
            pdf.bullet_point(line[1:].strip())

pdf.output('resume.pdf')
print("resume.pdf generated successfully.")
