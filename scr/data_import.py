#import json5
import spectra.database as db
import scr.strings as tr

def tag_list():
    tag_set = set(["all"])
    for data in db.objects.values():
        if "tags" in data:
            tag_set.update(data["tags"])
    return list(tag_set)

def obj_list(tag, lang):
    names = {}
    for name_0, data in db.objects.items():

        flag = True
        if tag != "all":
            if "tags" in data:
                if tag not in data["tags"]:
                    flag = False
            else:
                flag = False
        
        if flag:
            if "|" in name_0:
                name_1 = "{} [{}]".format(*name_0.split("|"))
            else:
                name_1 = name_0
            if lang != "en":
                index = ""
                if name_1[0] == "(":
                    parts = name_1.split(")", 1)
                    index = parts[0] + ") "
                    name_1 = parts[1].strip()
                elif "/" in name_1:
                    parts = name_1.split("/", 1)
                    index = parts[0] + "/"
                    name_1 = parts[1].strip()
                for obj_name, tranlation in tr.names.items():
                    if name_1.startswith(obj_name):
                        name_1 = name_1.replace(obj_name, tranlation[lang])
                        break
                name_1 = index + name_1
            names.update({name_1: name_0})
    return names
