from Job import *

class JobList(object):

    """"
    Final Project
    -Code Logic: nearestSeekerLocationtoTarget()
    -Code Logic: returnJobSeekerLanHosts()
    -Code GUI or convert unto .exe
    -(BONUS 5%) Resume From Crash Point
    """

    '''
    Needed Variables
    listofjobs: This list holds jobs that are created from the Client and will store all the information of the Jobs
    jobsToRequest: This is a static list which is used to hold the names of the types of jobs offered
    '''
    listofjobs = []
    jobsToRequest = ['IP Online Detection', 'Subnet IP Online Detection', 'Specific Port Status Detection',
                     'All Port Status Detection', 'ICMP Flood Attack', 'TCP Flood Attack', 'UDP Flood Attack']

    '''
    One-To-One Jobs
    '''
    def createIPOnlineDetectionJob(self, creatorName):

        #Creating IP Online Detection Job
        job = Job(creatorName, "IP Online Detection", '1')

        #Adding IP Online Detection Job to Job List
        self.listofjobs.append(job)

    def createSubnetIPOnlineDetection(self, creatorName):

        #Creating Subnet IP Online Detection Job
        job = Job(creatorName, "Subnet IP Online Detection", '1')

        #Adding Subnet IP Online Detection Job to Job List
        self.listofjobs.append(job)

    def specificPortStatusDetection(self, creatorName):

        #Creating Specific Port Status Detection Job
        job = Job(creatorName, "Specific Port Status Detection", '1')

        #Adding Specific Port Status Detection Job to Job List
        self.listofjobs.append(job)

    def allPortStatusDetection(self, creatorName):

        # Creating All Port Status Detection Job
        job = Job(creatorName, "All Port Status Detection", '1')

        # Adding All Port Status Detection Job to Job List
        self.listofjobs.append(job)

    '''
    One-To-Many Jobs
    '''
    def createICMPFloodAttackJob(self, creatorName, numOfSeekers):

        #Creating ICMP Flood Attack Job
        job = Job(creatorName, "ICMP Flood Attack", numOfSeekers)

        #Adding ICMP Flood Attack Job to Job List
        self.listofjobs.append(job)

    def createTCPFloodAttackJob(self, creatorName, numOfSeekers):

        #Creating TCP Flood Attack Job
        job = Job(creatorName, "TCP Flood Attack", numOfSeekers)

        #Adding TCP Flood Attack Job to Job List
        self.listofjobs.append(job)

    def createUDPFloodAttackJob(self, creatorName, numOfSeekers):

        #Creating UDP Flood Attack Job
        job = Job(creatorName, "UDP Flood Attack", numOfSeekers)

        #Adding UDP Flood Attack Job to Job List
        self.listofjobs.append(job)

    '''
    Final Project Jobs
    '''
    def nearestSeekerLocationtoTarget(self):
        print()

    def returnJobSeekerLanHosts(self):
        print()

    '''
    HELPER Functions
    '''
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

    def updateNumOfSeekers(self, jobNumber, creatorStart):
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
                if int(elements) == 0 and creatorStart is True:
                    NumofSeekers = "Job Started"
                else:
                    NumofSeekers = int(elements) - 1

            #Update Counter Variable
            count+=1

        #Removing the Old Job
        self.listofjobs.remove(self.listofjobs[jobNumber])

        #Adding the New Job
        self.updateJobList(jobCreatorName, jobName, str(NumofSeekers))

    def updateJobSeekerList(self, jobSelection, SeekerName):
        self.listofjobs[jobSelection].addSeekerList(SeekerName)
