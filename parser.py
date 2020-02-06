import sys

INT, FLOAT, ID, KEYWORD, OPERATOR, COMMA, EOI, INVALID = 1, 2, 3, 4, 5, 6, 7, 8
LETTER = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"
DIGIT = "0123456789"

def typeToString (tp):
    if (tp == INT): 
        return "Int"   
    elif (tp == FLOAT): 
        return "Float"    
    elif (tp == ID): 
        return "ID"    
    elif (tp == KEYWORD): 
        return "Keyword"    
    elif (tp == OPERATOR): 
        return "Operator" 
    elif (tp == COMMA):
        return "Comma"   
    elif (tp == EOI): 
        return "EOI"    
    return "Invalid"

class Token:    
    def __init__(self,tokenType, tokenVal):
        self.type = tokenType
        self.val = tokenVal

    def getTokenType(self):
        return self.type

    def getTokenValue(self):
        return self.val

    def __repr__(self):
        if (self.type in [INT, FLOAT, ID, KEYWORD, OPERATOR]):
            return self.val
        elif (self.type == COMMA):
            return ","
        elif (self.type == EOI):
            return ""
        else:
            return "invalid"

class Lexer:
    def __init__(self, s):
        self.stmt = s
        self.index = 0
        self.nextChar()

    def nextToken(self):
        while True:
            if self.ch.isalpha():
                id = self.consumeChars(LETTER+DIGIT)
                if id == "SELECT" or id == "FROM" or id == "WHERE" or id == "AND":
                    return Token(KEYWORD, id)
                return Token(ID, id)
            elif self.ch.isdigit():
                num = self.consumeChars(DIGIT)
                if self.ch != ".":
                    return Token(INT, num)
                num += self.ch
                self.nextChar()
                if self.ch.isdigit():
                    num += self.consumeChars(DIGIT)
                    return Token(FLOAT, num)
                else:
                    return Token(INVALID, num)
            elif self.ch == ' ':
                self.nextChar()
            elif self.ch == ',':
                self.nextChar()
                return Token(COMMA, ",")
            elif self.ch == '=' or self.ch == '>' or self.ch == '<':
                self.nextChar()
                return Token(OPERATOR, self.ch)
            elif self.ch == '$':
                return Token(EOI, "")
            else:
                self.nextChar()
                return Token(INVALID, self.ch)
    
    def nextChar(self):
        self.ch = self.stmt[self.index]
        self.index = self.index + 1
    
    def consumeChars(self, charSet):
        r = self.ch
        self.nextChar()
        while (self.ch in charSet):
            r = r + self.ch
            self.nextChar()
        return r

    """def checkChar(self, c):
        self.nextChar()
        if (self.ch == c):
            self.nextChar()
            return True
        else:
            return False"""
            
class Parser:
    def __init__(self, s):
        self.lexer = Lexer(s+"$")
        self.token = self.lexer.nextToken()

    def run(self):
        self.query()
        
    def query(self):
        print("<Query>")
        val = self.match_exact(KEYWORD, "SELECT")
        print("\t<Keyword>" + val + "</Keyword>")
        self.IDList()
        val = self.match_exact(KEYWORD, "FROM")
        print("\t<Keyword>" + val + "</Keyword>")
        self.IDList()
        if(self.token.getTokenType != EOI):
            val = self.match_exact(KEYWORD, "WHERE")
            print("\t<Keyword>" + val + "</Keyword>")
            self.condList()
        print("</Query>")    

    def IDList(self):
        print("\t<IDList>")
        val = self.match_type(ID)
        print("\t\t<Id>" + val + "</Id>")
        while self.token.getTokenType() != KEYWORD:
            #print("GOT HERE")
            #if(self.t
            print("\t\t<Comma>" + self.match_type(COMMA) + "</Comma>")
            print("\t\t<Id>" + self.match_type(ID) + "</Id>")
        print("\t</IDList>")
            
    def condList(self):
        print("\t<CondList>")
        self.cond()
        while self.token.getTokenType() != EOI:
            print("\t\t<Keyword>" + self.match_exact(KEYWORD, "AND") + "</Keyword")
            self.cond()
        print("\t</CondList>")

    def cond(self):
        print("\t\t<Cond>")
        val = self.match_type(ID)
        print("\t\t\t<Id>" + val + "</Id>")
        val = self.match_type(OPERATOR)
        print("\t\t\t<Operator>" + val + "</Operator>")
        self.Term()
        print("\t\t</Cond>")

    def Term(self):
        print("\t\t\t<Term>")
        token = self.token.getTokenType()
        val = self.token.getTokenValue()
        if(token == ID):
            print("\t\t\t\t<Id>" + val + "</Id>")
        elif(token == INT):
            print("\t\t\t\t<Int>" + val + "</Int>")
        elif(token == FLOAT):
            print("\t\t\t\t<Float>" + val + "</Float>")
        else:
            self.error_type(token)
        self.token = self.lexer.nextToken()
        print("\t\t\t</Term>")

    def match_type(self, tp):
        val = self.token.getTokenValue()
        if(self.token.getTokenType() == tp):
            self.token = self.lexer.nextToken()
        else:
            self.error_type(tp)
        return val

    def match_exact(self, tp, check):
        val = self.token.getTokenValue()
        #print(val)
        if(self.token.getTokenType() == tp):
            if(val == check):
                self.token = self.lexer.nextToken()
            else:
                self.error_exact(tp, check)
        else:
            self.error_type(tp)
        return val
        
    def error_type(self, tp):
        print("Syntax error: expecting: " + typeToString(tp) + "; saw: " + typeToString(self.token.getTokenType()))
        sys.exit(1)
        
    def error_exact(self, tp, check):
        print("Syntax error: expecting: " + check + "; saw: " + self.token.getTokenValue())
        sys.exit(1)



def main():
    parser = Parser("SELECT C1,C2 FROM T1 WHERE C1=5.23")
    parser.run()
    parser2 = Parser("SELECT Test1 , Test3 FROM Gigabyte WHERE Test1 = 54326 AND Test3 = Test1")
    parser2.run()

    #parser3 = Parser("SELECT Test1 , Test3 FROM Gigabyte WHERE Test1 = 54326 AND Test3 = Test1 AND")
    #parser3.run()
    parser4 = Parser("SELECT Test1 ,Test3 FROM   Gigabyte SELECT Test1 = 54326 AND Test3 = Test1 AND")
    parser4.run()


main()