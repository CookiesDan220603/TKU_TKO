
from urllib.parse import unquote
import os
import AlgoTKU
import time
# Ghi lại thời gian bắt đầu
class MainTestTKU:
    @staticmethod
    def main():
        # Input file path
        input_file = MainTestTKU.file_to_path("DB_Utility.txt")
        
        # Output file path
        output_file = "output.txt"
        
        # The parameter k
        k = 10

        # Applying the algorithm
        algo = AlgoTKU.AlgoTKU()
        algo.runAlgorithm(input_file, output_file, k)

    @staticmethod
    def file_to_path(filename):
        url = os.path.join(os.path.dirname(__file__), filename)
        return unquote(url)

if __name__ == "__main__":

    MainTestTKU.main()
