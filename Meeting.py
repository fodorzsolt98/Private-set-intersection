class Meeting:
    def __init__(self, startDate, startTime, length, title='', description=''):
        self.startDate = startDate
        self.startTime = startTime
        self.length = length
        self.title = title
        self.description = description

    def getStartTime(self):
        h = self.startTime // 60
        m = self.startTime % 60
        return f'{"0" + str(h) if h < 10 else h}:{"0" + str(m) if m < 10 else m}'

    def getEndTime(self):
        h = (self.startTime + self.length) // 60
        m = (self.startTime + self.length) % 60
        return f'{"0" + str(h) if h < 10 else h}:{"0" + str(m) if m < 10 else m}'

    def getDateAndTime(self):
        return f'{self.startDate.strftime("%Y-%m-%d")}: {self.getStartTime()} - {self.getEndTime()}'

    def getYear(self):
        return self.startDate.year

    def getWeek(self):
        return self.startDate.isocalendar().week

    def print(self):
        print(f'The {self.title} meeting is in {self.startDate.strftime("%Y-%m-%d")}, from {self.getStartTime()} to {self.getEndTime()}')
