import socket
import sys
import pickle
from _thread import *
from JobList import *

class Server(object):
    """
    Tasks to Develop or Fix
    -Viewing Joined Jobs (Job Seeker)
    -Write Target IP and/or Target Port to .txt (Job Creator)
    -Connect Group Members .py scripts

    Bugs to Work Out:
    -After Certain Actions The Client Needs to Send Blank Space to Continue
    -Setting Job to Finished as Soon as The Job Gets Started

    Server & Client Functions:
    -Determine if the Client is a Job Creator or Job Seeker
    -Job Creators can Post Jobs
    -Job Seekers can Join Jobs
    -Job Creators and Job Seekers can View the Job List
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
        connection.send(pickle.dumps("1.View Jobs\n2.Exit\n"))

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
                connection.send(pickle.dumps("Not a Valid Input...\n1.View Jobs\n2.Exit\n"))

    #FoundJobSeeker-->viewingMenuJS
    def viewingMenuJS(self, connection):

        self.jobListView(connection)

        connection.send(pickle.dumps("1.Join Job\n2.Go Back"))

        while True:
            #Receiving Message From Client
            data = connection.recv(2048)
            optionSelection = int(data.decode())

            if optionSelection == 1:
                self.acceptJob(connection)

            elif optionSelection == 2:
                self.FoundJobSeeker(connection)
            else:
                connection.send(pickle.dumps("Not Valid Input...\n1.Join Job\n2.Go Back"))

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
        connection.send(pickle.dumps("1.View Jobs\n2.Create Job\n3.Exit\n"))

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
               sys.exit(0)

            # Base Case Condition
            if optionSelection != '1' and optionSelection != '2' and optionSelection != '3':
                connection.send(pickle.dumps("Not a Valid Input...Try Again"))

    #FoundJobCreator-->viewingMenuJC
    def viewingMenuJC(self, connection):

        self.jobListView(connection)

        connection.send(pickle.dumps("1.Start Job\n2.View Seekers\n2.Exit"))

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
                connection.send(pickle.dumps("Not Valid Input...\n1.Start Job\n2.Exit"))

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
            connection.send(pickle.dumps("Job Has Been Started\nPress Enter to Wait for Job Completion"))

            self.waitForCompletion(connection, jobSelection)

        else:
            connection.send(pickle.dumps("Job Must Have 0 Seekers to Start"))

    #FoundJobCreator-->viewingMenuJC-->startJob-->waitForCompletion
    def waitForCompletion(self, connection, jobSelection):

        while self.jobList.listofjobs[jobSelection].getNumOfSeekers() == "Job Started":

            if self.jobCompletion == "Complete":
                connection.send(pickle.dumps("Job Finished\nPress Enter To Go Back To Main Menu"))
                self.FoundJobCreator(connection)
            else:
                continue

    '''             
    HELPER FUNCTIONS 
    '''
    def JobSelector(self, connection, jobNumber):

        connection.send(pickle.dumps("Enter The Job Creator's Name: "))

        data = connection.recv(2048)
        creatorName = data.decode()

        if jobNumber == 1:
            self.jobList.createIPOnlineDetectionJob(creatorName)

            connection.send(pickle.dumps("Job Has Been Created and Posted\nPress Enter to Continue"))
        elif jobNumber == 2:
            self.jobList.createSubnetIPOnlineDetection(creatorName)

            connection.send(pickle.dumps("Job Has Been Created and Posted\nPress Enter to Continue"))
        elif jobNumber == 3:
            self.jobList.specificPortStatusDetection(creatorName)

            connection.send(pickle.dumps("Job Has Been Created and Posted\nPress Enter to Continue"))
        elif jobNumber == 4:
            self.jobList.allPortStatusDetection(creatorName)

            connection.send(pickle.dumps("Job Has Been Created and Posted\nPress Enter to Continue"))
        elif jobNumber == 5:
            connection.send(pickle.dumps("Enter How Many Job Seekers Are Needed: "))

            data = connection.recv(2048)
            numOfSeekers = data.decode()

            self.jobList.createICMPFloodAttackJob(creatorName, numOfSeekers)

            connection.send(pickle.dumps("Job Has Been Created and Posted\nPress Enter to Continue"))
        elif jobNumber == 6:
            connection.send(pickle.dumps("Enter How Many Job Seekers Are Needed: "))

            data = connection.recv(2048)
            numOfSeekers = data.decode()

            self.jobList.createTCPFloodAttackJob(creatorName, numOfSeekers)

            connection.send(pickle.dumps("Job Has Been Created and Posted\nPress Enter to Continue"))
        elif jobNumber == 7:
            connection.send(pickle.dumps("Enter How Many Job Seekers Are Needed: "))

            data = connection.recv(2048)
            numOfSeekers = data.decode()

            self.jobList.createUDPFloodAttackJob(creatorName, numOfSeekers)

            connection.send(pickle.dumps("Job Has Been Created and Posted\nPress Enter to Continue"))

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

        connection.send(pickle.dumps(self.activeJobsWithSeekers[0].getJobSeekerList()))

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

if __name__ == "__main__":
    s = Server()
    s.main()
