import os

dir_path = '/home/cqfnenu/nosql-biosets-master/keggdrug/data/'
filenum = 0
for (root_1, dirs_1, files_1) in os.walk(dir_path):
    for file_name in files_1:
        filenum = filenum + 1

        with open(os.path.join(root_1, file_name), 'r') as f1:
            # line = f1.readline()
            num = 0
            for i in f1:
                num = num + 1
            print(file_name,  num)


