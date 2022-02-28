from utilities import singleton
import requests
import json
import debugpy


@singleton
class PlatformIOCommunication:
    """
    This class is used to send and receive messages to the platform.
    """    

    def __init__(self):
        self.base_link  = "http://127.0.0.1:8080"
        self.__online = self._is_platform_online()

    def send_message(self, message):
        """
        This method is used to send a message to the platform.

        Parameters 
        ----------
        message : str
            The message to be sent.
        """
        if self.__online:
            response = requests.post(self.base_link + "/add_message", data = json.dumps({'text':message}))
            pass

    def receive_message(self) -> str:
        """
        This method is used to receive a message from the platform.

        Returns
        -------
        str
            The message received from the platform.
        """
        if self.__online:
            response = requests.get(self.base_link + "/get_em_message")
            return response.json()['text']
        return ""
    
    def send_error_message(self, message):
        """
        This method is used to send an error message to the platform.

        Parameters
        ----------
        message : str
            The error message to be sent.
        """
        if self.__online:
            response = requests.post(self.base_link + "/add_error_message", data = json.dumps({'text':message, "error_type": ""}))
            pass

    def _is_platform_online(self) -> bool:
        """
        This method is used to check if the API of the evaluation platform is online.

        Returns
        -------
        bool
            True if the API is online, False otherwise.
        """
        try:
            response = requests.head(self.base_link + "/")
            if response.status_code == 200:
                return True
            else:
                return False
        except:
            return False

