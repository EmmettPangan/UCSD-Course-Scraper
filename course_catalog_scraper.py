import requests
from bs4 import BeautifulSoup
import re
import json
from course import Course

# Parses through the immediate siblings of the course_name_tag
# and concatenates them into an overall course description
def get_course_description(course_name_tag):
    course_description = ""
    next_sibling = course_name_tag.find_next_sibling()
    while next_sibling != None and is_description(next_sibling.get("class")):
        course_description += next_sibling.text + "\n"
        next_sibling = next_sibling.find_next_sibling()
    return course_description

def is_description(class_name):
    match class_name:
        case None | "course-descriptions":
            return True
        case "course-description":
            return True
        case "faculty-staff-listing":
            return True
        case _:
            return False

# Given any course id text, returns the list of (department, number, letter)
# tuples that are represented by the course id text
def process_id(course_id_text):
    courses = list()
    course_id_text = course_id_text.replace(" ", "")

    # # For course ids like "Linguistics/American Sign Language (LISL) 1A"
    # match = re.search(r"\(([A-Z]+)\)(.*)$", course_id_text)
    # if match:
    #     course_id_text = match.group(1) + match.group(2)

    # if "-" in course_id_text:
    #     course_list = course_id_text.split("-")
    #     for i in range(len(course_list)):
    #         course_part = course_list[i]
    #         # For course ids like "ECE 145AL-BL-CL"
    #         if re.fullmatch(r"[A-Z]+", course_part):
    #             letter = course_part
    #             for j in range(i - 1, -1, -1):
    #                 match = re.fullmatch(r"([A-Z]+)([0-9]+)[A-Z]*", course_list[j])
    #                 if match:
    #                     department = match.group(1)
    #                     number = match.group(2)
    #                     courses.append((department, number, letter))
    #                     break
    #         # For course ids like "ECE 145AL-BL-CL"
    #         else:
    #             courses.append(process_single_id(course_part))
    # elif "\u2013" in course_id_text:
    #     course_list = course_id_text.split("\u2013")
    #     for i in range(len(course_list)):
    #         course_part = course_list[i]
    #         # For course ids like "VIS 129A\u2013F"
    #         if re.fullmatch(r"[A-Z]", course_part):
    #             last_letter = course_part
    #             for j in range(i - 1, -1, -1):
    #                 match = re.fullmatch(r"([A-Z]+)([0-9]+)([A-Z])", course_list[j])
    #                 if match:
    #                     department = match.group(1)
    #                     number = match.group(2)
    #                     for letter in [chr(i) for i in range(ord(match.group(3)) + 1, ord(last_letter) + 1)]:
    #                         courses.append((department, number, letter))
    #                     break
    #         # For course ids like "SIOC 202A\u2013B"
    #         else:
    #             courses.append(process_single_id(course_part))
    # elif "," in course_id_text:
    #     course_list = course_id_text.split(",")
    #     for i in range(len(course_list)):
    #         course_part = course_list[i]
    #         # For course ids like "LIFR 5B, 5C, 5D"
    #         num_letter_match = re.fullmatch(r"([0-9]+)([A-Z]*)", course_part)
    #         if num_letter_match:
    #             number = num_letter_match.group(1)
    #             letter = num_letter_match.group(2)
    #             # Finds the closest preceding department to match with this number-letter combo
    #             for j in range(i - 1, -1, -1):
    #                 match = re.fullmatch(r"([A-Z]+)[0-9]*[A-Z]*", course_list[j])
    #                 if match:
    #                     department = match.group(1)
    #                     courses.append((department, number, letter))
    #                     break
    #         # For course ids like "ANTH 268, COGR 225A, HIGR 238, PHIL 209A, SOCG 255A"
    #         else:
    #             courses.append(process_single_id(course_part))
    # else:
    #     course_list = course_id_text.split("/")
    #     for i in range(len(course_list)):
    #         course_part = course_list[i]
    #         department_match = re.fullmatch(r"[A-Z]+", course_part)
    #         num_letter_match = re.fullmatch(r"([0-9]+)([A-Z]*)", course_part)
    #         # For course ids like "BENG/BIMM/CSE 181"
    #         if department_match:
    #             department = course_part
    #             # Finds the closest following number-letter combo to match with this department
    #             for j in range(i + 1, len(course_list)):
    #                 match = re.fullmatch(r"[A-Z]*([0-9]+)([A-Z]*)", course_list[j])
    #                 if match:
    #                     number = match.group(1)
    #                     letter = match.group(2)
    #                     courses.append((department, number, letter))
    #                     break
    #         # For course ids like "CHIN 160/260"
    #         elif num_letter_match:
    #             number = num_letter_match.group(1)
    #             letter = num_letter_match.group(2)
    #             # Finds the closest preceding department to match with this number-letter combo
    #             for j in range(i - 1, -1, -1):
    #                 match = re.fullmatch(r"([A-Z]+)[0-9]+[A-Z]*", course_list[j])
    #                 if match:
    #                     department = match.group(1)
    #                     courses.append((department, number, letter))
    #                     break
    #         # For course ids like "BENG 202/CSE 282"
    #         else:
    #             courses.append(process_single_id(course_part))

    # For course ids like "Linguistics/American Sign Language (LISL) 1A"
    invalid_match = re.search(r"\(([A-Z]+)\)(.*)$", course_id_text)
    if invalid_match:
        course_id_text = invalid_match.group(1) + invalid_match.group(2)
    
    if "\u2013" in course_id_text:
        course_components = course_id_text.split("\u2013")
        for i in range(len(course_components)):
            component = course_components[i]
            # For "F" component of "VIS 129A\u2013F"
            if re.fullmatch(r"[A-Z]", component):
                last_letter = component
                preceding_id = nearest_preceding_id(course_components, i - 1)
                if preceding_id != None:
                    department = preceding_id[0]
                    number = preceding_id[1]
                    for letter in [chr(k) for k in range(ord(preceding_id[2]) + 1, ord(last_letter) + 1)]:
                        courses.append((department, number, letter))
            # For "VIS 129A" component of "VIS 129A\u2013F"
            else:
                id_tuple = process_single_id(component)
                if id_tuple != None:
                    courses.append(id_tuple)
    elif "-" in course_id_text:
        course_components = course_id_text.split("-")
        for i in range(len(course_components)):
            component = course_components[i]
            # For "BL" and "CL" components of "ECE 145AL-BL-CL"
            if re.fullmatch(r"[A-Z]+", component):
                letter = component
                preceding_id = nearest_preceding_id(course_components, i - 1)
                if preceding_id != None:
                    department = preceding_id[0]
                    number = preceding_id[1]
                    courses.append((department, number, letter))
            # For "ECE 145AL" component of "ECE 145AL-BL-CL"
            else:
                id_tuple = process_single_id(component)
                if id_tuple != None:
                    courses.append(id_tuple)
    else:
        course_components = re.split(r"[,/]|or", course_id_text)
        for i in range(len(course_components)):
            component = course_components[i]
            department_match = re.fullmatch(r"[A-Z]+", component)
            number_letter_match = re.fullmatch(r"([0-9]+)([A-Z]*)", component)
            # For "BENG" and "BIMM" components of "BENG/BIMM/CSE 181"
            if department_match:
                department = component
                succeeding_id = nearest_succeeding_id(course_components, i + 1)
                if succeeding_id != None:
                    number = succeeding_id[1]
                    letter = succeeding_id[2]
                    courses.append((department, number, letter))
            # For "5B" and "5C" components of "LISL 5A, 5B, 5C"
            # For "260" component of "CHIN 160/260"
            elif number_letter_match:
                number = number_letter_match.group(1)
                letter = number_letter_match.group(2)
                preceding_id = nearest_preceding_id(course_components, i - 1)
                if preceding_id != None:
                    department = preceding_id[0]
                    courses.append((department, number, letter))
            # For all components of "ANTH 268, COGR 225A, HIGR 238, PHIL 209A, SOCG 255A"
            # All full ids are processed here
            else:
                id_tuple = process_single_id(component)
                if id_tuple != None:
                    courses.append(id_tuple)
    return courses

