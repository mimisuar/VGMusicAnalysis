THEMEDATA = [{"id":20,"name":"Thriller"},{"id":18,"name":"Science fiction"},{"id":1,"name":"Action"},
{"id":19,"name":"Horror"},{"id":21,"name":"Survival"},{"id":17,"name":"Fantasy"},{"id":22,"name":"Historical"},
{"id":23,"name":"Stealth"},{"id":27,"name":"Comedy"},{"id":28,"name":"Business"},{"id":31,"name":"Drama"},{"id":32,"name":"Non-fiction"},
{"id":35,"name":"Kids"},{"id":33,"name":"Sandbox"},{"id":38,"name":"Open world"},{"id":39,"name":"Warfare"},{"id":41,"name":"4X (explore, expand, exploit, and exterminate)"},
{"id":34,"name":"Educational"},{"id":43,"name":"Mystery"},{"id":40,"name":"Party"},{"id":44,"name":"Romance"},{"id":42,"name":"Erotic"}]

class Theme:
    def __init__(self, id):
        self.id = id
        self.name = ""

        for theme_info in THEMEDATA:
            if theme_info["id"] == id:
                self.name = theme_info["name"]
                break
        else:
            raise Exception("Invalid theme id {}.".format(self.id))

