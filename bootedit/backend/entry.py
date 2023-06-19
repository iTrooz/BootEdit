class UEFIEntry:
    """
    :attr id: ID of this entry (the 4 hex digit of the Boot### variable in decimal form)
    :attr name: Name of this entry
    :attr attributes: bitfield with flags of this entry
    :attr location: path of the executable to run
    """
    def __init__(self):
        self.id = 0
        self.name = ""
        self.attributes = 0
        self.location = ""
