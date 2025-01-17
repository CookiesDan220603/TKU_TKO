class StringPair:
    def __init__(self, x, y):
        self.x = x
        self.y = y
    
    def __lt__(self, other):
        return self.y > other.y
class StringPair2:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __lt__(self, other):
        """So sánh dựa trên thuộc tính y."""
        return self.y < other.y

    def __le__(self, other):
        """So sánh nhỏ hơn hoặc bằng dựa trên thuộc tính y."""
        return self < other or self == other

    def __eq__(self, other):
        """Kiểm tra xem hai đối tượng có bằng nhau không."""
        if other is None:
            return False
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        """Trả về chuỗi đại diện cho đối tượng."""
        return f'StringPair({self.x!r}, {self.y})'
    def compareTo(self, other):
        """So sánh hai đối tượng StringPair dựa trên thuộc tính y."""
        return self.y - other.y
