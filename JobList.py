from Job import *

class JobList(object):

    #Needed Variable
    listofjobs = []

    def updateJobList(self, creatorName, jobName, numofSeekers):
        """
        description: This Function takes in three strings and creates a
                    Job object and adds that object to a List of Jobs
        :param creatorName: Given From Client as a string
        :param jobName: Given From Client as a string
        :param numofSeekers: Given From Client as a string
        :return: VOID
        """

        #Creating Job Object
        job = Job(creatorName, jobName, numofSeekers)

        #Adding Job Object to List of Jobs
        self.listofjobs.append(job)

    def printJobList(self):
        """
        Description: This Function is used to print all jobs that are
                    currently inside the List of Jobs
        :return: VOID
        """

        #Loop For Every Job Object in The List of Jobs
        for jobs in self.listofjobs:

            #Loop For Every Element in The Job Object
            for elements in jobs:
                print(elements, end=", ")
            print()

    def updateNumOfSeekers(self, jobNumber):
        """
        Description: This Function takes in parameter jobNumber which is used to determine which job
                    will be updating the amount of Job Seekers needed, Loops through the three main
                    Job object parameters and stores all three in temp variables, updates the NumofSeekers
                    by subtracting one then removing the old Job object and adding in the new updated Job object
        :param jobNumber:This is given from the Client which is an integer
                        that determines which Job they will be updating the
                         number of seekers. This function is used during the
                        accept job phase. [TO BE REFACTORED]
        :return:VOID
        """

        #Counter Variable
        count = 1

        #Loop For Every Element in Specific Job
        for elements in self.listofjobs[jobNumber]:

            #JobCreatorName Condition
            if count == 1:
                jobCreatorName = elements

            #JobName Condition
            elif count == 2:
                jobName = elements

            #NumofSeekers Condition
            elif count == 3:
                NumofSeekers = int(elements) - 1

            #Update Counter Variable
            count+=1

        #Removing the Old Job
        self.listofjobs.remove(self.listofjobs[jobNumber])

        #Adding the New Job
        self.updateJobList(jobCreatorName, jobName, str(NumofSeekers))

    def updateJobSeekerList(self, jobSelection, SeekerName):
        self.listofjobs[jobSelection].addSeekerList(SeekerName)

    '''
    Obtain Functions
    '''
    def obtainJobCreator(self, jobSelection):

        return self.listofjobs[jobSelection].getJobCreator()

    def obtainJobName(self, jobSelection):

        return self.listofjobs[jobSelection].getJobName()

    def obtainNumOfSeekers(self, jobSelection):

        return self.listofjobs[jobSelection].getNumOfSeekers()

    def obtainFullJob(self, jobSelection):

        return self.listofjobs[jobSelection].getFullJob()

    def obtainJobSeekerList(self, jobSelection):

        return self.listofjobs[jobSelection].getJobSeekerList()
