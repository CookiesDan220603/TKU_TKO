import time
from collections import defaultdict
from queue import PriorityQueue
from .MemoryLogger import MemoryLogger

class Pair:
    def __init__(self, item=0, utility=0):
        self.item = item
        self.utility = utility

class Element:
    def __init__(self, tid, iutils, rutils):
        self.tid = tid
        self.iutils = iutils
        self.rutils = rutils

class UtilityList:
    def __init__(self, item):
        self.item = item
        self.elements = []
        self.sumIutils = 0
        self.sumRutils = 0

    def add_element(self, element):
        self.elements.append(element)
        self.sumIutils += element.iutils
        self.sumRutils += element.rutils

class ItemsetTKO:
    def __init__(self, prefix, item, utility):
        self.prefix = prefix 
        self.item = item
        self.utility = utility

    def get_prefix(self):
        return self.prefix

    def get_item(self):
        return self.item

    def __lt__(self, other):
        if self.utility == other.utility:
            return False 
        return self.utility < other.utility

    def __eq__(self, other):
        return self.utility == other.utility and self.item == other.item and self.prefix == other.prefix

    def __repr__(self):
        return f"{','.join(map(str, self.prefix))},{self.item}"




##CHIẾN LƯỢC RUC
class AlgoTKOBasic:
    def __init__(self):
        self.total_time = 0
        self.hui_count = 0
        self.k = 0
        self.logger = MemoryLogger.getInstance()  
        self.minutility = 0
        self.k_itemsets = PriorityQueue()
        self.map_item_to_twu = defaultdict(int)
        self.top_k_ci_list = []
        self.tid = 0


    def run_algorithm(self, input_path, k):
        start_time = time.time()
        self.minutility = 1
        self.k = k
        self.logger.checkMemory()

        with open(input_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line[0] in ('#', '%', '@'):
                    continue
                items, transaction_utility, _ = line.split(":")
                transaction_utility = int(transaction_utility)
                for item in map(int, items.split()):
                    self.map_item_to_twu[item] += transaction_utility

        list_items = []
        map_item_to_utility_list = {}

        for item, twu in self.map_item_to_twu.items():
            if twu >= self.minutility: 
                ulist = UtilityList(item)
                list_items.append(ulist)
                map_item_to_utility_list[item] = ulist

        list_items.sort(key=lambda ul: (self.map_item_to_twu[ul.item], ul.item))

        with open(input_path, 'r') as file:
            for line in file:
                line = line.strip()
                if not line or line[0] in ('#', '%', '@'):
                    continue

                items, _, utilities = line.split(":")
                items = list(map(int, items.split()))
                utilities = list(map(int, utilities.split()))

                revised_transaction = []
                remaining_utility = 0
                for item, utility in zip(items, utilities):
                    revised_transaction.append(Pair(item, utility))
                    remaining_utility += utility

                revised_transaction.sort(key=lambda pair: (self.map_item_to_twu[pair.item], pair.item))

                for pair in revised_transaction:
                    remaining_utility -= pair.utility
                    if pair.item in map_item_to_utility_list:
                        utility_list = map_item_to_utility_list[pair.item]
                        element = Element(self.tid, pair.utility, remaining_utility)
                        utility_list.add_element(element)
                self.tid += 1
        self.logger.checkMemory()
        self.search([], None, list_items)
        self.logger.checkMemory()
        self.total_time = time.time() - start_time

    def search(self, prefix, pUL, ULs):
        self.logger.checkMemory()
        for i, X in enumerate(ULs):
            if X.sumIutils >= self.minutility:
                self.write_out(prefix, X.item, X.sumIutils)

            if X.sumRutils + X.sumIutils >= self.minutility:
                exULs = []
                for Y in ULs[i + 1:]:
                    exULs.append(self.construct(pUL, X, Y))

                new_prefix = prefix + [X.item]
                self.search(new_prefix, X, exULs)

            if X.sumIutils >= self.minutility:
                self.apply_ruc(X)

    def apply_ruc(self, X):
        """Chiến lược RUC"""
        self.top_k_ci_list.append(X)
        self.top_k_ci_list.sort(key=lambda x: x.sumIutils, reverse=True)

        if len(self.top_k_ci_list) > self.k:
            if self.top_k_ci_list[self.k - 1].sumIutils < self.minutility:
                self.minutility = self.top_k_ci_list[self.k - 1].sumIutils
                self.top_k_ci_list = [item for item in self.top_k_ci_list if item.sumIutils >= self.minutility]
                # print(f"New minutility set to {self.minutility}")

    def write_out(self, prefix, item, utility):
        itemset = ItemsetTKO(prefix, item, utility)
        self.k_itemsets.put(itemset)
        if self.k_itemsets.qsize() > self.k:
            self.k_itemsets.get()
            self.minutility = self.k_itemsets.queue[0].utility

    def construct(self, P, px, py):
        pxyUL = UtilityList(py.item)
        px_elements_map = {ex.tid: ex for ex in px.elements}
        for ey in py.elements:
            ex = px_elements_map.get(ey.tid)
            if ex:
                if not P:
                    eXY = Element(ex.tid, ex.iutils + ey.iutils, ey.rutils)
                    pxyUL.add_element(eXY)
                else:
                    e = next((e for e in P.elements if e.tid == ex.tid), None)
                    if e:
                        eXY = Element(ex.tid, ex.iutils + ey.iutils - e.iutils, ey.rutils)
                        pxyUL.add_element(eXY)
        return pxyUL

    def print_stats(self):
        print("============= TKO-BASIC =============")
        print(f"High-utility itemsets count: {self.k}")
        print(f"Memory ~ {self.logger.getMaxMemory()} MB")
        print(f"Total time: {self.total_time:.2f} s")
        print("====================================")
