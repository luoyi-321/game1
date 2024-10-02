class ObjectDD:
    def __init__(self,img,position:list,Name:str,width:int,height:int):
        self.status = True
        self.img = img
        self.position = position
        self.Name = Name
        self.width = width
        self.height = height
        self.CoverageLine = None

class CoverageLine:
    def __init__(self,x:list,y:list):
        self.x = x
        self.y = y

class IMage:
    def __init__(self,img,pos):
        self.img = img
        self.pos = pos