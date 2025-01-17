import os

class CalculateDatabaseInfo:
    def __init__(self, inputPath):
        self.inputPath = inputPath
        self.totalUtility = 0
        self.databaseSize = 0
        self.maxID = 0
        self.sumAllLength = 0
        self.avgLength = 0.0
        self.maxLength = 0
        self.allItem = set()

    def runCalculate(self):
        try:
            with open(self.inputPath, 'r') as br:
                for line in br:
                    line = line.strip()
                    if not line:
                        continue

                    self.databaseSize += 1
                    tokens1 = line.split(":")  # divide into 3 parts
                    tokens2 = tokens1[0].split(" ")  # divide itemsets into items
                    self.totalUtility += int(tokens1[1])
                    self.sumAllLength += len(tokens2)
                    self.maxLength = max(self.maxLength, len(tokens2))

                    for token in tokens2:
                        num = int(token)
                        self.maxID = max(self.maxID, num)
                        self.allItem.add(num)

            self.avgLength = round(self.sumAllLength / self.databaseSize, 2)  # accurate to two decimal places

        except Exception as e:
            print(str(e))
            return False  # failure

        return True

    def outputResult(self, outputPath):
        try:
            with open(outputPath, 'w') as output:
                print("----------Database Information----------")
                print(f"Input file path: {self.inputPath}")
                print(f"Output file path: {outputPath}")
                print(f"Number of transactions: {self.databaseSize}")
                print(f"Total utility: {self.totalUtility}")
                print(f"Number of distinct items: {len(self.allItem)}")
                print(f"Maximum ID of item: {self.maxID}")
                print(f"Average length of transaction: {self.avgLength}")
                print(f"Maximum length of transaction: {self.maxLength}")

                output.write("----------Database Information----------\n")
                output.write(f"Input file path: {self.inputPath}\n")
                output.write(f"Output file path: {outputPath}\n")
                output.write(f"Number of transactions: {self.databaseSize}\n")
                output.write(f"Total utility: {self.totalUtility}\n")
                output.write(f"Number of distinct items: {len(self.allItem)}\n")
                output.write(f"Maximum ID of item: {self.maxID}\n")
                output.write(f"Average length of transaction: {self.avgLength}\n")
                output.write(f"Maximum length of transaction: {self.maxLength}\n")

        except FileNotFoundError as e:
            print(e)

    def getMaxID(self):
        return self.maxID

    def getMaxLength(self):
        return self.maxLength

    def getDBSize(self):
        return self.databaseSize