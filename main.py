from urllib.parse import quote
import requests
from bs4 import BeautifulSoup
import shutil
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas

YELLOW = '\033[93m'
BLUE = '\033[94m'
RESET = '\033[0m'
PURPLE = '\033[0;35m'

def format_url(course_name, page=1):
    quoted_course_name = quote(course_name)
    url = f"https://freecoursesite.com/page/{page}/?s={quoted_course_name}"
    return url

def save_to_pdf(courses, file_name="courses.pdf"):
    c = canvas.Canvas(file_name, pagesize=letter)
    width, height = letter
    c.setFont("Helvetica", 10)
    y_position = height - 40  
    
    for course in courses:
        title = course.get_text().strip()
        link = course.find('a')['href'].strip()
        
        c.drawString(30, y_position, title)
        y_position -= 10
        c.drawString(30, y_position, link)
        y_position -= 20  
        
        if y_position < 40:  
            c.showPage()
            y_position = height - 40
            c.setFont("Helvetica", 10)
    
    c.save()

def get_all_course_links(course_name):
    page = 1
    all_courses = []
    
    while True:
        url = format_url(course_name, page)
        response = requests.get(url)
        if response.status_code != 200:
            break 
        
        soup = BeautifulSoup(response.text, 'html.parser')
        courses = soup.find_all('h2', class_='title')
        terminal_width = shutil.get_terminal_size().columns
        title_width = terminal_width // 8
        link_width = terminal_width - title_width - 8
    
        print("-" + "-" * (title_width + 2) + "-" + "-" * (link_width + 2) + "-")
        for course in courses:
            title = course.get_text().strip()
            link = course.find('a')['href'].strip()
            print("| " + YELLOW + "{:<{}}".format(title, title_width) + RESET, end="\n| ")
            print(BLUE + "{:<{}}".format(link, link_width) + RESET)
            print("🔓" + "-" * (title_width + 2) + "-" + "-" * (link_width + 2) + "-")
        if not courses:
            break  
        
        all_courses.extend(courses)
        page += 1
    
    save_to_pdf(all_courses, f"{course_name}.pdf")
    print(PURPLE + f"🤖 Saved all courses to {course_name}.pdf" + RESET)

course_name = input("Enter the course name: ")
get_all_course_links(course_name)