# Given a single, well-formatted id, returns a (department, number, letter) tuple
def process_single_id(course_id_text):
    match = re.fullmatch(r"([A-Z]+)([0-9]+)([A-Z]*)", course_id_text)
    if match:
        department = match.group(1)
        number = match.group(2)
        letter = match.group(3)
        return (department, number, letter)
    else:
        print("Error matching " + course_id_text)
        return

# Given a list of course components and a starting index,
# returns the nearest succeeding complete id as a (department, number, letter) tuple
def nearest_succeeding_id(course_components, start_index):
    for i in range(start_index, len(course_components)):
        id_match = re.fullmatch(r"([A-Z]+)([0-9]+)([A-Z]*)", course_components[i])
        if id_match:
            return (id_match.group(1), id_match.group(2), id_match.group(3))
    print("Could not find a full id while going forward")
    return

# Given a list of course components and a starting index,
# returns the nearest preceding complete id as a (department, number, letter) tuple
def nearest_preceding_id(course_components, start_index):
    for i in range(start_index, -1, -1):
        id_match = re.fullmatch(r"([A-Z]+)([0-9]+)([A-Z]*)", course_components[i])
        if id_match:
            return (id_match.group(1), id_match.group(2), id_match.group(3))
    print("Could not find a full id while going backward")
    return

