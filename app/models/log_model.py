class Log:
    def __init__(self, title, description, category, system_name, created_by, timestamp=None, id=None):
        self.id = id
        self.title = title
        self.description = description
        self.category = category
        self.system_name = system_name
        self.created_by = created_by
        self.timestamp = timestamp