from pyrosim.commonFunctions import Save_Whitespace

class MATERIAL: 

    def __init__(self, tag, color):

        self.depth  = 3

        self.string1 = '<material name="' + str(tag) + '">'

        # self.string2 = '    <color rgba="0 0 1 1"/>'
        self.string2 = '    <color rgba="' + str(color[0]) + " " + str(color[1]) + " " + str(color[2]) + " " + str(color[3]) +'"/>'

        self.string3 = '</material>'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )
