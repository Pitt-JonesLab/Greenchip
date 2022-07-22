import os

class flatfileDB(object):

    def __init__(self, DB_root, delim=','):
        self.DB_root = DB_root
        self.DB_name = os.path.split(self.DB_root)[1]
        self.DB = {self.DB_name: {}}
        self.populate_DB(self.DB_root, self.DB[self.DB_name])
        self.entries = None
        self.delim = delim
        #print(self.DB_root)
        #print(self.DB_name)


    def __str__(self):
        return str(self.DB)

    def populate_DB(self, directory, entries):
        contents = os.listdir(directory)
        for item in contents:
            location = os.path.join(directory, item)
            if item[0] != ".":
                if os.path.isdir(location):


                    entries[item] = {}
                    self.populate_DB(location, entries[item])
                else:
                    #print('Adding '+item)
                    entries[item] = None

    def get_entries(self, DB_section, key):
        if not isinstance(DB_section[key], dict):
            return None
        DB_section = DB_section[key]
        entries = None
        for entry in DB_section:
            temp = self.get_entries(DB_section, entry)
            if temp is not None:
                if entries is None:
                    entries = []
                for item in temp:
                    entries.append((self.delim.join([key, item])))
        if entries is None:
            entries = [key]
        return entries

    def list_entries(self):
        if self.entries is not None:
            return self.entries
        self.entries = []
        DB = self.DB[self.DB_name]
        for item in DB:
            temp = self.get_entries(DB, item)
            for entry in temp:
                self.entries.append(entry)
        return self.entries

    def get_item(self, key, item, item_loader):
        DB = self.DB[self.DB_name]
        keys = key.split(self.delim)
        for key in keys:
            DB = DB[key]

        loader_used = False
        if DB.get(item, None) is None:
            keys.insert(0,self.DB_root)
            keys.append(item)
            path = os.path.join(*keys)
            DB[item] = item_loader(path)
            loader_used = True

        return DB[item], loader_used

    def list_items(self, key):
        DB = self.DB[self.DB_name]
        keys = key.split(self.delim)
        for key in keys:
            DB = DB[key]
        return DB



