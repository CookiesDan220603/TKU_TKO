class TKUTriangularMatrix:
    
    def __init__(self, elementCount):
        """Constructor"""
        self.elementCount = elementCount
        self.matrix = []
        for i in range(elementCount):
            # Allocate an array for each row
            self.matrix.append([0] * (elementCount - i))
    
    def get(self, i, j):
        """Get the value at the position (i, j) in the matrix"""
        return self.matrix[i][j]
    
    def __str__(self):
        """Get the string representation of the matrix"""
        result = []
        for i in range(len(self.matrix)):
            result.append(f"{i}: " + " ".join(map(str, self.matrix[i])))
        return "\n".join(result)
    
    def incrementCount(self, id1, id2, sum):
        """Increment count in the matrix by some value"""
        if id2 < id1:
            self.matrix[id2][self.elementCount - id1 - 1] += sum
        else:
            self.matrix[id1][self.elementCount - id2 - 1] += sum
    
    def getSupportForItems(self, id1, id2):
        """Get the support for some elements in the matrix"""
        if id2 < id1:
            return self.matrix[id2][self.elementCount - id1 - 1]
        else:
            return self.matrix[id1][self.elementCount - id2 - 1]
    
# Testing the class
if __name__ == "__main__":
    a = TKUTriangularMatrix(5)
    print(a)
    
    a.incrementCount(1, 2, 1)
    print("Add {1 2}")
    print(a)
    
    a.incrementCount(1, 2, 1)
    print("Add {1 2}")
    print(a)
    
    a.incrementCount(1, 3, 1)
    print("Add {1 3}")
    print(a)

    a.incrementCount(1, 4, 1)
    print("Add {1 4}")
    print(a)
    
    a.incrementCount(1, 3, 1)
    a.incrementCount(2, 4, 1)
    a.incrementCount(2, 4, 1)
    a.incrementCount(4, 3, 1)
    print(a)
    
    a.incrementCount(0, 2, 1)
    a.incrementCount(0, 3, 1)
    a.incrementCount(0, 4, 1)
    print(a)
