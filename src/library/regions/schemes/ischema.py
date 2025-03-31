class IScheme:

    def get_sorted_scheme_members(self)-> list[str]:
        pass
    
    @classmethod
    def get_sorted_scheme_members(cls)-> list[str]:
        '''
        Get sorted list of members
        '''
        members = [
            (name,value)
            for name,value in vars(cls).items()
            if not name.startswith('__') and not callable(value)
        ]
        return [member[0] for member in  sorted(members, key=lambda x: x[1][2])]