import socket
import sys
import pickle
from _thread import *
from JobList import *


class Server(object):

    def __init__(self):

        self.ServerSocket = socket.socket()
        self.host = '127.0.0.1'
        self.port = 1233
        self.ThreadCount = 0
        self.jobList = JobList()

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
                connection.send(bytes("Not a Valid Input...Try Again", 'UTF-8'))

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
                sys.exit(0)

            # Base Case Condition
            if optionSelection != '1' and optionSelection != '2':
                connection.send(pickle.dumps("Not a Valid Input...Try Again"))

    #FoundJobSeeker-->viewingMenuJS
    def viewingMenuJS(self, connection):

        self.jobListView(connection)

        connection.send(pickle.dumps("1.Join Job\n2.Exit"))

        #Receiving Message From Client
        data = connection.recv(2048)
        optionSelection = int(data.decode())

        if optionSelection == 1:
            self.acceptJob(connection)

        elif optionSelection == 2:
            print("Exit")
        else:
            connection.send(pickle.dumps("Not Valid Input"))

    #FoundJobSeeker-->viewingMenuJS-->acceptJob
    def acceptJob(self, connection):

        #Sending Message to Client to Send What Number Of Job They Want to Join
        connection.send(pickle.dumps("Please Enter What Number Job You Would Like To Join"))

        # Receiving Message From Client
        data = connection.recv(2048)
        jobSelection = int(data.decode()) - 1

        #Sending Message to Client to Send Job Seeker Name
        connection.send(pickle.dumps("Please Enter Your Name (Will Be Added To Job Seeker List): "))

        # Receiving Message From Client
        data = connection.recv(2048)
        SeekerName = data.decode()

        #Adding Job Seeker to the Job Seeker List
        self.jobList.updateJobSeekerList(jobSelection, SeekerName)

        #Decreases The Shown Amount of Seekers Needed for Accepted Job
        self.jobList.updateNumOfSeekers(jobSelection)

        #Sending Message to Client to Send Job Seeker Name
        connection.send(pickle.dumps("Please Enter Your Name (Will Be Added To Job Seeker List): "))

        # Receiving Message From Client
        data = connection.recv(2048)
        SeekerName = data.decode()

        #Adding Job Seeker to the Job Seeker List
        self.jobList.updateJobSeekerList(jobSelection, SeekerName)

        #Decreases The Shown Amount of Seekers Needed for Accepted Job
        self.jobList.updateNumOfSeekers(jobSelection)

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

        connection.send(pickle.dumps("1.Start Job\n2.Exit"))

        #Receiving Message From Client
        data = connection.recv(2048)
        optionSelection = int(data.decode())

        if optionSelection == 1:
            self.startJob(connection)

        elif optionSelection == 2:
            print("Exit")
        else:
            connection.send(pickle.dumps("Not Valid Input"))

    #FoundJobCreator-->jobCreationItems
    def jobCreationItems(self, connection):

        # Sending Job Creator Options to Client
        connection.send(pickle.dumps("Enter name of Job Creator:"))
        data = connection.recv(2048)
        creatorsName = data.decode()

        connection.send(pickle.dumps("Enter the job name:"))
        data = connection.recv(2048)
        jobName = data.decode()

        connection.send(pickle.dumps("Enter number of job seekers:"))
        data = connection.recv(2048)
        numofSeekers = data.decode()

        self.jobList.updateJobList(creatorsName, jobName, numofSeekers)

        # Sending Job Creator Options to Client
        connection.send(pickle.dumps("1.View Jobs\n2.Create Job\n3.Exit\n"))

    #FoundJobCreator-->viewingMenuJC-->startJob
    def startJob(self, connection):

        connection.send(pickle.dumps("Please Enter What Number Job You Would Like To Start: "))

        #Receiving Message From Client
        data = connection.recv(2048)
        jobSelection = int(data.decode()) - 1

        if int(self.jobList.obtainNumOfSeekers(jobSelection)) == 0:
            connection.send(pickle.dumps("Job Has Been Started"))

        else:
            connection.send(pickle.dumps("Job Must Have 0 Seekers to Start"))


    '''             
    HELPER FUNCTIONS 
    '''
    #Helper Method for View Lists
    def jobListView(self, connection):

        #Condition for No Jobs In Job List
        if len(self.jobList.listofjobs) == 0:
            connection.send(pickle.dumps("No Jobs Posted"))
        else:
            connection.send(pickle.dumps(self.jobList.listofjobs))

if __name__ == "__main__":
    s = Server()
    s.main()
