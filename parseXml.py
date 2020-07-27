import xmltodict

with open("C:\\Users\\KerryChen\\Desktop\\nosql-biosets-master\\tests\\data\\ko00010.xml") as fd:  # 将XML文件装载到dict里面

    doc = xmltodict.parse(fd.read())
    for key, val in doc['pathway'].items():
        #print(key, "=", val)
        if key == 'entry':
            #print(key, '=', val)
            for i in val:
                print(val)

        if key == 'relation':
            for j in val:
                print(j)


