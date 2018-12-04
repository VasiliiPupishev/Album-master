class ShadowAlbum:
    Name = ""
    Location = ""
    Items = None

    def __init__(self, location, name, list):
        self.Name = name
        self.Location = location
        self.Items = []
        for i in list:
            self.Items.append(i)
