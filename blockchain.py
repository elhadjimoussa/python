from hashlib import sha256
from datetime import datetime

# calcul du hash d'un bloc
def calculHash(block):
    bloc = str(block.index) + str(block.previousHash) + str(block.timestamp) + str(block.data) + str(block.nonce)
    return(sha256(bloc.encode('utf-8')).hexdigest())



 # création de la classe  Block
class Block(object):
    def __init__(self, index, previousHash, timestamp, data):
        self.index = index
        self.previousHash = previousHash
        self.timestamp = timestamp
        self.data = data
        self.nonce = 0
        self.hash = calculHash(self)

    def createBlock(self, difficulty):
        while self.hash[0:difficulty] != "0000":
            self.nonce = self.nonce + 1
            self.hash = calculHash(self)

# création de la  Blockchain


class Blockchain(object):
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.blocks = []
        

#Creation de notre premier block
        NotrepremierBlock = Block(0, None, datetime.now(), "Notre premier block")
        NotrepremierBlock.createBlock(self.difficulty)
        self.blocks.append(NotrepremierBlock)

    def newBlock(self, data):
        latestBlock = self.blocks[-1]
        return(Block(latestBlock.index + 1, latestBlock.hash, datetime.now(), data))

# Ajouter un bloc à la blockchain
    def addBlock(self, block):
        block.createBlock(self.difficulty)
        self.blocks.append(block)

#Verifier si le block est valide
    def PremierBlockValid(self):
        firstBlock = self.blocks[0]

        if firstBlock.index != 0:
            return False
        
        if firstBlock.previousHash is not None:
            return False

        if (firstBlock.hash is None or calculHash(firstBlock) != firstBlock.hash):
            return False

        return True

#Verifier si la blockchain est valide
    def BlockValid(self, block, previousBlock):
        if previousBlock.index+1 != block.index:
            return False

        if (block.previousHash is None or block.previousHash != previousBlock.hash):
            return False
        
        if (block.hash is None or calculHash(block) != block.hash):
            return False
        
        return True

    def BlockchainValid(self):
        if not self.PremierBlockValid():
            return False
        
        for i in range(1, len(self.blocks)):
            previousBlock = self.blocks[i-1]
            block = self.blocks[i]
            if not self.BlockValid(block, previousBlock):
                return False 

        return True
#Affichage de la blockchain
    def affiche(self):
        for block in self.blocks:
            chain = "Block #"+str(block.index)+" ["+"\n\tindex: "+str(block.index)+"\n\tprevious hash: "+str(block.previousHash)+"\n\ttimestamp: "+str(block.timestamp)+"\n\tdata: "+str(block.data)+"\n\thash: "+str(block.hash)+"\n\tnonce: "+str(block.nonce)+"\n]\n"
            print(str(chain))
    
if __name__ == '__main__':
    bchain = Blockchain(4)

    blockn1 = bchain.newBlock("Second Block")
    bchain.addBlock(blockn1)

    blockn2 = bchain.newBlock("Third Block")
    bchain.addBlock(blockn2)

    blockn3 = bchain.newBlock("Fourth Block")
    bchain.addBlock(blockn3)

    print("Super la blockchain est valide:", bchain.BlockchainValid())

    bchain.affiche()

else:
    print("Désolé la blockchain n'est pas valide:", bchain.BlockchainValid())


