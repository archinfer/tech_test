import json
import pandas as pd
import traceback
import logging
import logging.handlers

class Node(object):
    """A class used to represent an element in store pick menu

    Attributes:
    id : id of the menu element
    label : label/name of the menu element
    link : the link url for the menu element
    """
    
    def __init__(self, id, label, link):
        """Initialize the class object

        Parameters:
        id (int): id for class object
        label (str): label for class object
        link (int): link url for class object
        """

        self.link = link
        self.label = label
        self.id = id
        self.children = []

    def child(self,id, label,link):
        """Check if child class object exist
        If exits, return object
        If not, initialize child class object and append to parent children list

        Parameters:
        id (int): id for class object
        label (str): label for class object
        link (int): link url for class object

        Returns:
        class object : child class object
        """

        child_found = [c for c in self.children if c.label == label]
        if not child_found:
            child = Node(id,label,link)
            self.children.append(child)
        else:
            child = child_found[0]

        return child

    def as_dict(self):
        """Convert class object to dictionary
        
        Returns:
        dictionary : a key value pair of class object as dict
        """
        
        res = {'id': int(self.id),
        "link":self.link,
        "label":self.label}
        
        res['children'] = [c.as_dict() for c in self.children]
        return res

def preprocess_file(file_name):
    """Reads the file in pandas dataframe
    Checks if csv is valid
    Drops empty rows from dataframe
    Initializes the parent class object using first row of csv
    Drops the first row from dataframe

    Parameters:

    filename (str): Name of the csv file

    Returns:
    
    dictionary: A key value pair containing dataframe containing csv data,
    parent root class object and status if the fuction was executed successfully.
    """
    
    try:
        df = pd.read_csv(file_name)
        
        if df.shape[0] == 0 or df.shape[1] == 0:
            log.error("Empty file")
            response ={
                "status":"Fail"
            }
            return response
    except FileNotFoundError as e:
        log.error("Error reading file path")
        response ={
                "status":"Fail"
            }
        return response
    
    df = df.dropna(how='all')
    
    first_row = df.loc[0]
    root = Node(first_row[2],first_row[1],first_row[3])

    df = df.iloc[1: , :]

    response = {
        "df":df,
        "root":root,
        "status":"Success"
    }

    return response

def construct_parent_child_hierarchy(df, root):
    """
    Iterate all rows of dataframes to construct parent-child relationships
    Converts class object to json dumps

    Parameters:
    df (pandas dataframe): dataframe containing child rows
    root (class object): parent class object

    Returns:
    dictionary : Key value pair containg json dumps file of the class object
    having parent-children and status of function if Success or Fail
    """
    try:
        for row in df.iterrows():
            row = row[1].to_frame()
            #check if row level 1 label is equal to parent label
            if (row.iloc[1,0] != root.label):
                response = {
                    "status":"Fail"
                }
                return response

            row = row.dropna()
            no_child = int(row.size/3)-1

            append_child_to_parent(no_child, row, root)
        
        json_file = json.dumps(root.as_dict(), indent=4)
        print(json_file)
        response = {
            "json_file":json_file,
            "status":"Success"
        }

        return response
    
    except Exception as e:
        log.error("Error iterating code")
        log.error(str(e))
        response ={
            "status"=="Fail"
        }
        return response

def append_child_to_parent(no_child, row, root):
    """Append the child object to parent class object

    If first level of child, append directly to parent node
    Else, append child to parents children nodes

    Parameters:
    no_child (int) : Number of child for parent
    row (dataframe) : A pandas dataframe for a row from csv
    root (class object) : parent class object

    """
    for i in range(no_child):
        if (i==0):
            root.child(row.iloc[5,0],row.iloc[4,0],row.iloc[6,0])
            
        elif (i<=2):
            child_found = [c for c in root.children if c.label == row.iloc[(i*3)+1,0]]
            if not child_found:
                child_found = [c for c in root.children if c.label == row.iloc[(i*3)-2,0]]
                child_found[-1].children[-1].child(row.iloc[(i*3)+5,0],row.iloc[(i*3)+4,0],row.iloc[(i*3)+6,0])
            else:
                child_found[0].child(row.iloc[(i*3)+5,0],row.iloc[(i*3)+4,0],row.iloc[(i*3)+6,0])
                
        else:
            for j in range(i-2):
                if(j==0):
                    child_found = [c for c in root.children if c.label == row.iloc[4+(j*3),0]]
                else:
                    child_found = [c for c in child_found[-1].children if c.label == row.iloc[4+(j*3),0]]
            child_found = [c for c in child_found[-1].children if c.label == row.iloc[(i*3)-2,0]]  

            child_found[-1].children[-1].child(row.iloc[(i*3)+5,0],row.iloc[(i*3)+4,0],row.iloc[(i*3)+6,0])

def write_to_disk(json_file):
    """Writes the json to a .json file on disk
    
    Parameters:
    json_file (json dumps): json dumps dictionary
    
    Returns:
    boolean : boolean value if writing to disk was success or failed
    """

    try:
        with open("../../output/output.json", "w") as outfile:
            outfile.write(json_file)
        return True
    except PermissionError as e:
        log.error("Inadequate permissions to write to disk")
        return False
    except Exception as e:
        log.error("Error writing json to disk")
        return False

#Main execution block
try:
    log = logging.getLogger("morrisons_tech_test")
    log.setLevel(10)
    handler = logging.handlers.RotatingFileHandler(
            "../../logs/app.log",
            maxBytes = 104857600,
            backupCount = 5)
    handler.setFormatter(
        logging.Formatter("%(asctime)s - - %(name)s - - [%(levelname)s] %(module)s %(funcName)1s() - %(message)s"))
    log.addHandler(handler)

    file_name = "../../data/data.csv"
    response = preprocess_file(file_name)
    response = construct_parent_child_hierarchy(response['df'], response['root'])
    status = write_to_disk(response['json_file'])
    if status == True:
        log.info("Success")
except Exception as e:
    log.error(traceback.format_exc())
    log.error(str(e))