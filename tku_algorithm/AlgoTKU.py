# Import necessary modules
import os
from queue import PriorityQueue
from tku_algorithm.library import CalculateDatabaseInfo, MemoryLogger, RedBlackTree
from tku_algorithm.AlgoPhase2OfTKU import AlgoPhase2OfTKU
from . import StringPair
from . import TKUTriangularMatrix
import time
from sortedcontainers import SortedList
class AlgoTKU:
    # itemCount = 0
    def __init__(self):

        # User Parameters
        self.sortedTopKcandidateFile = "sortedTopKcandidate.txt"
        self.theInputFile = None
        self.theCandidateFile = None
        self.kValue = 0
        self.itemCount = 0
        self.globalMinUtil = 0
        self.arrayTWUItems = []
        self.arrayMIU = []
        self.arrayMAU = []
        self.totalTime = 0
        
        self.patternCount = 0
    def printValues(self):
        print(f"kValue: {self.kValue}")
        print(f"Input File: {self.theInputFile}")
        print(f"Candidate File: {self.theCandidateFile}")
        print(f"Item Count: {self.itemCount}")
        print(f"arrayTWUItems: {self.arrayTWUItems}")
        print(f"arrayMIU: {self.arrayMIU}")
        print(f"arrayMAU: {self.arrayMAU}")
    def runAlgorithm(self, inputFile, outputFile, k):
        start_time = time.time()
        logger = MemoryLogger.getInstance()
        logger.reset()
        self.totalTime = os.times()[4]

        self.globalMinUtil = 0

        # ------------ PHASE 0 -----------------------
        # Calculate statistics about the database, required by the algorithm
        tool = CalculateDatabaseInfo.CalculateDatabaseInfo(inputFile)
        tool.runCalculate()
        print('done run calculate')
        ulist = []

        self.kValue = k
        self.theInputFile = inputFile
        self.theCandidateFile = "topKcandidate.txt"
        self.itemCount = tool.getMaxID() + 1
        self.arrayTWUItems = [0] * self.itemCount
        self.arrayMIU = [0] * self.itemCount
        self.arrayMAU = [0] * self.itemCount
        with open(self.theCandidateFile, 'w') as bfw_CI:
            # Generate P1 & perform Pre_Evaluation
            self.globalMinUtil = self.preEvaluation(
                self.theInputFile, self.arrayTWUItems, self.itemCount,
                self.arrayMIU, self.arrayMAU, self.globalMinUtil, self.kValue
            )
            print(self.globalMinUtil)
            # Build FP-Tree
            tree = self.BuildUPTree(self.arrayTWUItems, self.theInputFile)
            # Calculate how many nodes in the UP-Tree
            tree.traverse_tree(tree.root, 0)

            DSNodeCountHeap = RedBlackTree.VisualRedBlackTree()

            for child in tree.root.childLink:
                Sum_DS = [0] * self.itemCount
                DSItem = child.item
                tree.sum_descendent(child, Sum_DS)

                for j, sum_ds in enumerate(Sum_DS):
                    if sum_ds != 0 and j != DSItem:
                        DS_Value = (self.arrayMIU[j] + self.arrayMIU[DSItem]) * sum_ds
                        self.UpdateNodeCountHeap(DSNodeCountHeap, DS_Value)

            DSNodeCountHeap = RedBlackTree.VisualRedBlackTree()
            ISNodeCountHeap = RedBlackTree.VisualRedBlackTree()

            self.getUlist(self.arrayTWUItems, ulist)
            prefix = ""
            tree.UPGrowth(tree, ulist, prefix, bfw_CI, ISNodeCountHeap, self.arrayTWUItems, self)
            # print("ISNodeCountHeap.size():", ISNodeCountHeap.size)
            for i, twu in enumerate(self.arrayTWUItems):
                if twu >= self.globalMinUtil:
                    # print("item: " , i , " arraytwu: ", +self.arrayTWUItems[i])

                    bfw_CI.write(f"{i}:{twu}\n")

        logger.getInstance().checkMemory()

        
        self.runSortHUIAlgorithm(self.theCandidateFile, self.sortedTopKcandidateFile)
        os.remove(self.theCandidateFile)

        logger.getInstance().checkMemory()

        algoPhase2 = AlgoPhase2OfTKU()
        algoPhase2.run_algorithm(int(self.globalMinUtil), tool.getDBSize(), k, inputFile, self.sortedTopKcandidateFile, outputFile)
        self.patternCount = algoPhase2.get_number_of_top_k_huis()

        logger.getInstance().checkMemory()
        end_time = time.time()
        self.totalTime = end_time -start_time
        self.printStats()

    def runSortHUIAlgorithm(self, theCandidateFile, sortedTopKcandidateFile):
        # Đọc dữ liệu từ file
        with open(theCandidateFile, 'r') as file:
            records = file.readlines()

        # Dùng SortedList để tạo một cấu trúc heap theo giá trị y (dạng giảm dần)
        heap = SortedList()

        # Đọc từng dòng và thêm vào SortedList
        for record in records:
            record = record.strip()  # Loại bỏ ký tự newline
            temp = record.split(":")
            # Tách chuỗi số và giá trị (tách chuỗi trước dấu ":" và sau dấu ":")
            items = temp[0]
            count = int(temp[1])
            heap.add(StringPair.StringPair(items, count))


        # Ghi kết quả vào file sau khi sắp xếp
        with open(sortedTopKcandidateFile, 'w') as file:
            while len(heap) > 0:
                max_pair = heap.pop(0)  # Lấy phần tử lớn nhất (theo count)
                file.write(f"{max_pair.x}:{max_pair.y}\n")

    def printStats(self):
        print("=============  TKU - v.2.26  =============")
        print(f" Total execution time : {self.totalTime} s")
        print(f" Number of top-k high utility patterns : {self.patternCount}")
        print(f" Max memory usage : {MemoryLogger.MemoryLogger.getInstance().getMaxMemory()} MB")
        print("===================================================")

    def preEvaluation(self, HDB, TWU1, num_Item, MinBNF, MaxBNF, mini_utility, pK):
        a = TKUTriangularMatrix.TKUTriangularMatrix(num_Item)

        with open(HDB, 'r') as bfr:
            for transaction in bfr:
                if transaction != None:
                    temp1 = transaction.strip().split(':')
                    temp2 = temp1[0].split(' ')
                    temp3 = temp1[2].split(' ')
                    for s, item in enumerate(temp2):
                        item = int(item)
                        utility = int(temp3[s])

                        if MinBNF[item] == 0:
                            if utility > 0:
                                MinBNF[item] = utility
                        elif MinBNF[item] > utility:
                            MinBNF[item] = utility

                        if MaxBNF[item] < utility:
                            MaxBNF[item] = utility

                        TWU1[item] += int(temp1[1])

                        if s > 0:
                            a.incrementCount(int(temp2[0]), item, int(temp3[0]) + utility)
        logger = MemoryLogger.MemoryLogger().getInstance()
        logger.checkMemory()
        Initial_BUT = self.getInitialUtility(a, num_Item, pK)

        return Initial_BUT

    class HeapEntry:
        def __init__(self, count, priority):
            self.count = count
            self.priority = priority

        def __lt__(self, other):
            return self.priority > other.priority

    def getInitialUtility(self, TM, nItem, K):
        topKList = PriorityQueue()

        count = 0

        for i in range(nItem):
            for j, value in enumerate(TM.matrix[i]):
                if value != 0:
                    if topKList.qsize() < K:
                        count += 1
                        entry = self.HeapEntry(count, value)
                        topKList.put(entry)
                    elif value > topKList.queue[0].priority:
                        count += 1
                        entry = self.HeapEntry(count, value)
                        topKList.put(entry)
                        topKList.get()
        return topKList.queue[0].priority

    def getUlist(self, P1, list):
        for i, value in enumerate(P1):
            if value > 0 and value >= self.globalMinUtil:
                self.InsertItem(list, i, P1)

    def InsertItem(self, list, target, Order):
        if not list:
            list.append(target)
        else:
            for i, item in enumerate(list):
                if Order[target] > Order[item]:
                    list.insert(i, target)
                    return 0
                elif Order[target] == Order[item] and target < item:
                    list.insert(i, target)
                    return 0
                elif i == len(list) - 1:
                    list.append(target)
                    return 0
        return -1

    def sorttrans(self, tran, pre, tranlen, P1):
        for i in range(pre, tranlen - 1):
            for j in range(pre, tranlen - 1):
                if P1[tran[j]] < P1[tran[j + 1]]:
                    tran[j], tran[j + 1] = tran[j + 1], tran[j]
                elif P1[tran[j]] == P1[tran[j + 1]] and tran[j] > tran[j + 1]:
                    tran[j], tran[j + 1] = tran[j + 1], tran[j]

    def sorttrans2(self, tran, bran, pre, tranlen, P1, parent):
        for i in range(pre, tranlen - 1):
            for j in range(pre, tranlen - 1):
                if P1[tran[j]] < P1[tran[j + 1]]:
                    # Swap elements
                    tran[j], tran[j + 1] = tran[j + 1], tran[j]
                    bran[j], bran[j + 1] = bran[j + 1], bran[j]
                elif P1[tran[j]] == P1[tran[j + 1]]:
                    if tran[j] > tran[j + 1]:
                        # Swap elements
                        tran[j], tran[j + 1] = tran[j + 1], tran[j]
                        bran[j], bran[j + 1] = bran[j + 1], bran[j]

    def UpdateNodeCountHeap(self, NCH, NewValue):
        # If the size of the heap is less than the required kValue, add the new value.
        if NCH.size < self.kValue:
            NCH.add(NewValue)
        elif NCH.size >= self.kValue:
            NCH.add(NewValue)
            NCH.popMinimum()
        if( NCH.minimum() > self.globalMinUtil and NCH.size >= self.kValue):
            self.globalMinUtil = NCH.minimum()


    def BuildUPTree(self, P1, HDB):
        NodeCountHeap = RedBlackTree.RedBlackTree()
        tree = self.FPtree(self)
        # Create an instance of FPtree with the root node

        # Read Database again
        with open(HDB, 'r') as fr:
            for transaction in fr:
                transaction = transaction.strip()
                temp1 = transaction.split(":")
                temp2 = temp1[0].split(" ")
                bran = temp1[2].split(" ")
                bran2 = [None] * len(bran)  # Preallocate space for bran2

                tranlen = 0
                tran = [0] * len(temp2)

                for m in range(len(temp2)):
                    if P1[int(temp2[m])] >= self.globalMinUtil:
                        bran2[tranlen] = bran[m]
                        tran[tranlen] = int(temp2[m])
                        tranlen += 1
                self.sorttrans2(tran, bran2, 0, tranlen, P1, self)  # Sort transaction
                tree.instrans3(tran, bran2, tranlen, P1, 1, NodeCountHeap, self)  # Insert transaction to tree
        logger = MemoryLogger.MemoryLogger()
        logger.getInstance().checkMemory()

        return tree

