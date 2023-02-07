from pyrosim.commonFunctions import Save_Whitespace

class GEOMETRY_SDF: 

    def __init__(self,size, objectType):

        self.depth   = 4

        self.string1 = '<geometry>'

        #sizeString = str(size[0]) + " " + str(size[1]) + " " + str(size[2])

        #self.string2 = '   <box>'

        #self.string3 = '      <size>' + sizeString + '</size>'

        #self.string4 = '   </box>'
        
        
        if objectType == 'box':
            #print(objectType)
            
            sizeString = str(size[0]) + " " + str(size[1]) + " " + str(size[2])
            
            self.string2 = ' <box>'
            
            self.string3 = ' <size>' + sizeString + '</size>'
            
            self.string4 = ' </box>'
        
        elif objectType== 'sphere':
            
            sizeString = str(size[0])
            
            self.string2 = ' <sphere>'
            
            self.string3 = ' <radius>' + sizeString + '</radius>'
            
            self.string4 = ' </sphere>'
            
            
        else :
                sizeString = str(size[0]) + " " + str(size[1]) #+ " " + str(size[2]) 
                self.string2 = ' <cylinder>'
                
                self.string3 =  ' <size>' + sizeString + '</size>'
                
                self.string4 = ' <cylinder>'
    
        self.string5 = '</geometry>'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string4 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string5 + '\n' )
        