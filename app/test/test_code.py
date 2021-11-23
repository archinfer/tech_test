import src.code_csv_json as code_csv_json

def test_csv_file():
    #test if file is preprocessed rightly and return Success
    file_name = "../../data/data.csv"
    response = code_csv_json.preprocess_file(file_name)
    assert response['status'] == 'Success'

def test_csv_file_wrong_name():
    #test if response Returned is Fail if csv file is wrong/path doesnt exist
    file_name = "data.csv"
    response = code_csv_json.preprocess_file(file_name)
    assert response['status'] == 'Fail'

def test_valid_df():
    #test if Response is Success if csv file is valid
    file_name = "../../data/data.csv"
    response = code_csv_json.preprocess_file(file_name)
    assert response['status'] == 'Success'
    response = code_csv_json.construct_parent_child_hierarchy(response['df'],response['root'])
    assert response['status'] == 'Success'

def test_invalid_df():
    #pass a csv in which Level 1 Label is different than the root label
    file_name = "../../data/invalid_df.csv"
    response = code_csv_json.preprocess_file(file_name)
    assert response['status'] == 'Success'
    response = code_csv_json.construct_parent_child_hierarchy(response['df'],response['root'])
    assert response['status'] == 'Fail'

def test_write_to_disk():
    file_name = "../../data/data.csv"
    response = code_csv_json.preprocess_file(file_name)
    assert response['status'] == 'Success'
    response = code_csv_json.construct_parent_child_hierarchy(response['df'],response['root'])
    assert response['status'] == 'Success'
    response = code_csv_json.write_to_disk(response['json_file'])
    assert response == True
    
