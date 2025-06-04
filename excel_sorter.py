import subprocess
import sys
import re

#package management
def install_and_import(package):
    import importlib
    try:
        importlib.import_module(package)
    except ImportError:
        import pip
        pip.main(['install', package])
    finally:
        globals()[package] = importlib.import_module(package)

install_and_import('openpyxl')



numbers = 0
alphabets = ""
new_cell = []


def separateNumbersAlphabets(kelime):
    global numbers
    numbers = re.findall(r'[0-9]+', kelime)
    global alphabets
    alphabets = re.findall(r'[a-zA-Z]+', kelime)


path = input("your file name = ")

wb_obj = openpyxl.load_workbook(path)

sheet_obj = wb_obj.active

rows = int(input("number of rows = "))
column = int(input("number of columns = "))

print(str(rows) + " x " + str(column))

# openpyxl uses 1-based indexing. include the user supplied limits
for c in range(1, column + 1):
    for r in range(1, rows + 1):
        cell_obj = sheet_obj.cell(row=r, column=c)
        temp_cell = cell_obj.value
        if type(temp_cell) is float:
            print(str(temp_cell) + " num")
            continue
        if type(temp_cell) is int:
            print(str(temp_cell) + " num")
            continue
        if temp_cell is None:
            print("empty")
            continue
        # only process textual values
        if isinstance(temp_cell, str) and temp_cell.isalpha():
            separateNumbersAlphabets(temp_cell)
            print(temp_cell[::-1])
            for k in temp_cell[::-1]:
                if k == "\n":
                    break
                if k == "-":
                    continue
                print(k)
                new_cell.append(k)
            new_cell.reverse()
            if new_cell == []:
                continue
            print(new_cell)
            new_value = "".join(new_cell)
            new_value = new_value.replace(',', '.')
            new_value = new_value.replace('>', ' ')
            new_value = new_value.replace('<', ' ')
            print(new_value)
                
            print(str(r)+" "+str(c))
            cell_obj.value = float(new_value)
            new_cell = []
            #print(temp_cell)
wb_obj.save(filename=path)
