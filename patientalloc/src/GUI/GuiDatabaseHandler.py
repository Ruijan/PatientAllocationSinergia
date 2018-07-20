class GuiDatabaseHandler():
    def __init__(self, app, databaseHandler):
        self.app = app
        self.databaseHandler = databaseHandler

    def loadDatabase(self, folder, fileName):
        self.app.setStatusbar("Loading database...", field=0)
        database = self.databaseHandler.loadDatabase(folder, fileName)
        self.app.setStatusbar("Database loaded", field=0)
        return database

    def saveDatabase(self, database, folder, fileName):
        self.app.setStatusbar("Saving database...", field=0)
        self.databaseHandler.saveDatabase(database, folder, fileName)
        self.app.setStatusbar("Database saved", field=0)
