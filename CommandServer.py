from JobList import *
import pickle

class Server(object):
  """
  Server<---->Client
  Command List:
  CREATEJOB  <CREATORNAME> <JOBTYPE> <NUMOFSEEKERS> <TARGETIP> <TARGETPORT>
  REMOVEJOB  <CREATORNAME> <JOBTYPE> <NUMOFSEEKERS> <TARGETIP> <TARGETPORT>
  VIEWJOBS
  CHECKJOBTEAM <CREATORNAME> <JOBTYPE>
  JOINJOB <CREATORNAME> <JOBTYPE> <SEEKERNAME>
  STARTJOB <CREATORNAME> <JOBTYPE>
  
  PREDEFINED VARIABLES
  JOBTYPE->
           <IP Online Detection>
           <Subnet IP Online Detection>
           <Specific Port Status Detection>
           <All Port Status Detection>
           <ICMP Flood Attack>
           <TCP Flood Attack>
           <UDP Flood Attack>
  """
  connectionMessage = ["CREATEJOB  <CREATORNAME> <JOBTYPE> <NUMOFSEEKERS> <TARGETIP> <TARGETPORT>",
                      "REMOVEJOB  <CREATORNAME> <JOBTYPE> <NUMOFSEEKERS> <TARGETIP> <TARGETPORT>",
                      "VIEWJOBS", "CHECKJOBTEAM <CREATORNAME> <JOBTYPE>", "JOINJOB <CREATORNAME> <JOBTYPE> <SEEKERNAME>",
                      "STARTJOB <CREATORNAME> <JOBTYPE>", "JOBTYPE SELECTION:", 
                      "<IP Online Detection>", "<Subnet IP Online Detection>", "<Specific Port Status Detection>",
                      "<All Port Status Detection>", "<ICMP Flood Attack>", "<TCP Flood Attack>", "<UDP Flood Attack>"]
  
  def __init__(self):
    self.ServerSocket = socket.socket()
    self.host = '127.0.0.1'
    self.port = 1233
    self.ThreadCount = 0
    self.jobListOBJ = JobList()
    self.command = ""
    self.parameterList = []
    
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
    self.connectionMessage()
    
    while true:
      #Limiting to 2048 Bytes
      clientMessage = connection.recv(2048)

      #Receiving Message From Client
      self.command = clientMessage.pickle.loads(clientMessage)
      
      self.ParseCommand(self.command)
      
      self.commandRouting(self.parameterList)
      
      
  
  def connectionMessage(self):
    self.connection.send(pickle.dumps(connectionMessage))
  
  def ParseCommand(self, Command):
    self.parameterList = Command.split(" ")
    
  def createJob(self, parameterList):
    self.connection.send(pickle.dumps("Job has been created and added to the Job List"))
    self.jobListOBJ.createJob(parameterList[1], parameterList[2], parameterList[3], parameterList[4], parameterList[5])
  
  def removeJob(self, parameterList):
    for Job in self.jobListOBJ.listofjobs:
      if Job.jobParameters == parameterList:
        self.connection.send(pickle.dumps(Job.FullJob+" has been removed from the Job List"))
        self.jobListOBJ.listofjobs.remove(Job)
        
  def viewJobs(self):
    self.connection.send(pickle.dumps(jobListOBJ.listofjobs))
  
  def checkJobTeam(self, parameterList):
    for Job in self.jobListOBJ.listofjobs:
      if Job.jobParameters == parameterList:
        self.connection.send(pickle.dumps(Job.JobSeekerList))
        
  
  def joinJob(self, parameterList, seekerName):
    for Job in self.jobListOBJ.listofjobs:
      if Job.jobParameters == parameterList:
        self.connection.send(pickle.dumps(seekerName+" has joined: "+Job.FullName))
        Job.JobSeekerList.add(seekerName)
        
  
  def startJob(self, parameterList):
    for Job in self.jobListOBJ.listofjobs:
      if Job.jobParameters == parameterList:
        Job.setNumOfSeekers("Job Started")
  
  def commandRouting(parameterList):
    if parameterList[0] == "CREATEJOB":
      self.createJob()  
    elif parameterList[0] == "REMOVEJOB":
      self.removeJob()
    elif parameterList[0] == "VIEWJOBS":
      self.viewJob()
    elif parameterList[0] == "CHECKJOBTEAM":
      self.checkJobTeam()
    elif parameterList[0] == "JOINJOB":
      self.joinJob()
    elif parameterList[0] == "STARTJOB":
      self.startJob()
    else:
      self.connection.send(pickle.dumps("Invalid Command"))
