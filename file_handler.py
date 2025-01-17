from typing import List, Tuple

# def parse_uploaded_file(file_content: str) -> List[Tuple[List[int], int, List[int]]]:

#     transactions = []
#     for line in file_content.splitlines():
#         if not line.strip():
#             continue
#         items_part, trans_util_part, utils_part = line.strip().split(':')
#         items = list(map(int, items_part.split()))
#         trans_utility = int(trans_util_part)
#         utilities = list(map(int, utils_part.split()))
#         transactions.append((items, trans_utility, utilities))
#     return transactions
def parse_uploaded_file(file_content: str) -> List[Tuple[List[int], int, List[int]]]:
    transactions = []
    previous_line_empty = False

    for line in file_content.splitlines():
        if not line.strip():
            if previous_line_empty:
                continue
            previous_line_empty = True
        else:
            previous_line_empty = False
            
        items_part, trans_util_part, utils_part = line.strip().split(':')
        items = list(map(int, items_part.split()))
        trans_utility = int(trans_util_part)
        utilities = list(map(int, utils_part.split()))
        transactions.append((items, trans_utility, utilities))
    
    return transactions

def save_results_to_file(file_path: str, k_itemsets: List[Tuple[List[int], int]]):

    with open(file_path, 'w') as file:
        for itemset, utility in k_itemsets:
            itemset_str = " ".join(map(str, itemset))
            file.write(f"{itemset_str} #UTIL: {utility}\n")
