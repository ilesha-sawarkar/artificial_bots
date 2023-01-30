import math

import pybullet

import pyrosim.pyrosim as pyrosim

import pyrosim.constants as c

class NEURON: 

    def __init__(self,line):

        self.Determine_Name(line)

        self.Determine_Type(line)

        self.Search_For_Link_Name(line)

        self.Search_For_Joint_Name(line)

        self.Set_Value(0.0)
        
        #self.type

    def Add_To_Value( self, value ):

        self.Set_Value( self.Get_Value() + value )

    def Get_Joint_Name(self):

        return self.jointName

    def Get_Link_Name(self):

        return self.linkName

    def Get_Name(self):

        return self.name

    def Get_Value(self):

        return self.value

    def Is_Sensor_Neuron(self):

        return self.type == c.SENSOR_NEURON

    def Is_Hidden_Neuron(self):

        return self.type == c.HIDDEN_NEURON

    def Is_Motor_Neuron(self):

        return self.type == c.MOTOR_NEURON

    def Print(self):

        # self.Print_Name()

        # self.Print_Type()

        self.Print_Value()

        # print("")

    def Set_Value(self,value):

        self.value = value
    
    def Update_Sensor_Neuron(self): #new method
        self.value = pyrosim.Get_Touch_Sensor_Value_For_Link(
            self.Get_Link_Name())
        self.Set_Value(pyrosim.Get_Touch_Sensor_Value_For_Link(
            self.Get_Link_Name()))
        
    def Allow_Presynaptic_Neuron_To_Influence_Me(self, current_synapse_weight, presynaptic_neuron_value):
            self.Add_To_Value(presynaptic_neuron_value * current_synapse_weight)
            
    def Update_Hidden_Or_Motor_Neuron(self, neurons, synapses): #new method
        self.Set_Value(0.0)
        
        for synapse in synapses:
            #current_synapse_weight = synapses[synapse].Get_Weight()
            #presynaptic_neuron_value = neurons[synapse[0]].Get_Value()
            
            #print(current_synapse_weight)
            #print(presynaptic_neuron_value)
            if  synapse[1] == self.Get_Name():
                current_synapse_weight = synapses[synapse].Get_Weight()
                presynaptic_neuron_value = neurons[synapse[0]].Get_Value()
                #print("\n\n------------")
                #print(current_synapse_weight)
                #print(presynaptic_neuron_value)
                self.Allow_Presynaptic_Neuron_To_Influence_Me(current_synapse_weight, presynaptic_neuron_value)
                self.Threshold()
                
    
        
# -------------------------- Private methods -------------------------

    def Determine_Name(self,line):

        if "name" in line:

            splitLine = line.split('"')

            self.name = splitLine[1]

    def Determine_Type(self,line):

        if "sensor" in line:

            self.type = c.SENSOR_NEURON

        elif "motor" in line:

            self.type = c.MOTOR_NEURON

        else:

            self.type = c.HIDDEN_NEURON

    def Print_Name(self):

       print(self.name)

    def Print_Type(self):

       print(self.type)

    def Print_Value(self):

       print(self.value , " " , end="" )

    def Search_For_Joint_Name(self,line):

        if "jointName" in line:

            splitLine = line.split('"')

            self.jointName = splitLine[5]

    def Search_For_Link_Name(self,line):

        if "linkName" in line:

            splitLine = line.split('"')

            self.linkName = splitLine[5]

    def Threshold(self):

        self.value = math.tanh(self.value)
        