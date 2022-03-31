class Statistics:
    def __init__(self):
        self.__sentences_count = 0
        self.__word_count = 0
        self.__morphologic_quantity = dict()
        self.__plot_number = 0
        self.__dictionary = dict()
        self.__standartStructures = dict()
        self.__posStructures = dict()
        self.__morphologicStructures = dict()


   def __createTable(self, value: StructureStatistic, minStructQuantity: int):
        if value.structure_quantity >= minStructQuantity:
            data = list(value.morphologic_probability.values())
            rows = list(value.morphologic_probability.keys())
            columns = value.structure
            fig = plt.figure(figsize=(15, 5), dpi=400)
            ax = fig.add_subplot(111)
            fig.patch.set_visible(False)
            plt.title('Количество предложений с подобной структурой: ' + str(value.structure_quantity), fontsize=11,
                      loc='left')
            ax.axis('off')
            ax.axis('tight')
            ax.table(cellText=data, rowLabels=rows, colLabels=columns, loc='center', fontsize=22)
            fig.tight_layout()
            plt.savefig(os.getcwd() + '\\tables\\table_' + str(self.__plot_number))
            plt.close()
            self.__plot_number += 1

    def calculateProbability(self):
        for key, value in self.__morphologic_quantity.items():
            self.__morphologic_quantity[key].calculateProbability()

    def createTables(self, minStructQuantity):
        for key, value in self.__morphologic_quantity.items():
            self.__createTable(self.__morphologic_quantity[key], minStructQuantity)

    def saveData(self):
        morphologic_quantity_data = dict()
        for key, value in self.__morphologic_quantity.items():
            morphologic_quantity_data[key] = value.toDict()
        data = {'All_Sentences': self.__sentences_count, 'Unique_Sentences': len(self.__morphologic_quantity),
                'morphologic_quantity_data': morphologic_quantity_data}
        with open('data.json', 'w') as f:
            json.dump(data, f)

    def loadData(self):
        with open('data.json', "r") as read_file:
            load_data = json.load(read_file)

        self.__sentences_count = load_data['All_Sentences']

        for key, value in load_data['morphologic_quantity_data'].items():
            structure_statistic = StructureStatistic([])
            structure_statistic.toStructureStatistic(value)
            self.__morphologic_quantity[key] = structure_statistic