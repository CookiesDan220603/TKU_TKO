class MemoryLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(MemoryLogger, cls).__new__(cls)
            cls._instance.maxMemory = 0
        return cls._instance

    @classmethod
    def getInstance(cls):
        if cls._instance is None:
            cls()  # Ensure the instance is created if it doesn't exist yet
        return cls._instance

    def getMaxMemory(self):
        return self.maxMemory

    def reset(self):
        self.maxMemory = 0

    def checkMemory(self):
        import psutil
        process = psutil.Process()
        current_memory = process.memory_info().rss / 1024 / 1024  # Convert to MB
        if current_memory > self.maxMemory:
            self.maxMemory = current_memory