# Given a units string, returns a list of formatted units
def process_units(course_units_text):
    units = list()
    course_units_text = course_units_text.replace(" ", "")

    # For units like "0\u20134/0\u20134/0\u20134" or "2\u20134/0"
    if "/" in course_units_text:
        units = course_units_text.split("/")
    # For units like "1\u20134, 1\u20134, 1\u20134, 1\u20134, 1\u20134, 1\u20134"
    elif "," in course_units_text and "\u2013" in course_units_text:
        units = course_units_text.split(",")
    # For units like "2 or 4 or 6" or "6, 8, 10" or "1 to 4"
    elif re.search(r"or|,|to", course_units_text):
        match = re.fullmatch(r"([0-9][0-9]?).+?([0-9][0-9]?)", course_units_text)
        if match:
            min = match.group(1)
            max = match.group(2)
            units.append(min + "\u2013" + max)
        else:
            print("Error matching " + course_units_text)
    elif "-" in course_units_text:
        unit_list = course_units_text.split("-")
        first_unit = unit_list[0]
        last_unit = unit_list[len(unit_list) - 1]
        # For units like "4-4-4"
        if first_unit == last_unit:
            units = unit_list
        # For units like "0-2-4"
        else:
            units.append(first_unit + "\u2013" + last_unit)
    # For units like "4"
    else:
        units.append(course_units_text)
    return units


# Returns a list of Course objects given a tag
def create_courses(course_tag):
    courses = list()
    course_text = course_tag.text.strip()

    # # Find the course id
    # match = re.search(r"^(.+?)\.", course_text)
    # if match:
    #     id = match.group(1)
    #     course_text = course_text[match.end():]
    # else:
    #     id = None
    #     print("Error scraping id for " + course_tag.text)
    #     courses.append(Course(course_text, "", "", "", "", ""))
    #     return courses
    # # print("ID = " + id, end = " :: ")

    # # Find the number of units
    # match = re.search(r"\(([^)]+?)\)$", course_text)
    # if match:
    #     units = match.group(1)
    #     course_text = course_text[:match.start()]
    # else:
    #     units = "Unknown"
    #     print("Error scraping units for " + course_tag.text)
    # # print("Units = " + units, end = " :: ")
    
    # # Find the course name
    # name = course_text.strip()
    # # print("Name = " + name)

    # Find the course description
    description = get_course_description(course_tag)
    if description == "":
        print("No description found for " + course_tag.text)

    course_match = re.fullmatch(r"(.+?)\.\s*(.*?)\s*\(([^)]+?)\)", course_text)
    if course_match:
        id = course_match.group(1)
        name = course_match.group(2)
        units = course_match.group(3)
    else:
        print("Formatting error for course: " + course_tag.text)
        courses.append(Course(course_tag.text, "", "", "", "", description))
        return courses
    
    id = process_id(id)
    if not id:
        print("Error processing id for " + course_tag.text)
        courses.append(Course(course_tag.text, "", "", "", "", description))
        return courses
    
    units = process_units(units)
    for i in range(len(id)):
        if i >= len(units):
            courses.append(Course(id[i][0], id[i][1], id[i][2], units[0], name, description))
        else:
            courses.append(Course(id[i][0], id[i][1], id[i][2], units[i], name, description))
    return courses

def scrape_courses(links):
    courses = list()
    for link in links:
        parser = BeautifulSoup(requests.get(link).content, "html.parser", multi_valued_attributes = None)
        course_tags = parser.find_all("p", class_ = "course-name")
        for course_tag in course_tags:
            courses.extend(create_courses(course_tag))
    with open("Courses.json", "w") as file:
        file.write(json.dumps([course.__dict__ for course in courses], indent = 4))
