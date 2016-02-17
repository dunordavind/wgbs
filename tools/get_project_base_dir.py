import os


# returns project base dir
# if this file is moved relative to the project root
# then it will provide wrong results
# however, i don't know any other method to make project work
# regardless of where it is located
def get_project_base_dir():
    file_path = os.path.realpath(__file__)
    base_dir_path = os.path.split(os.path.dirname(file_path))[0]
    return base_dir_path
