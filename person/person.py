import json

class Person:
    src_file = "person/person.json"
    person = None

    def __init__(self):
        self.read_data()
    
    def read_data(self):
        file = open(self.src_file)
        self.person = json.load(file)
        file.close()

    def check_name(self, new_name):
        if new_name==None:
            return True
        for i in range(1, self.person[0]["nums"]+1):
            if self.person[i]["name"]==new_name:
                return True
        return False

    def append_data(self, data):
        if self.check_name(data)==True:
            print ("The name '" + data + "' is already exist!")
            return False
        self.person[0]["nums"] += 1
        tmp = {"id": self.person[0]["nums"], "name": data}
        self.person.append(tmp)
        file = open(self.src_file, "w+")
        file.write(json.dumps(self.person, indent=4))
        file.close()
        return True

    def pop_data(self):
        if self.person[0]["nums"]==0:
            return
        del self.person[self.person[0]["nums"]]
        self.person[0]["nums"] -= 1
        file = open(self.src_file, "w+")
        file.write(json.dumps(self.person, indent=4))
        file.close()
    
person = Person()



