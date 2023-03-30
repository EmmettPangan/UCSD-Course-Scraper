class Course:
    def __init__(self, department, number, letter, units, name, description):
        self.department = department
        self.number = number
        self.letter = letter
        self.units = units
        self.name = name
        self.description = description

        self.id = department + number + letter
        self.level = int(number) // 100 if number.isdigit() else "-1"

    def __str__(self):
        return self.name + " ({})".format(self.units) + "\n" + self.description