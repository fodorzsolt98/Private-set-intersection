from random import randint, choice
from datetime import date, timedelta
from Meeting import Meeting
import string

class MeetingHandler:
    def __init__(self):
        self.meetings = {}

    def createDummyMeetingsOnlyWithTimeInfo(self, count, start, end):
        meetings = {}
        dateDiff = abs((end - start).days)
        for i in range(0, count):
            rdate = start + timedelta(days=randint(0, dateDiff))
            y = rdate.year
            w = rdate.isocalendar().week
            if y not in meetings:
                meetings[y] = {}
            if w not in meetings[y]:
                meetings[y][w] = []
            meetings[y][w].append(Meeting(
                startDate=rdate,
                startTime=randint(50, 260) * 5,
                length=randint(6, 24) * 5,
                title=''.join(choice(string.ascii_lowercase) for i in range(randint(5, 20))),
                description=''.join(choice(string.ascii_lowercase) for i in range(randint(20, 100)))))
        return meetings

    def createDummyMeetings(self, count, start, end):
        meetings = self.createDummyMeetingsOnlyWithTimeInfo(count, start, end)
        for year in meetings.keys():
            for week in meetings[year].keys():
                for meeting in meetings[year][week]:
                    meeting.title = ''.join(choice(string.ascii_lowercase) for i in range(randint(5, 20)))
                    meeting.description = ''.join(choice(string.ascii_lowercase) for i in range(randint(20, 100)))
        return meetings

    def appendMeetings(self, meetings):
        for year in meetings.keys():
            if year not in self.meetings:
                self.meetings[year] = meetings[year]
            else:
                for week in meetings[year].keys():
                    if week not in self.meetings[year]:
                        self.meetings[year][week] = meetings[year][week]
                    else:
                        self.meetings[year][week].extend(meetings[year][week])

    def createMeetingSequences(self, date, start, end, length):
        meetings = {}
        meetings[date.year] = {}
        meetings[date.year][date.isocalendar().week] = []
        for currentStart in self.getStartTimes(start, end, length):
            meeting = Meeting(date, currentStart, length)
            meetings[date.year][date.isocalendar().week].append(meeting)
        return meetings

    def getStartTimes(self, start, end, length):
        startTimes = {start}
        while start + length <= end:
            for t in [start + i * length for i in range(0, (end - start) // length)]:
                startTimes.add(t)
            start += 15
        startTimesList = list(startTimes)
        startTimesList.sort()
        return startTimesList

    def getMeetingWeeks(self, meetings):
        weeks = {}
        for y in meetings.keys():
            weeks[y] = list(meetings[y].keys())
        return weeks

    def getAndCeheckTheLengthOfTheMeetings(self, meetings):
        years = list(meetings.keys())
        length = meetings[years[0]][list(meetings[years[0]].keys())[0]][0].length
        correct = True
        y = 0
        while correct and (y < len(years)):
            weeks = list(meetings[years[y]].keys())
            w = 0
            while correct and (w < len(weeks)):
                ms = meetings[years[y]][weeks[w]]
                m = 0
                while correct and (m < len(ms)):
                    if ms[m].length != length:
                        correct = False
                    m += 1
                w += 1
            y += 1
        if correct:
            return length
        else:
            return None

