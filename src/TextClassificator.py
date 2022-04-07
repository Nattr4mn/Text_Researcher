import numpy as np

from src.Statistics.StatisticalData import StatisticalData


class TextClassificator:
    def __init__(self, nat_statistic_data: StatisticalData, gen_statistic_data: StatisticalData):
        self.__natural_dmx, self.__natural_theta = self.__colectingStatisticData(nat_statistic_data.texts_statistic)
        self.__gen_dmx, self.__gen_theta = self.__colectingStatisticData(gen_statistic_data.texts_statistic)
        self.__statistic_natural_dmx = {'min': np.min(self.__natural_dmx), 'max': np.max(self.__natural_dmx),
                                        'mean': np.mean(self.__natural_dmx), 'median': np.median(self.__natural_dmx)}
        self.__statistic_natural_theta = {'min': np.min(self.__natural_theta), 'max': np.max(self.__natural_theta),
                                          'mean': np.mean(self.__natural_theta),
                                          'median': np.median(self.__natural_theta)}
        self.__statistic_gen_dmx = {'min': np.min(self.__gen_dmx), 'max': np.max(self.__gen_dmx),
                                    'mean': np.mean(self.__gen_dmx), 'median': np.median(self.__gen_dmx)}
        self.__statistic_gen_theta = {'min': np.min(self.__gen_theta), 'max': np.max(self.__gen_theta),
                                      'mean': np.mean(self.__gen_theta), 'median': np.median(self.__gen_theta)}

        print('Natural:')
        print(self.__statistic_natural_dmx)
        print(self.__statistic_natural_theta)
        print('Generated:')
        print(self.__statistic_gen_dmx)
        print(self.__statistic_gen_theta)

    def classificationMedianDmx(self, text: str) -> bool:
        statistical_data = StatisticalData()
        statistic, _ = statistical_data.calculateStatistics(text)
        if statistic.maxDmx > self.__statistic_natural_dmx['median']:
            return True
        else:
            return False

    def classificationMeanDmx(self, text: str) -> bool:
        statistical_data = StatisticalData()
        statistic, _ = statistical_data.calculateStatistics(text)
        if statistic.maxDmx > self.__statistic_natural_dmx['mean']:
            return True
        else:
            return False

    def classificationMedianTheta(self, text: str) -> bool:
        statistical_data = StatisticalData()
        statistic, _ = statistical_data.calculateStatistics(text)
        if statistic.maxDmx > self.__statistic_natural_theta['median']:
            return True
        else:
            return False

    def classificationMeanTheta(self, text: str) -> bool:
        statistical_data = StatisticalData()
        statistic, _ = statistical_data.calculateStatistics(text)
        if statistic.maxDmx > self.__statistic_natural_theta['mean']:
            return True
        else:
            return False

    def __colectingStatisticData(self, statistic_list: list):
        statistics_dict = {'max(Dmx)': [], 'max(θ)': []}
        for statistic in statistic_list:
            statistics_dict['max(Dmx)'].append(statistic.maxDmx)
            statistics_dict['max(θ)'].append(statistic.maxTheta)
        dmx = np.array(statistics_dict['max(Dmx)'])
        theta = np.array(statistics_dict['max(θ)'])
        return dmx, theta


