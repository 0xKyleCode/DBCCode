import csv


def openCSV(file):
    """
    opens and returns a csv file contents
    """
    firstColumn = []
    secondColumn = []
    with open(file, 'rt') as csvFile:
        reader = csv.reader(csvFile)
        for row in reader:
            if(len(row) != 0 and len(row) != 1):
                if(is_number(row[0])):
                    if(is_number(row[1])):
                        firstColumn.append(float(row[0]))
                        secondColumn.append(float(row[1]))

    return [firstColumn, secondColumn]


def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
