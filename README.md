# UCSD Course Scraper

Running the `main.py` file will scrape all available course data from [UCSD's Course Catalog](https://catalog.ucsd.edu/front/courses.html)
and store it in a JSON file. Certain courses will have inconsistent formatting, and errors encountered while
scaping these are printed to stdout.

Information scraped about each course includes:
* Department code
* Course number
* Letter modifier
* Number of units
* Course name
* Course description
* Course id (department + number + letter)
* Course level (0 for lower division, 1 for upper division, 2 for graduate)

For example, the course CSE 8A is scraped as follows:
```
"department": "CSE",
"number": "8",
"letter": "A",
"units": "4",
"name": "Introduction to Programming and Computational Problem-Solving I",
"description": "Introductory course for students interested in computer science and programming. Basics of programming including variables, conditionals, loops, functions/methods. Structured data storage such as arrays/lists and dictionaries, including data mutation. Hands-on experience with designing, writing, hand-tracing, compiling or interpreting, executing, testing, and debugging programs. Students solve relevant computational problems using a high-level programming language. CSE 8A is part of a two-course sequence (CSE 8A-B) that is equivalent to CSE 11. Students should take CSE 8B to complete the CSE 8A-B track. Students who have taken CSE 8B or CSE 11 may not take or receive credit for CSE 8A. Students may only receive credit for one of the following: BILD 62, COGS 18, CSE 8A, or CSE 6R. Recommended preparation: No prior programming experience is assumed, but comfort using computers is helpful. Students should consult the \u201cCSE Course Placement Advice\u201d web page for assistance in choosing which CSE course to take first. Prerequisites: restricted to undergraduates. Graduate students will be allowed as space permits.\n",
"id": "CSE8A",
"level": 0
```
