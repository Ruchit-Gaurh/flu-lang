class Parser:
    def __init__(self, tokens):
        self.index = 0
        self.tokens = tokens
        self.token = self.tokens[self.index]

    def factor(self):
        if self.token.type == "INT" or self.token.type == "FLT":
            return self.token
        elif self.token.value == "(":
            self.move()
            expression = self.boolean_expression()
            return expression
        elif self.token.value == "nahi":
            operatior = self.token
            self.move()
            return [operatior, self.boolean_expression()]
        elif self.token.type.startswith("VAR"):
            return self.token
        elif self.token.value == '+' or self.token.value == '-':
            operator = self.token
            self.move()
            operand = self.boolean_expression()
            return [operator, operand]
        
    def term(self):
        left_node = self.factor()
        self.move()
        while self.token.value == "*" or self.token.value == "/" or self.token.value == "i" or self.token.value == "d":
            operation = self.token
            self.move()
            right_node = self.factor()
            self.move()
            left_node= [left_node, operation, right_node]

        return left_node
    
    def comparision_expression(self):
        left_node = self.expression()
        while self.token.type == "COMP":
            operation = self.token
            self.move()
            if operation.value == "bada" or operation.value == "chota":
                val = operation.value
                if self.token.value == "ya":
                    if val == "bada":
                        operation.value = "badabr"
                    else:
                        operation.value = "chotabr"
                    self.move()
                    self.move()
                self.move()
            
            right_node = self.expression()
            self.move()
            left_node= [left_node, operation, right_node]

        return left_node


    def boolean_expression(self):
        left_node = self.comparision_expression()
        while self.token.type == "BOOL":
            operation = self.token
            self.move()
            right_node = self.comparision_expression()
            left_node= [left_node, operation, right_node]

        return left_node
        
    def expression(self):
        left_node = self.term()
        while self.token.value == "+" or self.token.value == "-" or self.token.value == "p" or self.token.value == "m":
            operation = self.token
            self.move()
            right_node = self.term()
            left_node= [left_node, operation, right_node]

        return left_node
    
    def while_statement(self):
        self.move()
        condition = self.boolean_expression()

        if self.token.value == "toh":
            self.move()
            action = self.statement()
            return [condition, action]
        
        elif self.tokens[self.idx-1].value == "toh":
            action = self.statement()
            return [condition , action]
    
    def if_statement(self):
        self.move()
        condition = self.boolean_expression()
        
        if self.token.value == "toh":
            self.move()
            action = self.statement()
            return condition,action
        elif self.tokens[self.index-1] == "toh":
            action = self.statement()
            return condition,action
    
    def if_statements(self):
        conditions = []
        actions = []
        if_statement = self.if_statement()

        conditions.append(if_statement[0])
        actions.append(if_statement[1])

        while self.token.value == "nito":
            if_statement = self.if_statement()
            conditions.append(if_statement[0])
            actions.append(if_statement[1])

        if self.token.value == "warna":
            self.move()
            else_action = self.statement()
            return [conditions, actions, else_action]

        return [conditions, actions]
    
    def statement(self):

        if self.token.type == "INT" or self.token.type == "FLT" or self.token.type == "OP" or self.token.value == "nahi":
            return self.boolean_expression()
        elif self.token.value == "agar":
            return [self.token, self.if_statements()]
        elif self.token.value == "jabtk":
            return [self.token, self.while_statement()]
        else:
            left_node= self.variable()
            self.move()
            if self.token.value == "=" or self.token.value=="barabar":
                operation = self.token
                self.move()
                right_node = self.boolean_expression()

                return [left_node, operation, right_node]

    def variable(self):
        if self.token.type.startswith("VAR"):
            return self.token

    def parse(self):
        return self.statement()

    def move(self):
        self.index += 1
        if self.index < len(self.tokens):
            self.token = self.tokens[self.index]