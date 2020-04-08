from data.db_controller import get_schools


class HouseNany:
    def __init__(self):
        pass

    @staticmethod
    def get_schools():
        return get_schools()

    @staticmethod
    def get_properties(school: str):
        return {'QUARTA': {"x": 1, "y": 2}}