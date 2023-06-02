class Node:
    def callmanager(para1, fullMemory ):
        # Entire size of memory
        para1.fullMemory  = fullMemory
        # Allocated size for operating system
        para1.osMemory = 400
        # Available memory size for user process
        para1.availableMemory = fullMemory - para1.osMemory
        # Call Block class
        para1.frontNode = Block()
        # Create memory (pass parameter)
        para1.frontNode.callBlock(0, para1.availableMemory)

    # Allocate memory definition
    def allocateMemory(para1, processID, memoBlockSize):
        currentNode = para1.frontNode
        previousNode = None

        # Check memory block to allocate
        while currentNode:
            if not currentNode.isAllocated and currentNode.memoBlockSize >= memoBlockSize:
                if currentNode.memoBlockSize == memoBlockSize:
                    # If the block size is exactly equal to the requested size, allocate the entire block
                    currentNode.isAllocated = True
                    currentNode.processID = processID
                else:
                    # Create a new memory block for the remaining 
                    newBlock = Block()
                    newBlock.callBlock(currentNode.startingAdd + memoBlockSize, currentNode.memoBlockSize - memoBlockSize)
                    newBlock.nextMemoBlock= currentNode.nextMemoBlock
                    currentNode.nextMemoBlock= newBlock

                    # Update current block 
                    currentNode.memoBlockSize = memoBlockSize
                    currentNode.isAllocated = True
                    currentNode.processID = processID

                print("Allocate" + processID + " " + str(memoBlockSize) + "k")
                return

            previousNode = currentNode
            currentNode = currentNode.nextMemoBlock

    def releaseMemory(para1, processID):
        currentNode = para1.frontNode
        previousNode = None

        # Find the memory block allocated to the process
        while currentNode:
            if currentNode.isAllocated and currentNode.processID == processID:
                currentNode.isAllocated = False
                currentNode.processID = None
                print("Terminate" + processID)

                # nextblock free(merge two blocks)
                if currentNode.nextMemoBlock and not currentNode.nextMemoBlock.isAllocated:
                    currentNode.memoBlockSize += currentNode.nextMemoBlock.memoBlockSize
                    currentNode.nextMemoBlock= currentNode.nextMemoBlock.nextMemoBlock

                # previous block free(merge two blocks)
                if previousNode and not previousNode.isAllocated:
                    previousNode.memoBlockSize += currentNode.memoBlockSize
                    previousNode.nextMemoBlock= currentNode.nextMemoBlock

                return

            previousNode = currentNode
            currentNode = currentNode.nextMemoBlock

    def printMemory(para1):
        currentNode = para1.frontNode
        print("print memory details:")

        # Print each memory details
        while currentNode:
            status = "Allocated" if currentNode.isAllocated else "Free"
            print("Address:" + str(currentNode.startingAdd) + "memoBlockSize:" + str(currentNode.memoBlockSize) + "k" + "Status:" + status)
            currentNode = currentNode.nextMemoBlock


class Block:
    def callBlock(para1, startingAdd, memoBlockSize):
        # Start address (memory block) named as startingAdd
        para1.startingAdd = startingAdd
        # Memory block size named as memoBlockSize
        para1.memoBlockSize = memoBlockSize
        # At the starting point, the block is allocated as False
        para1.isAllocated = False
        # Allocated process ID
        para1.processID = None
        # Reference of the next memory block(tgis is a linked list)
        para1.nextMemoBlock = None  

# Test the code
x = Node()
x.callmanager(2500)
x.allocateMemory("P1", 600)
x.allocateMemory("P2", 1000)
x.allocateMemory("P3", 300)
x.releaseMemory("P2")
x.allocateMemory("P4", 700)
x.releaseMemory("P1")
x.allocateMemory("P5", 400)
x.printMemory()
