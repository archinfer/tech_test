The solution takes csv file and converts them to a nested JSON file with tree structure.

### Folder Structure

```
├──app
|   ├──__init__.py
|   └──code_csv_json.py
├──test
|   ├──__init__.py
|   └──test_code.py
├──data
|   ├──data.csv
|   └──invalid_df.csv
├──logs
|   └──app.log
├──output
|   └──output.json
├──requirements.txt
└──README.md
```

### Language

The solution is written in Python 3.8.10.

## IDE

Visual Studio Code was used as IDE for developing the solution.

1. A class object is created which contains the required fields such as id, link and label. The initial number of children in the object is zero.
2. Once the csv file is read, it is prepocessed to remove the blank rows, create the top level parent which is the first row of the csv file, remove the first row after creating the parent.
3. Next the rows of the file are iterated to to form the child-parent relationships.
4. The resulting object is first converted to a dictionary and written as a json file to disk.

Pytest library is used for creating the Unit tests required by the solution.
