import os
import uuid
import shutil

class TempDir:
    def __init__(self, base_path=""):
        self.__dir = "666666" + str(uuid.uuid4()) + "/"
        self.__wd = os.path.abspath(base_path)

    ##dir name
    @property
    def dirname(self):
        return self.__dir

    ##working directory
    @property
    def wd(self):
        return self.__wd

    ##full path
    @property
    def path(self):
        return os.path.join(self.wd, self.dirname)
        
    ##create
    def create(self):
        print("Creating directory")
        if not os.path.exists(self.path):
            os.mkdir(self.path)

    ##delete
    def delete(self):
        if os.path.exists(self.path):
            shutil.rmtree(self.path)