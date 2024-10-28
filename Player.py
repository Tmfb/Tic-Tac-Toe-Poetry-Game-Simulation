
class Player:
#

    def __init__(self, type, color, fichas = [],fichas_schema = {}):
        self.type = type
        self.fichas = fichas
        self.color = color
        self.fichas_schema = fichas_schema
    
    def __str__(self):
        return f"[Type: {self.type},\nFichas: {self.fichas}]"

    def getType(self):
        return self.type
    
    #Return first word if especified index 1 or the second word if specified index 2, Else returns a list of both words
    def getFichas(self):
        return self.fichas
    
    def getColor(self):
        return self.color

    #Returns a list of strings with each word type there are any fichas of
    def getFichasSchema(self):
        avaliable_types = []
        for type in self.fichas_schema:
            if self.fichas_schema[type] > 0:
                avaliable_types.append(type)
        return avaliable_types 

    def setFichas(self, fichas):
        self.fichas = fichas

    def setFichasSchema(self, fichas_schema):
        self.fichas_schema = fichas_schema

    def popFicha(self, index):
            popped = self.fichas.pop(index)
            self.fichas_schema[popped.getType()] -= 1
            return popped
