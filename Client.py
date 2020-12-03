import pickle
from FloodAttack import *

'''
After Client runs Job Specific Program (EX: UDP Flood Attack)
Send Message to Server to tell Job Creator the job is complete
'''


class Client(object):

    def __init__(self):
        """
        Name: Client Constructor
        Type: void
        Description: This constructor will save all the necessary variables that will be used
                    in the other class functions
        """

        # Server Information
        self.SERVER = "127.0.0.1"
        self.PORT = 1233

        # Target Information
        self.targetIP = "1.1.1.1"
        self.targetPort = 25565

        # Needed Objects
        self.udpAttack = FloodAttack()

        # Needed Variables
        self.serverMessage = ''

        # Creating Client Socket Object
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connecting Client--->Server
        self.client.connect((self.SERVER, self.PORT))

    '''
    HELPER Functions
    '''

    # Handles and Chooses Right Path For Server Messages
    def serverMessageHandler(self):

        # When True The Client Can Send and Receive Messages
        while True:
            # Refresh Buffer For New Server Message
            self.resetServerMessage()

            self.obtainList(self.serverMessage)
            
            # Gathering Input From Client to send to Server
            clientMessage = input()

            # Sending Message To Server
            self.client.send(pickle.dumps(clientMessage))

    # Takes in Server Message to Run Specific Job
    def jobPrograms(self, serverMessage):
        if in_data == "IP Online Detection":
            print("Job 1")
        elif in_data == "Subnet IP Online Detection":
            print("Job 2")
        elif in_data == "Specific Port Status Detection":
            print("Job 3")
        elif in_data == "All Port Status Detection":
            print("Job 4")
        elif in_data == "ICMP Flood Attack":
            print("Job 5")
        elif in_data == "TCP Flood Attack":
            print("Job 6")
        elif in_data == "UDP Flood Attack":
            self.udpAttack.sendUDPPackets(self.targetIP, self.targetPort)

    #Prints List Messages From Server
    def obtainList(self, serverMessage):
        count = 1

        # If JobList is sent from Server Print the Job List
        if type(serverMessage) == list:
            for job in serverMessage:
                print(str(count) + ":", end=" ")
                count += 1
                for element serverMessage:
                    if len(element) == 1:
                        print(element, end="")
                    else:
                        print(element, end=" ")
                print()
        else:
            print(serverMessage)

    # Prints Single Lined Messages From Server
    def normalCommunication(self, serverMessage):
        if type(serverMessage) != list:
            print(serverMessage)

    # Sets The Global Target Credentials (Job Seeker)
    def setTargetCredentials(self, serverMessage):

        if serverMessage == "Target Credentials":
            print("Obtaining Target Information")

            # Refresh Buffer For New Server Message
            self.resetServerMessage()

            # Setting Global targetIP
            self.targetIP = str(serverMessage)
            print(self.targetIP)

            # Refresh Buffer For New Server Message
            self.resetServerMessage()

            # Setting Global targetPort
            self.targetPort = int(serverMessage)
            print(self.targetPort)

            # Skip Blank Space
            print("Press Enter to Continue")

    # Refresh Buffer For New Server Message
    def resetServerMessage(self):
        # Limiting to 2048 bytes
        self.serverMessage = self.client.recv(2048)

        # Sets in_data to what is sent from the Server
        self.serverMessage = pickle.loads(self.in_data)

    # Closes Connection to Server
    def closeConnection(self, serverMessage):
        if serverMessage == 'exit':
            self.client.close()

    # Main Function
    def main(self):
        self.serverMessageHandler()


# Start Main Function
if __name__ == "__main__":
    s = Client()
    s.main()
