from JobList import *

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
  
  def __init__(self):
    self.jobListOBJ = JobList()
    
    self.COMMAND = ""
    self.parameterList = []
  
  def ParseCommand(self, Command):
    self.parameterList = Command.split(" ")
    
  def createJob(self, CREATORNAME, JOBTYPE, NUMOFSEEKERS, TARGETIP, TARGETPORT):
    self.jobListOBJ.createJob(CREATORNAME, JOBTYPE, NUMOFSEEKERS, TARGETIP, TARGETPORT)
  
  def removeJob(self, CREATORNAME, JOBTYPE, NUMOFSEEKERS, TARGETIP, TARGETPORT):
  
  def viewJobs(self):
  
  def checkJobTeam(self, CREATORNAME, JOBTYPE):
  
  def joinJob(self, CREATORNAME, JOBTYPE, SEEKERNAME):
  
  def startJob(self, CREATORNAME, JOBTYPE):
  
  def viewActiveJobs(self):
  
  def CommandtoFunction(self):
    if self.parameterList[0] == "CREATEJOB":
      self.createJob()
