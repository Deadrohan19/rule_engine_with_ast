
class SyntaxError(Exception):
    """ Exception raised for sytax errors 
    
    Attributes:
        expected: expected token
        got: token got at that position
        val: value of that token

    """
    def __init__(self, expected, got, val):
        self.message = "SyntaxError: expected {} but, got {} with value {}".format(expected, got, val)
        super().__init__(self.message)

class InvalidTokenError(Exception):
    """ Exception raised for Invalid tokens 

    Attributes:
        token: token which caused error         
        pos: position of token
    """
    def __init__(self, token, pos):
        self.message = "InvalidToken: '{}' at position {}".format(token, pos)
        super().__init__(self.message)

class TypeError(Exception):
    """ Type errors during evaluation 
    
    Attributes:
        attr: attribute which is being compared
        val: compare value
        ref: reference value

    """
    def __init__(self, attr, val, ref):
        self.message = "TypeError: cannot compare {} with {}, attribute: {}".format(val, ref, attr)
        super().__init__(self.message)

class InsufficientDataError(Exception):
    """ attribute not present in provided data

    Attributes:
        attr: attribute which is not present
    """
    def __init__(self, attr):
        self.message = "InsufficientDataError: {} attribute is not present in provided data".format(attr)
        super().__init__(self.message)
