import numpy as np


class Statistics:
    def __init__(self):
        # deg
        self.d = None
        self.maxD = None
        self.meanD = None
        self.medianD = None
        self.stdD = None

        # degMx
        self.dMx = None
        self.maxDmx = None
        self.meanDmx = None
        self.medianDmx = None
        self.stdDmx = None

        # degMn
        self.dMn = None
        self.maxDmn = None
        self.meanDmn = None
        self.medianDmn = None
        self.stdDmn = None

        # degMdn
        self.dMdn = None
        self.maxDmdn = None
        self.meanDmdn = None
        self.medianDmdn = None
        self.stdDmdn = None

        # theta
        self.theta = None
        self.maxTheta = None
        self.meanTheta = None
        self.medianTheta = None
        self.stdTheta = None

        # thetaS
        self.thetaS = None
        self.maxThetaS = None
        self.meanThetaS = None
        self.medianThetaS = None
        self.stdThetaS = None

    def calculate(self, graph, sentenceCount):
        # deg
        self.d = self.__calculateDeg(graph)
        self.maxD = np.max(self.d)
        self.meanD = np.mean(self.d)
        self.medianD = np.median(self.d)
        self.stdD = np.std(self.d)

        # degMx
        self.dMx = self.__calculateDegMx(graph)
        self.maxDmx = np.max(self.dMx)
        self.meanDmx = np.mean(self.dMx)
        self.medianDmx = np.median(self.dMx)
        self.stdDmx = np.std(self.dMx)

        # degMn
        self.dMn = self.__calculateDegMn(graph)
        self.maxDmn = np.max(self.dMn)
        self.meanDmn = np.mean(self.dMn)
        self.medianDmn = np.median(self.dMn)
        self.stdDmn = np.std(self.dMn)

        # degMdn
        self.dMdn = self.__calculateDegMdn(graph)
        self.maxDmdn = np.max(self.dMdn)
        self.meanDmdn = np.mean(self.dMdn)
        self.medianDmdn = np.median(self.dMdn)
        self.stdDmdn = np.std(self.dMdn)

        # theta
        self.theta = np.array(self.__calculateTheta(graph))
        self.maxTheta = np.max(self.theta)
        self.meanTheta = np.mean(self.theta)
        self.medianTheta = np.median(self.theta)
        self.stdTheta = np.std(self.theta)

        # thetaS
        self.thetaS = self.__calculateThetaS(sentenceCount)
        self.maxThetaS = np.max(self.thetaS)
        self.meanThetaS = np.mean(self.thetaS)
        self.medianThetaS = np.median(self.thetaS)
        self.stdThetaS = np.std(self.thetaS)

    def __calculateDeg(self, graph):
        deg = np.zeros((len(graph)))
        for i in range(len(graph)):
            deg[i] = np.count_nonzero(graph[i])
        deg.sort()
        return deg

    def __calculateDegMx(self, graph):
        degMx = np.zeros(len(graph))
        for i in range(len(graph)):
            degMx[i] = np.max(graph[i])
        degMx.sort()
        return degMx

    def __calculateDegMn(self, graph):
        degMn = np.zeros(len(graph))
        for i in range(len(graph)):
            degMn[i] = np.mean(graph[i])
        degMn.sort()
        return degMn

    def __calculateDegMdn(self, graph):
        degMdn = np.zeros(len(graph))
        for i in range(len(graph)):
            degMdn[i] = np.median(graph[i])
        degMdn.sort()
        return degMdn

    def __calculateTheta(self, graph):
        theta = graph[np.triu_indices(len(graph), 1)]
        theta.sort()
        theta = np.extract(theta != 0, theta)
        return theta

    def __calculateThetaS(self, sentenceCount):
        thetaS = self.theta
        thetaS = thetaS / sentenceCount
        thetaS.sort()
        return thetaS

    def toList(self):
        return [
            list(self.d), self.maxD, self.meanD, self.medianD, self.stdD,
            list(self.dMx), self.maxDmx, self.meanDmx, self.medianDmx, self.stdDmx,
            list(self.dMn), self.maxDmn, self.meanDmn, self.medianDmn, self.stdDmn,
            list(self.dMdn), self.maxDmdn, self.meanDmdn, self.medianDmdn, self.stdDmdn,
            list(self.theta), self.maxTheta, self.meanTheta, self.medianTheta, self.stdTheta,
            list(self.theta), self.maxThetaS, self.meanThetaS, self.medianThetaS, self.stdThetaS
        ]

    def toStatistics(self, data: list):
        self.d = data[0]
        self.maxD = data[1]
        self.meanD = data[2]
        self.medianD = data[3]
        self.stdD = data[4]
        self.dMx = data[5]
        self.maxDmx = data[6]
        self.meanDmx = data[7]
        self.medianDmx = data[8]
        self.stdDmx = data[9]
        self.dMn = data[10]
        self.maxDmn = data[11]
        self.meanDmn = data[12]
        self.medianDmn = data[13]
        self.stdDmn = data[14]
        self.dMdn = data[15]
        self.maxDmdn = data[16]
        self.meanDmdn = data[17]
        self.medianDmdn = data[18]
        self.stdDmdn = data[19]
        self.theta = data[20]
        self.maxTheta = data[21]
        self.meanTheta = data[22]
        self.medianTheta = data[23]
        self.stdTheta = data[24]
        self.thetaS = data[25]
        self.maxThetaS = data[26]
        self.meanThetaS = data[27]
        self.medianThetaS = data[28]
        self.stdThetaS = data[29]
