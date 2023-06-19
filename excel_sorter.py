import subprocess
import sys

import re


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


path = input("le nom du fichier = ")

wb_obj = openpyxl.load_workbook(path)

sheet_obj = wb_obj.active
rows = int(input("nombre de lignes = "))
column = int(input("nombre de colonnes = "))

print(str(rows) + " x " + str(column))

for c in range(1, column):
    for r in range(1, rows):
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
        if temp_cell.isalpha:
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