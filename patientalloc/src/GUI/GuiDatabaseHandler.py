class GuiDatabaseHandler():
    def __init__(self, app, databaseHandler):
        self.app = app
        self.databaseHandler = databaseHandler

    def loadDatabase(self, folder, file):
        self.app.setStatusbar("Loading database...", field=0)
        database = self.databaseHandler.loadDatabase(folder, file)
        self.app.setStatusbar("Database loaded", field=0)
        return database

    def saveDatabase(self, database, folder, file):
        self.app.setStatusbar("Saving database...", field=0)
        self.databaseHandler.loadDatabase(database, folder, file)
        self.app.setStatusbar("Database saved", field=0)