# Truyền đối tượng AlgoTKU cho FPtree
    class TreeNode:
            def __init__(self, item, twu, count):
                self.item = item  # item of node X
                self.count = count  # count of node X
                self.twu = twu  # Total Weight Utility
                self.hLink = None  # horizontal link of node X
                self.parentLink = None  # parent link
                self.childLink = []  # children nodes of node X

    class FPtree:
        
        # # item_count = super().itemCount
        # def __init__(self,parent):
        #     # algo = super().__init__()  # Gọi hàm khởi tạo của lớp cha
        #     print(parent.itemCount)  # Truy cập itemCount ngay sau khi khởi tạo

        def __init__(self,parent):
            self.root = parent.TreeNode(-1,0,0)  # Khởi tạo root
            self.header_table = [None] * parent.itemCount
            self.arrayMIU = [0] * parent.itemCount  # Khởi tạo arrayMIU
            self.globalMinUtil = parent.globalMinUtil  # Sử dụng globalMinUtil từ lớp cha

# Kết thúc lớp FPtree

        def insPatternBase(self, tran, tran_len, L1, TWU, IC, SumBNF, parent):
            par = self.root

            # print(par.childLink)
            for i in range(tran_len):
                target = tran[i]
                cs = len(par.childLink)

                if cs == 0:
                    M = TWU - (SumBNF - parent.arrayMIU[target] * IC)
                    SumBNF -= parent.arrayMIU[target] * IC

                    nNode = parent.TreeNode(target, M, IC)
                    par.childLink.append(nNode)
                    nNode.parentLink = par

                    if self.header_table[target] is None:
                        self.header_table[target] = nNode
                    else:
                        nNode.hLink = self.header_table[target]
                        self.header_table[target] = nNode

                    par = nNode
                else:
                    for j in range(cs):
                        comp = par.childLink[j]

                        if target == comp.item:
                            M = TWU - (SumBNF - parent.arrayMIU[target] * IC)
                            SumBNF -= parent.arrayMIU[target] * IC

                            comp.twu += M
                            comp.count += IC
                            par = comp
                            break
                        elif L1[target] > L1[comp.item]:
                            M = TWU - (SumBNF - parent.arrayMIU[target] * IC)
                            SumBNF -= parent.arrayMIU[target] * IC

                            nNode = parent.TreeNode(target, M, IC)
                            par.childLink.insert(j, nNode)
                            nNode.parentLink = par

                            if self.header_table[target] is None:
                                self.header_table[target] = nNode
                            else:
                                nNode.hLink = self.header_table[target]
                                self.header_table[target] = nNode

                            par = nNode
                            break
                        elif (L1[target] == L1[comp.item]) and (target < comp.item):
                            M = TWU - (SumBNF - parent.arrayMIU[target] * IC)
                            SumBNF -= parent.arrayMIU[target] * IC

                            nNode = parent.TreeNode(target, M, IC)
                            par.childLink.insert(j, nNode)
                            nNode.parentLink = par

                            if self.header_table[target] is None:
                                self.header_table[target] = nNode
                            else:
                                nNode.hLink = self.header_table[target]
                                self.header_table[target] = nNode

                            par = nNode
                            break
                        elif j == (cs - 1):
                            M = TWU - (SumBNF - parent.arrayMIU[target] * IC)
                            SumBNF -= parent.arrayMIU[target] * IC

                            nNode = parent.TreeNode(target, M, IC)
                            par.childLink.append(nNode)
                            nNode.parentLink = par

                            if self.header_table[target] is None:
                                self.header_table[target] = nNode
                            else:
                                nNode.hLink = self.header_table[target]
                                self.header_table[target] = nNode

                            par = nNode
        
        def instrans3(self, tran, bran, tran_len, L1, IC, NodeCountHeap, parent):
            TWU = 0
            par = self.root
            # NodeCountHeap.visualize_tree()
            for i in range(tran_len):
                TWU += int(bran[i])
                target = tran[i]
                cs = len(par.childLink)
                if cs == 0:
                    
                    nNode = parent.TreeNode(target, TWU, IC)
                    # print("nnode : ", nNode.twu, "global : ", self.globalMinUtil)
                    
                    par.childLink.append(nNode)
                    # print(len(par.childLink))
                    # print("1")
                    
                    # print(parent.globalMinUtil)
                    
                    if nNode.twu > parent.globalMinUtil:
                        
                        parent.UpdateNodeCountHeap(NodeCountHeap, nNode.twu)

                    nNode.parentLink = par

                    if self.header_table[target] is None:
                        self.header_table[target] = nNode
                    else:
                        nNode.hLink = self.header_table[target]
                        self.header_table[target] = nNode

                    par = nNode
                else:
                    
                    for j in range(cs):
                        # print(par.childLink[j].twu)
                        comp = par.childLink[j]
                        # print("comp: ",comp.item," target : ", target)
                        if target == comp.item:
                            NodeCountHeap.remove(comp.twu)
                            parent.UpdateNodeCountHeap(NodeCountHeap, comp.twu + TWU)

                            comp.twu += TWU
                            comp.count += IC
                            par = comp
                            break
                        elif L1[target] > L1[comp.item]:
                            if comp.twu > parent.globalMinUtil:
                                parent.UpdateNodeCountHeap(NodeCountHeap, TWU)

                            nNode = parent.TreeNode(target, TWU, IC)
                            par.childLink.insert(j, nNode)

                            nNode.parentLink = par

                            if self.header_table[target] is None:
                                self.header_table[target] = nNode
                            else:
                                nNode.hLink = self.header_table[target]
                                self.header_table[target] = nNode

                            par = nNode
                            break
                        elif (L1[target] == L1[comp.item]) and (target < comp.item):
                            if comp.twu > parent.globalMinUtil:
                                parent.UpdateNodeCountHeap(NodeCountHeap, TWU)

                            nNode = parent.TreeNode(target, TWU, IC)
                            par.childLink.insert(j, nNode)

                            nNode.parentLink = par

                            if self.header_table[target] is None:
                                self.header_table[target] = nNode
                            else:
                                nNode.hLink = self.header_table[target]
                                self.header_table[target] = nNode

                            par = nNode
                            break
                        elif j == (cs - 1):
                            if comp.twu > parent.globalMinUtil:
                                parent.UpdateNodeCountHeap(NodeCountHeap, TWU)

                            nNode = parent.TreeNode(target, TWU, IC)
                            par.childLink.append(nNode)

                            nNode.parentLink = par

                            if self.header_table[target] is None:
                                self.header_table[target] = nNode
                            else:
                                nNode.hLink = self.header_table[target]
                                self.header_table[target] = nNode

                            par = nNode

        def UPGrowth(self, tree, flist, prefix, bfw_UCI, ISNodeCountHeap, LP1, parent):
                # Bottom-up traversal of Header Table
                for i in range(len(flist)):
                    if LP1[flist[i]] >= parent.globalMinUtil:
                        # Nprefix = f"{prefix} {flist[i]}" if prefix else str(flist[i])
                        Nprefix = f"{prefix} {flist[i]}" if prefix else str(flist[i])

                        citem = flist[i]  # get current item
                        chLink = tree.header_table[citem]  # current horizontal link
                        # print("prefix:",Nprefix)
                        # print("")
                        # print("flist[i]:", flist[i])
                        # print()
                        # Conditional pattern base & count
                        CPB = []  # Conditional Pattern Base
                        CPBW = []  # for twu
                        CPBC = []  # for count

                        LocalF1 = [0] * parent.itemCount
                        LocalCount = [0] * parent.itemCount

                        # Traverse Horizontal links, and merge subtrees into a cofi_tree
                        while chLink is not None:
                            # print(chLink)
                            # print(f"{chLink.item}:{chLink.count}")

                            path = []
                            cptr = chLink

                            while cptr.parentLink is not None:
                                # print(cptr.item)
                                path.append(cptr.item)

                                LocalF1[cptr.item] += chLink.twu
                                LocalCount[cptr.item] += chLink.count
                                cptr = cptr.parentLink

                            path.pop(0)  # remove the first item
                            CPB.append(path)
                            CPBW.append(chLink.twu)
                            CPBC.append(chLink.count)

                            # Turn to the next horizontal link
                            chLink = chLink.hLink

                        # Create localflist
                        localflist = []
                        for j in range(len(LocalF1)):
                            if LocalF1[j] < parent.globalMinUtil:
                                LocalF1[j] = -1
                            else:
                                if j != citem:
                                    parent.InsertItem(localflist, j, LocalF1)

                                    fprefix = f"{citem} {j}"

                                    # Print the output
                                    # print(f"{fprefix}:{LocalF1[j]}")
                                    UTI = f"{Nprefix} {j}"
                                    SumMau = sum(parent.arrayMAU[int(x)] for x in UTI.split())
                                    SumMiu = sum(parent.arrayMIU[int(x)] for x in UTI.split())

                                    MAU = SumMau * LocalCount[j]

                                    if MAU >= parent.globalMinUtil:
                                        MIU = SumMiu * LocalCount[j]
                                        bfw_UCI.write(f"{Nprefix} {j}:{LocalF1[j]}\n")

                                        if MIU > parent.globalMinUtil:
                                            parent.UpdateNodeCountHeap(ISNodeCountHeap, MIU)

                        if CPB:
                            # Build Tree for citem according to conditional pattern base
                            C_FPtree = parent.FPtree(parent)

                            for k in range(len(CPB)):
                                ltran = CPB[k]
                                Sum_MinBNF = 0

                                # delete infrequent node
                                tran = [0] * len(ltran)
                                tranlen = 0

                                for h in range(len(ltran)):
                                    if LocalF1[ltran[h]] >= parent.globalMinUtil:
                                        Sum_MinBNF += CPBC[k] * parent.arrayMIU[ltran[h]]
                                        tran[tranlen] = ltran[h]
                                        tranlen += 1
                                    else:
                                        sum_value = CPBW[k]
                                        sum_value -= CPBC[k] * parent.arrayMIU[ltran[h]]
                                        CPBW[k] = sum_value

                                self.sort_trans(tran, 0, tranlen, LocalF1)

                                C_FPtree.insPatternBase(tran, tranlen, LocalF1, CPBW[k], CPBC[k], Sum_MinBNF, parent)
                            C_FPtree.UPGrowth_MinBNF(C_FPtree, localflist, Nprefix, bfw_UCI, ISNodeCountHeap, LocalF1, parent)

                bfw_UCI.flush()

        def insert_item(self, localflist, item, localF1):
            # Implement your insert logic here
            pass
        def update_node_count_heap(self, ISNodeCountHeap, MIU):
            # Implement your update logic here
            pass
        def sort_trans(self, tran, start, end, localF1):
            # Implement your sorting logic here
            pass

        def UPGrowth_MinBNF(self, tree, flist, prefix, bfw_UCI, ISNodeCountHeap, LP1,parent):
            for i in range(len(flist)):
                if LP1[flist[i]] >= parent.globalMinUtil:
                    Nprefix = f"{prefix} {flist[i]}" if prefix else str(flist[i])
                    # # Print statements in Python
                    # print(f"prefix: {Nprefix}")
                    # print()  # This prints a blank line
                    # print(f"flist2[{i}]: {flist[i]}")
                    # print()  # This prints another blank line
                    citem = flist[i]  # get current item
                    chLink = tree.header_table[citem]  # current horizontal link

                    # Conditional pattern base & count
                    CPB = []  # Conditional Pattern Base
                    CPBW = []  # for twu
                    CPBC = []  # for count

                    LocalF1 = [0] * parent.itemCount  # Local frequent 1-items
                    LocalCount = [0] * parent.itemCount

                    # Traverse Horizontal links, and merge subtrees into a cofi_tree
                    while chLink is not None:
                        path = []
                        cptr = chLink
                        # print(chLink)  # This calls the __str__ method

                        # # Print specific attributes
                        # print(f"{chLink.item}:{chLink.count}")  # Prints: ExampleItem:5
                        while cptr.parentLink is not None:
                            path.append(cptr.item)

                            LocalF1[cptr.item] += chLink.twu
                            LocalCount[cptr.item] += chLink.count
                            cptr = cptr.parentLink

                        path.pop(0)  # remove the first item
                        CPB.append(path)
                        CPBW.append(chLink.twu)
                        CPBC.append(chLink.count)

                        # Turn to the next horizontal link
                        chLink = chLink.hLink

                    # Create localflist
                    localflist = []
                    for j in range(len(LocalF1)):
                        if LocalF1[j] < parent.globalMinUtil:
                            LocalF1[j] = -1
                        else:
                            if j != citem:
                                parent.InsertItem(localflist, j, LocalF1)
                                # Concatenate strings
                                fprefix = f"{citem} {j}"

                                # Print the output
                                # print(f"{fprefix}:{LocalF1[j]}")
                                UTI = f"{Nprefix} {j}"
                                TempItem = UTI.split(" ")
                                SumMau = sum(parent.arrayMAU[int(item)] for item in TempItem)
                                SumMiu = sum(parent.arrayMIU[int(item)] for item in TempItem)

                                MAU = SumMau * LocalCount[j]

                                if MAU >= parent.globalMinUtil:
                                    MIU = SumMiu * LocalCount[j]
                                    bfw_UCI.write(f"{Nprefix} {j}:{LocalF1[j]}\n")

                                    if MIU > parent.globalMinUtil:
                                        parent.UpdateNodeCountHeap(ISNodeCountHeap, MIU)

                    if CPB:
                        # Build Tree for citem according to conditional pattern base
                        C_FPtree = parent.FPtree(parent)

                        for k in range(len(CPB)):
                            ltran = CPB[k]
                            SumMinBNF = 0

                            # Delete infrequent node
                            tran = [0] * len(ltran)
                            tranlen = 0

                            for h in range(len(ltran)):
                                if LocalF1[ltran[h]] >= parent.globalMinUtil:
                                    SumMinBNF += CPBC[k] * parent.arrayMIU[ltran[h]]
                                    tran[tranlen] = ltran[h]
                                    tranlen += 1
                                else:
                                    sumValue = CPBW[k]
                                    sumValue -= CPBC[k] * parent.arrayMIU[ltran[h]]
                                    CPBW[k] = sumValue

                            # Sort items in conditional pattern path
                            parent.sorttrans(tran, 0, tranlen, LocalF1)

                            C_FPtree.insPatternBase(tran,tranlen, LocalF1, CPBW[k], CPBC[k], SumMinBNF, parent)
                            
                        C_FPtree.UPGrowth_MinBNF(C_FPtree, localflist, Nprefix, bfw_UCI, ISNodeCountHeap, LocalF1, parent)

            # Ensure memory is checked and buffer is flushed
            logger = MemoryLogger.MemoryLogger()
            logger.getInstance().checkMemory()
            bfw_UCI.flush()

        # def InsertItem(self, localflist, item, localF1):
        #     # Implement your insert logic here
        #     pass

        # def UpdateNodeCountHeap(self, ISNodeCountHeap, MIU):
        #     # Implement your update logic here
        #     pass

        # def SortTrans(self, tran, start, end, localF1):
        #     # Implement your sorting logic here
        #     pass

        def traverse_tree(self, cNode, level=0):
            level += 1
            if cNode is not None:
                for child in cNode.childLink:
                    self.traverse_tree(child, level)

        def sum_descendent(self, cNode, DS_Sum_Table):
            if cNode is not None:
                DS_Sum_Table[cNode.item] += cNode.count
                for child in cNode.childLink:
                    self.sum_descendent(child, DS_Sum_Table)

        # Các hàm khác như instrans3, UPGrowth, và InsertItem có thể được thêm vào đây...