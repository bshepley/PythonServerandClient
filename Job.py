
class Job(object):

    def __init__(self, jobCreator, jobName, numOfSeekers):

        self.JobCreator = jobCreator
        self.JobName = jobName
        self.NumOfSeekers = numOfSeekers
        self.FullJob = jobCreator+" "+" "+jobName+" "+" "+numOfSeekers
        self.JobSeekerList = [numOfSeekers]

    def __iter__(self):
        yield self.JobCreator
        yield self.JobName
        yield self.NumOfSeekers

    def addSeekerList(self, SeekerName):
        self.JobSeekerList.append(SeekerName)
        for seekers in self.JobSeekerList:
            print(seekers)

    '''
    Getter Functions
    '''
    def getJobCreator(self):
        return self.JobCreator

    def getJobName(self):
        return self.JobName

    def getNumOfSeekers(self):
        return self.NumOfSeekers

    def getFullJob(self):
        return self.FullJob

    def getJobSeekerList(self):
        return self.JobSeekerList

    '''
    Setter Functions
    '''

    def setJobCreator(self, JobCreator):
        self.JobCreator = JobCreator

    def setJobName(self, JobName):
        self.JobName = JobName

    def setNumOfSeekers(self, NumOfSeekers):
        self.NumOfSeekers = NumOfSeekers

    def setFullJob(self, FullJob):
        self.FullJob = FullJob

    def setJobSeekerList(self, JobSeekerList):
        self.JobSeekerList = JobSeekerList