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
  VIEWACTIVEJOBS <SEEKERNAME>
  
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
                      "STARTJOB <CREATORNAME> <JOBTYPE>", "VIEWACTIVEJOBS <SEEKERNAME>", "JOBTYPE SELECTION:", 
                      "<IP Online Detection>", "<Subnet IP Online Detection>", "<Specific Port Status Detection>",
                      "<All Port Status Detection>", "<ICMP Flood Attack>", "<TCP Flood Attack>", "<UDP Flood Attack>"]
  
  def __init__(self):
    self.jobListOBJ = JobList()
    self.COMMAND = ""
    self.parameterList = []
    
  def connectionMessage(self):
    self.connection.send(pickle.dumps(connectionMessage))
  
  def ParseCommand(self, Command):
    self.parameterList = Command.split(" ")
    
  def createJob(self, parameterList):
    self.jobListOBJ.createJob(parameterList[1], parameterList[2], parameterList[3], parameterList[4], parameterList[5])
  
  def removeJob(self, parameterList):
    for Job in self.jobListOBJ.listofjobs:
      if Job.fullJob == parameterList:
        self.connection.send(pickle.dumps("Job Removed"))
        self.jobListOBJ.listofjobs.remove(Job)

  
  def viewJobs(self):
  
  def checkJobTeam(self, parameterList):
  
  def joinJob(self, parameterList):
  
  def startJob(self, parameterList):
  
  def viewActiveJobs(self):
