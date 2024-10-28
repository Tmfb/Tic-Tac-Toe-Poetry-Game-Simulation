
class Ficha:
#Creates a token, color coded blue/yellow with a word on each face, both words share the same grammar category

    def __init__(self, color, words,type):
        self.color = color
        self.words = words
        self.type = type
    
    def __str__(self):
        return f"[Color: {self.color}, Words: {self.words}, Type: {self.type}]"

    #Returns Ficha's color string
    def getColor(self):
        return self.color
    
    #Return first word if especified index 1 or the second word if specified index 2, Else returns a list of both words
    def getWords(self,index = 2):
        if index == 0 or index == 1:
            return self.words[index]
        else:
            return (self.words[0] + " - " +self.words[1])

    #Returns Ficha's type string
    def getType(self):
        return self.type
    
    def flip(self):
        self.words = self.words[::-1]