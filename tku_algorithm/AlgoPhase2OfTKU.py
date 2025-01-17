import os
from . import StringPair
from sortedcontainers import SortedList
from tku_algorithm.library import CalculateDatabaseInfo, MemoryLogger, RedBlackTree
class AlgoPhase2OfTKU:
    
    def __init__(self):
        self.min_utility = 0
        self.current_k = 0
        self.number_of_transactions = 0
        self.input_file_path = ""
        self.sorted_candidate_path = ""
        self.temporary_file_path_whuis = "HUI.txt"
        self.output_top_k_huis_file_path = ""
        self.delimiter = ":"
        self.num_top_k_hui = 0

    def run_algorithm(self, min_util, transaction_count, current_k, input_path, sorted_candidate_file, output_file):
        self.min_utility = min_util
        self.number_of_transactions = transaction_count
        self.current_k = current_k
        self.input_file_path = input_path
        self.sorted_candidate_path = sorted_candidate_file
        self.output_top_k_huis_file_path = output_file

        # Initialize temporary file
        with open(self.temporary_file_path_whuis, 'w') as temp_file:
            HDB = [[] for _ in range(self.number_of_transactions)]
            BNF = [[] for _ in range(self.number_of_transactions)]

            # Initialization
            self.initialization(HDB, BNF, len(HDB))

            # Read Database into memory
            self.read_database(HDB, BNF, len(HDB), self.input_file_path)

            # Read Candidate from disk
            self.read_candidate_itemsets(HDB, BNF, len(HDB), self.sorted_candidate_path, temp_file)

        # Process the temporary file and write top-k HUIs
        with open(self.temporary_file_path_whuis, 'r') as temp_file, \
             open(self.output_top_k_huis_file_path, 'w') as output_file:

            self.set_number_of_top_k_huis(0)
            for record in temp_file:
                temp = record.split(self.delimiter)

                if int(temp[1]) >= self.min_utility:
                    # Ensure the output is in SPMF format
                    record = record.replace(":", " #UTIL: ")
                    output_file.write(record)
                    self.set_number_of_top_k_huis(self.get_number_of_top_k_huis() + 1)

        # Clean up temporary files
        os.remove(self.temporary_file_path_whuis)
        os.remove(self.sorted_candidate_path)

    def read_candidate_itemsets(self, HDB, BNF, num_trans, CI_path, Lbfw):
          # Assumed import for RedBlackTree and StringPair

        heap = RedBlackTree.RedBlackTree()
        with open(CI_path, 'r') as bf:
            num_HU = 0

            for CIR in bf:
                CI = CIR.split(self.delimiter)
                match_count = 0
                e_utility = 0

                candidate = CI[0].split(" ")
                if int(CI[1]) >= self.min_utility:
                    # For each Candidate, Scan DB
                    for i in range(num_trans):
                        if len(HDB[i]) != 0:
                            match_count = 0
                            p_utility = 0

                            for s in range(len(candidate)):
                                if int(candidate[s]) in HDB[i]:
                                    match_count += 1
                                    index = HDB[i].index(int(candidate[s]))
                                    B = BNF[i]
                                    ben = B[index]
                                    p_utility += ben
                                else:
                                    p_utility = 0
                                    break

                            if match_count == len(candidate):
                                e_utility += p_utility

                    if e_utility >= self.min_utility:
                        Lbfw.write(CI[0] + ":" + str(e_utility) + "\n")
                        self.update_heap(heap, CI[0], e_utility)
                        num_HU += 1

        return num_HU

    def read_database(self, HDB, BNF, num_trans, DB_path):
        with open(DB_path, 'r') as bf:
            trans_count = 0
            for record in bf:
                data = record.split(":")
                transaction = data[0].split(" ")
                benefit = data[2].split(" ")

                for i in range(len(transaction)):
                    HDB[trans_count].append(int(transaction[i]))
                    BNF[trans_count].append(int(benefit[i]))

                trans_count += 1

    def initialization(self, HDB, BNF, num_trans):
        for i in range(num_trans):
            HDB[i] = []
            BNF[i] = []

    def update_heap(self, NCH, HUI, utility):
        if NCH.size < self.current_k:
            NCH.add(StringPair.StringPair2(HUI, utility))
        elif NCH.size >= self.current_k:
            if utility > self.min_utility:
                NCH.add(StringPair.StringPair2(HUI, utility))
                NCH.popMinimum_str()

        if NCH.minimum().y > self.min_utility and NCH.size >= self.current_k:
            self.min_utility = NCH.minimum().y

    def get_number_of_top_k_huis(self):
        return self.num_top_k_hui

    def set_number_of_top_k_huis(self, num_top_k_hui):
        self.num_top_k_hui = num_top_k_hui

