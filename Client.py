import socket
import sys
import pickle


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

        # Creating Client Socket Object
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Connecting Client--->Server
        self.client.connect((self.SERVER, self.PORT))

    def JobCorS(self):

        # When True The Client Can Send and Receive Messages
        while True:

            count = 1

            # Limiting to 1024 bytes
            in_data = self.client.recv(2048)

            # Sets in_data to what is sent from the Server
            in_data = pickle.loads(in_data)

            # If JobList is sent from Server Print the Job List
            if type(in_data) == list:
                for job in in_data:
                    for element in job:
                        print(count + ": " + element, end=" ")
                        count += 1
                    print()
            else:
                print(in_data)

            # Getting Message For Server
            out_data = input()

            # Sending Message To Server
            self.client.sendall(bytes(out_data, 'UTF-8'))

        # Closing the Socket Connection
        self.client.close()

    def main(self):
        self.JobCorS()


if __name__ == "__main__":
    s = Client()
    s.main()