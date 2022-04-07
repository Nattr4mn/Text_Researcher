import collections
import json

from src.TextInfo.Structure import Structure


class StructuresList(collections.MutableSequence):
    def __init__(self, *args):
        self.__structures = list()
        self.__index_table = dict()
        self.extend(list(args))

    def __len__(self):
        return len(self.__structures)

    def __getitem__(self, i: int):
        return self.__structures[i]

    def clear(self):
        self.__structures.clear()
        self.__index_table.clear()

    def __delitem__(self, i):
        self.__index_table.pop(self.__structures[i].standart_structure)
        del self.__structures[i]

    def __str__(self):
        return '; '.join([str(structure.toList()) for structure in self.__structures])

    def __setitem__(self, i: int, structure: Structure):
        self.__index_table.pop(str(self.__structures[i].standart_structure))
        self.__index_table.update({str(structure.standart): i})
        self.__structures[i] = structure

    def __contains__(self, structure: Structure):
        if self.__index_table.get(str(structure.standart)) is not None:
            return True
        else:
            return False

    def insert(self, i, sentence_info: list):
        structure = Structure()
        structure.createStructure(sentence_info)
        index = self.__index_table.get(str(structure.standart))
        if index is not None:
            self.__structures[index].count += 1
        else:
            self.__structures.append(structure)
            self.__index_table.update({str(structure.standart): len(self.__structures) - 1})

    def save(self, file_name="StructuresList"):
        try:
            with open(str(file_name) + ".json", "w") as write_file:
                save_data = []
                value_list = [value.toList() for value in self.__structures]
                save_data.append(value_list)
                save_data.append(self.__index_table)
                json.dump(save_data, write_file)
        except Exception:
            print('An error occurred while saving the structures!')

    def load(self, file_name="StructuresList"):
        try:
            with open(str(file_name) + ".json", "r") as read_file:
                load_data = json.load(read_file)

            self.__structures = [Structure.toStructures(data) for data in load_data[0]]
            self.__index_table = load_data[1]
        except Exception:
            print('An error occurred while loading the list of structures!')
