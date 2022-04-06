from tracemalloc import Statistic

import numpy as np

from src.Statistics.StatisticalData import StatisticalData


class TextClassificator:
    def __init__(self, nat_statistic_data: StatisticalData, gen_statistic_data: StatisticalData):
        self.__nat_max_dmx_mean, self.__nat_max_dmdn_ean, self.__nat_max_theta_mean, self.__nat_max_dmx_median, \
        self.__nat_max_dmdn_median, self.__nat_max_theta_median = self.__calculateStatistic(nat_statistic_data.texts_statistic)

    def __calculateStatistic(self, statistic_list: list):
        dmx, dmdn, theta = self.__colectingStatisticData(statistic_list)
        return np.mean(dmx), np.mean(dmdn), np.mean(theta), np.median(dmx), np.median(dmdn), np.median(theta)

    def __colectingStatisticData(self, statistic_list: list):
        statistics_dict = {'max(Dmx)': [], 'max(Dmdn)': [], 'max(θ)': []}
        for statistic in statistic_list:
            statistics_dict['max(Dmx)'].append(statistic.maxDmx)
            statistics_dict['max(Dmdn)'].append(statistic.maxDmdn)
            statistics_dict['max(θ)'].append(statistic.maxTheta)
        dmx = np.array(statistics_dict['max(Dmx)'])
        dmdn = np.array(statistics_dict['max(Dmdn)'])
        theta = np.array(statistics_dict['max(θ)'])
        return dmx, dmdn, theta