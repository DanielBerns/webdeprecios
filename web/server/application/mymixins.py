class GetIdMixin:
    '''
    This provides my own implementations for the methods that Flask-Login
    expects user objects to have.
    '''

    # Python 3 implicitly set __hash__ to None if we override __eq__
    # We set it back to its default implementation
    __hash__ = object.__hash__

    @property
    def is_active(self):
        return True

    @property
    def is_authenticated(self):
        return True

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        try:
            return str(self.identifier)
        except AttributeError:
            raise NotImplementedError("No 'identifier' attribute - override 'get_id'")

    def __eq__(self, other):
        '''
        Checks the equality of two 'GetIdMixin' objects using 'get_id'.
        '''
        if isinstance(other, GetIdMixin):
            return self.get_id() == other.get_id()
        return NotImplemented

    def __ne__(self, other):
        '''
        Checks the inequality of two 'GetIdMixin' objects using 'get_id'.
        '''
        equal = self.__eq__(other)
        if equal is NotImplemented:
            return NotImplemented
        return not equal
 
