import socket
import sys
import pickle
from _thread import *
from JobList import *

class Server(object):
    """
    Assignment 3 Tasks to Develop or Fix
    -Multiple Jobs Creates Conflict With Updating Active Seeker List
    -Connect Group Members .py scripts

    Wanted Tasks to Develop or Fix:
    -Removing Job Seeker From a Job (Job Creator)
    -Viewing Joined Jobs (Job Seeker)
    -View Job History (Job Seeker)

    Bugs to Work Out:
    -After Certain Actions The Client Needs to Send Blank Space to Continue
    -Setting Job to Finished as Soon as The Job Gets Started

    Server & Client Functions:
    -Determine if the Client is a Job Creator or Job Seeker
    -Job Creators can Post Jobs
    -Job Seekers can Join Jobs
    -Job Creators and Job Seekers can View the Job List
    -Job Creators can Send Target IP and Port
    -Job Seekers can Obtain Target IP and Port
    -Job Creators can View Job Seeker List
    -Job Creators can Start The Job
    -Job Seekers can Complete The Job
    """

    def __init__(self):

        self.ServerSocket = socket.socket()
        self.host = '127.0.0.1'
        self.port = 1233
        self.ThreadCount = 0
        self.jobList = JobList()
        self.jobCompletion = "Not Complete"
        self.activeJobsWithSeekers = []

        #From Job Creator-->Server-->Job Seeker
        self.targetIP = '1.1.1.1'
        self.targetPort = 25565

        # Bind socket to port
        try:
            self.ServerSocket.bind((self.host, self.port))

        except socket.error as e:
            print(str(e))

        print('Waiting for a Connection..')
        self.ServerSocket.listen(5)

    def main(self):
        while True:
            Client, address = self.ServerSocket.accept()
            print('Connected to: ' + address[0] + ':' + str(address[1]))
            start_new_thread(self.threadedClient, (Client,))
            self.ThreadCount += 1
            print('Thread Number: ' + str(self.ThreadCount))

    def threadedClient(self, connection):

        connection.send(pickle.dumps("Welcome, Are You A Job Seeker or A Job Creator?\n"
                                     + "Enter JS for Job Seeker, JC for Job Creator or Exit to quit"))

        while True:
            # Limiting to 2048 Bytes
            data = connection.recv(2048)

            # Receiving Message From Client
            roleSelection = data.decode()

            # Job Creator Condition
            if roleSelection.upper() == 'JC':
                self.FoundJobCreator(connection)

            # Job Seeker Condition
            if roleSelection.upper() == 'JS':
                self.FoundJobSeeker(connection)

            # Exit Program Condition
            if roleSelection.upper() == 'EXIT':
                sys.exit(0)

            # Base Condition
            if roleSelection.upper() != 'JC' and roleSelection.upper() != 'JS' and roleSelection.upper() != 'EXIT':
                connection.send(pickle.dumps("Not a Valid Input...Enter JS for Job Seeker, "
                                             + "JC for Job Creator or Exit to quit"))

    '''             
    JOB SEEKER FUNCTIONS 
    '''
    #Client Identifies as a Job Seeker
    def FoundJobSeeker(self, connection):

        # Sending Job Seeker Options
        connection.send(pickle.dumps("Job Seeker Menu:\n1.View Jobs\n2.Exit\n"))

        while True:
            # Receiving Message From Client
            data = connection.recv(2048)
            optionSelection = data.decode()

            # View Jobs Condition
            if optionSelection == '1':
                self.viewingMenuJS(connection)

            # Exit Condition
            if optionSelection == '2':
                self.threadedClient(connection)

            # Base Case Condition
            if optionSelection != '1' and optionSelection != '2':
                connection.send(pickle.dumps("Job Seeker Menu:\n1.View Jobs\n2.Exit\n"))

    #FoundJobSeeker-->viewingMenuJS
    def viewingMenuJS(self, connection):

        self.jobListView(connection)

        connection.send(pickle.dumps("Job Viewing Menu:\n1.Join Job\n2.Return to Job Seeker Menu"))

        while True:
            #Receiving Message From Client
            data = connection.recv(2048)
            optionSelection = int(data.decode())

            if optionSelection == 1:
                self.acceptJob(connection)

            elif optionSelection == 2:
                self.FoundJobSeeker(connection)
            else:
                connection.send(pickle.dumps("Job Viewing Menu:\n1.Join Job\n2.Return to Job Seeker Menu"))

    #FoundJobSeeker-->viewingMenuJS-->acceptJob
    def acceptJob(self, connection):

        #Sending Message to Client to Send What Number Of Job They Want to Join
        connection.send(pickle.dumps("Please Enter What Number Job You Would Like To Join"))

        while True:
            # Receiving Message From Client
            data = connection.recv(2048)
            jobSelection = int(data.decode()) - 1

            if int(jobSelection) <= len(self.jobList.listofjobs):

                #Adding Job Seeker to the Job Seeker List
                self.joinSeekerList(connection, jobSelection)

                #Decreases The Shown Amount of Seekers Needed for Accepted Job
                self.jobList.updateNumOfSeekers(jobSelection, False)

                #Keeps the Client Waiting Until JobCreator Starts Job
                self.waitForStart(connection)

            else:
                connection.send(pickle.dumps("Not Valid Input...\nEnter What Number Job You Would Like To Join"))

    # FoundJobSeeker-->viewingMenuJS-->acceptJob-->waitForStart
    def waitForStart(self, connection):

        connection.send(pickle.dumps("Press Enter to go to waiting Screen"))

        while True:
            for jobs in self.jobList.listofjobs:
                if jobs.getNumOfSeekers() == "Job Started":
                    connection.send(pickle.dumps("Press Enter to run "+jobs.getJobName()+ " Program"))

                    #Sending Key Word
                    connection.send(pickle.dumps(jobs.getJobName()))

                    self.jobCompletion = "Complete"
                else:
                    continue

    #Used to Send The Targets IP and Port to Job Seeker
    def sendTargetCredentials(self, connection, targetIP, targetPort):

        connection.send(pickle.dumps("Target Credentials"))

        connection.send(pickle.dumps(targetIP))

        connection.send(pickle.dumps(targetPort))

    '''             
    JOB CREATOR FUNCTIONS 
    '''
    # Client Identifies as a Job Creator
    def FoundJobCreator(self, connection):

        """
        :Description: This Function will Run when the Client identifies themselves as a Job Creator.
                        It will then send the Client a list of options to choose from, when one of these
                        choices are picked it will run another function to fulfil the job requested from
                        the Job Creator Client
        :param connection: This is the Socket which is used to send and receive message from the Client
        :return: VOID
        """

        # Sending Job Creator Options to Client
        connection.send(pickle.dumps("Job Creator Menu:\n1.View Jobs\n2.Create Job\n3.Exit\n"))

        while True:


            # Receiving Message From Client
            data = connection.recv(2048)
            optionSelection = data.decode()

            # View Jobs Condition
            if optionSelection == '1':
                self.viewingMenuJC(connection)

            # Create Job Condition
            if optionSelection == '2':
                self.jobCreationItems(connection)

            # Exit Condition
            if optionSelection == '3':
               self.threadedClient(connection)

            # Base Case Condition
            if optionSelection != '1' and optionSelection != '2' and optionSelection != '3':
                connection.send(pickle.dumps("Not a Valid Input...Try Again"))

    #FoundJobCreator-->viewingMenuJC
    def viewingMenuJC(self, connection):

        self.jobListView(connection)

        connection.send(pickle.dumps("Job Viewing Menu:\n1.Start Job\n2.View Seekers\n3.Exit"))

        while True:
            #Receiving Message From Client
            data = connection.recv(2048)
            optionSelection = int(data.decode())

            if optionSelection == 1:
                self.startJob(connection)
            elif optionSelection == 2:
                self.seekerListView(connection)
            elif optionSelection == 3:
                self.FoundJobCreator(connection)
            else:
                connection.send(pickle.dumps("Job Viewing Menu:\n1.Start Job\n2.View Seekers\n3.Exit"))

    #FoundJobCreator-->jobCreationItems
    def jobCreationItems(self, connection):

        # Sending Job Creator Options to Client
        connection.send(pickle.dumps(self.jobList.jobsToRequest))

        data = connection.recv(2048)
        jobNumber = data.decode()

        self.JobSelector(connection, int(jobNumber))

        #Sending Job Creator Options to Client
        self.FoundJobCreator(connection)

    #FoundJobCreator-->viewingMenuJC-->startJob
    def startJob(self, connection):

        connection.send(pickle.dumps("Please Enter What Number Job You Would Like To Start: "))

        #Receiving Message From Client
        data = connection.recv(2048)
        jobSelection = int(data.decode()) - 1

        self.jobList.updateNumOfSeekers(jobSelection, True)

        if self.jobList.listofjobs[jobSelection].getNumOfSeekers() == "Job Started":
            connection.send(pickle.dumps("Job Has Been Started\nPress Enter To Go Back To Job Creator Menu"))

            self.FoundJobCreator(connection)

        else:
            connection.send(pickle.dumps("Job Must Have 0 Seekers to Start\nPress Enter To Go Back To Job Creator Menu"))
            self.FoundJobCreator(connection)

    #Used to Get The Targets IP and Port From Job Creator (Inside def JobSelector(self, connection, jobNumber))
    def getTargetCredentials(self, connection):

        connection.send(pickle.dumps("Enter The Target's IP Address"))

        # Receiving Message From Client
        data = connection.recv(2048)
        self.targetIP = str(data.decode())

        connection.send(pickle.dumps("Enter The Target's Port if Port Not Needed Enter 0"))

        # Receiving Message From Client
        data = connection.recv(2048)
        self.targetPort = int(data.decode())

    '''             
    HELPER FUNCTIONS 
    '''
    def JobSelector(self, connection, jobNumber):

        connection.send(pickle.dumps("Enter The Job Creator's Name: "))

        data = connection.recv(2048)
        creatorName = data.decode()

        if jobNumber == 1:
            self.jobList.createIPOnlineDetectionJob(creatorName)

            self.getTargetCredentials(connection)
        elif jobNumber == 2:
            self.jobList.createSubnetIPOnlineDetection(creatorName)

            self.getTargetCredentials(connection)
        elif jobNumber == 3:
            self.jobList.specificPortStatusDetection(creatorName)

            self.getTargetCredentials(connection)
        elif jobNumber == 4:
            self.jobList.allPortStatusDetection(creatorName)

            self.getTargetCredentials(connection)
        elif jobNumber == 5:
            connection.send(pickle.dumps("Enter How Many Job Seekers Are Needed: "))

            data = connection.recv(2048)
            numOfSeekers = data.decode()

            self.jobList.createICMPFloodAttackJob(creatorName, numOfSeekers)

            self.getTargetCredentials(connection)
        elif jobNumber == 6:
            connection.send(pickle.dumps("Enter How Many Job Seekers Are Needed: "))

            data = connection.recv(2048)
            numOfSeekers = data.decode()

            self.jobList.createTCPFloodAttackJob(creatorName, numOfSeekers)

            self.getTargetCredentials(connection)
        elif jobNumber == 7:
            connection.send(pickle.dumps("Enter How Many Job Seekers Are Needed: "))

            data = connection.recv(2048)
            numOfSeekers = data.decode()

            self.jobList.createUDPFloodAttackJob(creatorName, numOfSeekers)

            self.getTargetCredentials(connection)

    #Helper Method for View Lists
    def jobListView(self, connection):

        #Condition for No Jobs In Job List
        if len(self.jobList.listofjobs) == 0:
            connection.send(pickle.dumps("No Jobs Posted"))
        else:
            connection.send(pickle.dumps(self.jobList.listofjobs))

    #Helper Method to View Seeker List
    def seekerListView(self, connection):

        connection.send(pickle.dumps("Please Enter What Job Number You Would Like To View the Active Seekers: "))

        #Receiving Message From Client
        data = connection.recv(2048)
        jobSelection = int(data.decode()) - 1

        if len(self.activeJobsWithSeekers) == 0:
            connection.send(pickle.dumps("No Active Job Seekers\nPress Enter to Return to Job Viewing Screen"))

            #Client Must Send Empty Space To Obtain This Message
            self.FoundJobCreator(connection)
        else:
            connection.send(pickle.dumps(self.activeJobsWithSeekers[jobSelection].getJobSeekerList()))

            #Client Must Send Empty Space To Obtain This Message
            self.FoundJobCreator(connection)

    #SeekerList Gets Appended
    def joinSeekerList(self, connection, jobNumber):
        #Sending Message to Client to Send Job Seeker Name
        connection.send(pickle.dumps("Please Enter Your Name (Will Be Added To Job Seeker List): "))

        #Receiving Message From Client
        data = connection.recv(2048)
        SeekerName = data.decode()

        #Updating Client Specific Job Seeker List
        self.jobList.listofjobs[jobNumber].getJobSeekerList().append(SeekerName)

        #Updating Server Specific Job Seeker List with Client Specific Job Seeker List
        self.activeJobsWithSeekers.append(self.jobList.listofjobs[jobNumber])

    def matchJobs(self, jobNumber):
        count = -1
        for job in self.jobList.listofjobs:
            count+=1
            if job.getFullJob() == self.activeJobsWithSeekers[count].getFullJob():
                print()


if __name__ == "__main__":
    s = Server()
    s.main()
