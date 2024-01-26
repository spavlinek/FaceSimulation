class Emotion():
    def __init__(self, name, emotionDict):
        #emotion should be dict of muscle names: percent
        #at 100% each of the muscles are pulled to a certain percent
        #musclesPercent should be given as values when percentExpressed is 100%
        self.emotionDict = emotionDict
        self.name = name
    #using the percentExpressed value (Joy 30%) get the respective percentages of each of the muscles
    def getMusclePercent(self, muscle):
        return self.emotionDict[muscle]
    #when an emotion is showing less than 100% modify the percent values for it
    def modifyEmotionValuesByPercent(self, percent):
        for muscle in self.emotionDict.keys():
             currPercent = self.emotionDict[muscle]
             newPercent = percent*currPercent
             self.emotionDict[muscle] = newPercent