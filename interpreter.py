from tokens import Integer, Float, Reserved

class Interpreter:
    def __init__(self,tree, base):
        self.tree = tree
        self.data = base

    def read_INT(self, value):
        return int(value)

    def read_FLT(self, value):
        return float(value)

    def read_VAR(self, id):
        variable = self.data.read(id)
        variable_type = variable.type

        return getattr(self, f"read_{variable_type}")(variable.value)

    def compute_binary(self, lft, op, rght):
        left_type = "VAR" if str(lft.type).startswith("VAR") else lft.type
        right_type = "VAR" if str(rght.type).startswith("VAR") else rght.type

        if op.value == "=" or op.value == "barabar":
            lft.type=f"VAR({right_type})"
            self.data.write(lft, rght)
            return self.data.read_all()

        left = getattr(self, f"read_{left_type}")(lft.value)
        right = getattr(self, f"read_{right_type}")(rght.value)

        if op.value == "+" or op.value == "p":
            output = left + right
        elif op.value == "-" or op.value == "m":
            output = left - right
        elif op.value == "*" or op.value == "i":
            output = left * right
        elif op.value == "/" or op.value == "d":
            output = left / right
        elif op.value == "bada":
            output = True if left>right else False
        elif op.value == "chota":
            output = True if left<right else False
        elif op.value == "badabr":
            output = True if left>=right else False
        elif op.value == "chotabr":
            output = True if left<=right else False
        elif op.value == "brabr":
            output = True if left==right else False
        elif op.value == "aur":
            output = True if left and right else False
        elif op.value == "ya":
            output = True if left or right else False
    
        return Integer(output) if(left_type == "INT" and right_type=="INT") else Float(output)
    

    def compute_unary(self, operator, operand):
        operand_type = "VAR" if str(operand.type).startswith("VAR") else operand.type
        operand = getattr(self, f"read_{operand_type}")(operand.value)
        if operator.value == "+":
            output = +operand
        elif operator.value == "-":
            output = -operand
        elif operator.value == "nahi":
            output = True if not operand else False
        
        return Integer(output) if (operand_type == "INT") else Float(output)

    def interpret(self, tree=None):
        if tree is None:
            tree = self.tree

        if isinstance(tree, list):
            if isinstance(tree[0], Reserved):
                if tree[0].value == "agar":
                    for idx, condition in enumerate(tree[1][0]):
                        evaluation = self.interpret(condition)
                        if evaluation.value == 1:
                            return self.interpret(tree[1][1][idx])
                    
                    if len(tree[1]) == 3:
                        return self.interpret(tree[1][2])

                    else:
                        return
                
                elif tree[0].value == "jabtk":
                    condition = self.interpret(tree[1][0])

                    while condition.value == 1:
                        self.interpret(tree[1][1])

                        condition = self.interpret(tree[1][0])
                    return

        if isinstance(tree, list) and len(tree) == 2:
            expression = tree[1]
            if isinstance(expression, list):
                expression = self.interpret(expression)
            return self.compute_unary(tree[0], expression)
        
        elif not isinstance(tree, list):
            return tree

        else:
            left_node = tree[0]

            if isinstance(left_node, list):
                left_node = self.interpret(left_node)

            right_node = tree[2]
            if isinstance(right_node, list):
                right_node = self.interpret(right_node)
            operator = tree[1]

            return self.compute_binary(left_node, operator, right_node)