from data.db_controller import get_schools, get_properties_by_school, get_property


class HouseNany:
    def __init__(self):
        pass

    @staticmethod
    def get_schools(args: dict):
        return get_schools(args)

    @staticmethod
    def get_properties(args):
        return get_properties_by_school(args)

    @staticmethod
    def get_property(args):
        return get_property(args)
