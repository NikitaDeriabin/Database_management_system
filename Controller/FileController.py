import os


class FileController:
    @staticmethod
    def get_db_file_names():
        return list(filter(lambda x: x.endswith('.db'), os.listdir("resource")))

    @staticmethod
    def delete_db_file(path):
        os.remove(path)
