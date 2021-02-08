import pickle
import socket
from _thread import *
from JobList import *
from JobCreator import *
from JobSeeker import *
from FileRecord import *
import sys
try:
    from ip2geotools.databases.noncommercial import DbIpCity
except ImportError:
    print("Need to install ip2geotools to continue")
    sys.exit(0)

class Server(object):

    #Message Variables:
    initialConnectionMessage = ["LOGIN <USERNAME> <PASSWORD> <POSITION>", "POSITION SELECTION: ", "<JobCreator>",
                                "<JobSeeker>"]

    jobCreatorCommandMessage = ["CREATEJOB  <CREATORNAME> <JOBTYPE> <NUMOFSEEKERS> <TARGETIP> <TARGETPORT>",
                                "REMOVEJOB <CREATORNAME> <JOBTYPE> <NUMOFSEEKERS> <TARGETIP> <TARGETPORT>",
                                "VIEWJOBS",
                                "STARTJOB <CREATORNAME> <JOBTYPE>",
                                "JOBTYPE SELECTION: ",
                                "<IPDetection>", "<PortDetection>",
                                "<TCPFloodAttack>", "<UDPFloodAttack>",
                                "<NodeLocation>", "<NodeLANScan>"]

    jobSeekerCommandMessage = ["VIEWJOBS",
                               "JOINJOB <CREATORNAME> <JOBTYPE> <SEEKERNAME>",
                               "COMPLETEJOB <CREATORNAME> <JOBTYPE> <TARGETIP> <TARGETPORT>"]

    def __init__(self):
        self.ServerSocket = socket.socket()
        self.host = '127.0.0.1'
        self.port = 1233
        self.ThreadCount = 0
        self.jobListOBJ = JobList()
        self.fileRecordOBJ = FileRecord()
        self.jobCreatorList = []
        self.jobSeekerList = []
        self.command = ""
        self.parameterList = []
        self.readBackup()
        self.count = 0


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

    #COMPLETE
    def threadedClient(self, connection):
        self.connectionMessage(connection)

        while True:
            # Limiting to 2048 Bytes
            clientMessage = connection.recv(2048)

            # Receiving Message From Client
            self.command = pickle.loads(clientMessage)

            self.ParseCommand(self.command)

            self.commandRouting(connection, self.parameterList)

    #COMPLETE
    def connectionMessage(self, connection):
        connection.send(pickle.dumps(self.initialConnectionMessage))

    #COMPLETE
    def ParseCommand(self, Command):
        self.parameterList = Command.split(" ")

    #COMPLETE
    def login(self, connection, parameterList):
        if parameterList[3] == "JobCreator":
            self.jobCreatorList.append(JobCreator(parameterList[1], parameterList[2]))
            connection.send(pickle.dumps(self.jobCreatorCommandMessage))

        elif parameterList[3] == "JobSeeker":
            self.jobCreatorList.append(JobSeeker(parameterList[1], parameterList[2]))
            connection.send(pickle.dumps(self.jobSeekerCommandMessage))
        else:
            connection.send(pickle.dumps("Not a valid position"))

    #COMPLETE
    def createJob(self, connection, parameterList):
        connection.send(pickle.dumps("Job has been created and added to the Job List"))
        self.jobListOBJ.updateJobList(parameterList[1], parameterList[2], parameterList[3], parameterList[4],
                                      parameterList[5])

        self.fileRecordOBJ.updateJobListBackup(self.jobListOBJ.listofjobs)

    #COMPLETE
    def removeJob(self, connection, parameterList):
        for Job in self.jobListOBJ.listofjobs:
            if Job.jobParameters[0] == parameterList[1] and Job.jobParameters[1] == parameterList[2]:
                connection.send(pickle.dumps(Job.FullJob + " has been removed from the Job List"))
                self.jobListOBJ.listofjobs.remove(Job)
            else:
                connection.send(pickle.dumps("Entered Job Does Not Exist In Job List"))

    #COMPLETE
    def viewJobs(self, connection):
        if len(self.jobListOBJ.listofjobs) == 0:
            connection.send(pickle.dumps("No Jobs Posted"))
        else:
            try:
                connection.send(pickle.dumps(self.jobListOBJ.listofjobs))
            except EOFError:
                pass

    #COMPLETE
    def joinJob(self, connection, parameterList):
        count = 0
        for Job in self.jobListOBJ.listofjobs:
            count += 1

            if Job.jobParameters[0] == parameterList[1] and Job.jobParameters[1] == parameterList[
                2] and Job.NumOfSeekers == "Job Started":
                connection.send(pickle.dumps("Job is full"))
                break

            if count > len(self.jobListOBJ.listofjobs):
                connection.send(pickle.dumps("Entered Job Does Not Exist In Job List"))
                break

            if Job.jobParameters[0] == parameterList[1] and Job.jobParameters[1] == parameterList[2] and int(
                    Job.NumOfSeekers) != 0:
                connection.send(pickle.dumps(parameterList[3] + " has joined: " + Job.FullJob))
                Job.JobSeekerList.append(parameterList[3])
                Job.NumOfSeekers = int(Job.NumOfSeekers) - 1
                Job.NumOfSeekers = str(Job.NumOfSeekers)
                break

    #COMPLETE
    def startJob(self, connection, parameterList):
        count = 0
        for Job in self.jobListOBJ.listofjobs:
            count += 1
            if count > len(self.jobListOBJ.listofjobs):
                connection.send(pickle.dumps("Entered Job Does Not Exist In Job List"))
                break

            if Job.jobParameters[0] == parameterList[1] and Job.jobParameters[1] == parameterList[2]:
                connection.send(pickle.dumps(Job.FullJob + " has been started"))
                Job.setNumOfSeekers("Job Started")
                break

    #COMPLETE
    def completeJob(self, connection, parameterList):

        print("Sending Job Type To Client")
        connection.send(pickle.dumps(parameterList[2]))
        print("Sending Target IP To Client (If Needed)")
        connection.send(pickle.dumps(parameterList[3]))
        print("Sending Target Port To Client (If Needed)")
        connection.send(pickle.dumps(parameterList[4]))

        print("Waiting For Response From Client")

        #Limiting to 2048 Bytes
        clientOutput = connection.recv(2048)

        print("Received Response From Client")

        #Receiving Message From Client
        clientCompletion = pickle.loads(clientOutput)

        print("Response From Client Saved")

        #Recording Multi Lined Client Output
        if type(clientCompletion) == list:

            for hosts in clientCompletion:
                self.fileRecordOBJ.recordOutput(hosts)

        #Recording Single Lined Client Output
        else:
            self.fileRecordOBJ.recordOutput(clientCompletion)

    #COMPLETE
    def commandRouting(self, connection, parameterList):
        if parameterList[0] == "LOGIN":
            self.login(connection, parameterList)
        elif parameterList[0] == "CREATEJOB":
            self.createJob(connection, parameterList)
        elif parameterList[0] == "REMOVEJOB":
            self.removeJob(connection, parameterList)
        elif parameterList[0] == "VIEWJOBS":
            self.viewJobs(connection)
        elif parameterList[0] == "JOINJOB":
            self.joinJob(connection, parameterList)
        elif parameterList[0] == "STARTJOB":
            self.startJob(connection, parameterList)
        elif parameterList[0] == "COMPLETEJOB":
            self.completeJob(connection, parameterList)
        else:
            connection.send(pickle.dumps("Invalid Command"))

    #COMPLETE
    def readBackup(self):
        try:
            backup = open("JobBackup.txt", 'r')
            backupList = backup.readlines()

            for lines in backupList:
                self.ParseCommand(lines.rstrip('\n'))
                self.jobListOBJ.updateJobList(self.parameterList[0], self.parameterList[1], self.parameterList[2],
                                              self.parameterList[3], self.parameterList[4])
            print("Jobs Have Been Restored")
        except IOError:
            pass


if __name__ == "__main__":
    s = Server()
    s.main()