import json
import importlib.resources as pkg_resources
import json_data
import logging
import queue
from camelot_IO_communication import CamelotIOCommunication
from camelot_input_multiplexer import CamelotInputMultiplexer
"""
Inputs: Json file with the description of each action
Outputs: 
"""
#TODO: check if parameters in action are what camelot expects
class CamelotAction:

    def __init__(self):
        self.camelot_input_multiplex = CamelotInputMultiplexer()
        self.camelot_input_multiplex.start()
        self.camelot_IO_communication = CamelotIOCommunication()
        self.success_messages = queue.Queue()
        with pkg_resources.open_text(json_data, 'Actionlist.json') as json_file:
            self.json_data_r = json.load(json_file)

    
    '''
    Purpose: Waits for success or fail response from Camelot
    Inputs: command that was sent to Camelot
    Outputs: True for success, False for failure
    '''

    def check_for_success(self,command):

        # Keep getting responses until the success of fail the given command is received
        while True:

            # Get response from Camelot
            received = self.camelot_input_multiplex.get_success_message()
            logging.debug("Camelot output: %s" % received)
            
            # Return True if success response, else false for fail response
            if received == 'succeeded ' + command:
                self.success_messages.put(received)
                return True
            elif received.startswith('failed ' + command):
                return False
            elif received.startswith('error ' + command):
                return False

    '''
    Purpose: Format an action for interpretation by Camelot
    Inputs: Action to be sent to Camelot
    Outputs: True for success, False for failure
    '''
    def action(self, action_name, parameters = [] , wait=True):
        if(not any(d['name'] == action_name for d in self.json_data_r)):
            raise KeyError("Action name {:} does not exist. The parameter Action Name is case sensitive.".format(action_name))
        if(type(parameters) == bool):
            wait = parameters
            parameters = []

        action_data = [d for d in self.json_data_r if d['name'] == action_name][0]
        
        if(len(parameters) > 0):
            self._check_action_parameters(action_data, parameters)

        # Format commands
        # This method assumes that the parameters are checked and ok to be printed
        command = self._generate_camelot_string(action_name, parameters, action_data)
        

        self.camelot_IO_communication.print_action('start ' + command)
        # open(0).write('start ' + command)
        #print('start ' + command)

        if wait==True:
            # Call function to check for its success
            return self.check_for_success(command)
        else:
            return True
    
    def _generate_camelot_string(self, action_name, parameters, action_data):
        command = action_name + "("
        index = 0
        for item in parameters:
            if(type(item) == str and action_data['param'][index]['type'] == "String"):
                command += '"' + item + '"'
            elif(type(item) == bool):
                command += str(item).lower()
            else:
                command += item
            command += ', '
            index += 1
        if(index > 0):
            command = command[:-2]
        command += ")"
        return command
    
    def _check_action_parameters(self, action_data, parameters):
        nparam = 0
        for item in action_data['param']:
            if(item['default'] == 'REQUIRED'):
                nparam += 1
        
        if(len(parameters) < nparam):
            raise KeyError("Number of parameters less then REQUIRED ones.")


