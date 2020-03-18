# A simple container class with parents and children used to construct the DAKOTA input file.
# Mulitple instances can be used to implement a tree which keeps track of the tiered structure 
# of the variables in the file. 

# Each line of the file is an instance of this class with the following member data:
# KEY       : The 'name' of the entry
# ATTRIBUTE : An attribute for lines of the form 'key = attribute' or 'key attribute'
# EQUALS    : Indicates whether the line is 'key = attribute' or simply 'key attribute'
# CHILDREN  : A list of child container classes beneath this one
# PARENT    : The parent class above this one

import numpy as np
from exceptions import *

class Container:

    def __init__(self,key,parent=None,attribute=None,equals=True):

        self.key       = key
        self.attribute = attribute
        self.equals    = equals
        self.parent    = parent

        # Initialise list of children to an empty list
        self.children  = []

        # Set as a child of the parent
        if parent is not None:
            parent.add_children( [self] )

    # Just adds existing objects to list of children of this object
    def add_children(self,children):
        
        if not ( isinstance( children, list ) or isinstance( children, Container ) ):
            raise ContainerError('Objects passed to add_children must be containers or lists of containers.')

        if not isinstance( children,list ):
            self.children.append(children)
        else:
            
            # Check every entry of list is a container
            type_arr = [ isinstance(x,Container) for x in children ]
            if not np.all(type_arr):
                 raise ContainerError('All elements of list passed to add_children must be containers.')

            self.children = self.children + children

    # Return the instance with a given key from beneath this one
    # This will not work reiably if there are multiple instances 
    # of the same key beneath the instance this is called from.
    def get(self,key):

        waiting = [self]

        while len(waiting) != 0:

            # Get current line from waiting list
            current = waiting.pop(-1)

            # Check if this is the desired instance
            if current.key == key:
                return current
            else:
                # Add children of current line to waiting list
                waiting = waiting + current.children

        return None

    # Add a new child beneath the object with name 'key' somewhere down the tree
    def add_child(self,key,child):

        if not isinstance( child, Container ):
            raise ContainerError('Objects passed to add_child must be containers.')

        instance = self.get(key)
        if instance is not None:
            child.parent = instance
            instance.children.append( child )
        else:
            raise ContainerError('Instance with key '+key+' does not exist.')

    # Find out how far down the tree this instance is
    def get_depth(self):

        current = self
        depth = 0

        while current.parent is not None:

            current = current.parent
            depth = depth + 1

        return depth

    # Return the attribute corresponding to a given key
    def get_attribute(self,key):

        instance = self.get(key)
        if instance is not None:
            return instance.attribute
        else:
            raise ContainerError('Instance with key '+key+' does not exist.')

    # Set attribute of an instance
    def set_attribute(self,key,attribute):

        instance = self.get(key)
        if instance is not None:
            instance.attribute = attribute
        else:
            raise ContainerError('Instance with key '+key+' does not exist.')

    def append_attribute(self,key,attribute):

        instance = self.get(key)
        if instance is None:
            raise ContainerError('Instance with key '+key+' does not exist.')

        # Check if attribute is already a list, if not make it one. 
        if not isinstance( instance.attribute,list ):
            instance.attribute = [ instance.attribute ]

        if not isinstance( attribute,list ):
            instance.attribute.append( attribute )
        else:
            instance.attribute += attribute

    # Write the current instances line to the DAKOTA input file
    def write_line(self,filehandle):

        # Don't write the top level dakota instance
        if self.parent is None:
            return

        depth = self.get_depth()

        line = ' '*(depth-1) + self.key
        if self.attribute is not None:

            if self.equals:
                line = line + ' = '
            else:
                line = line + ' '

            if isinstance( self.attribute, list ):
                line = line + " ".join( [ str(x) for x in self.attribute ] )
            else:
                line = line + str(self.attribute)

        line = line + '\n'

        filehandle.write(str(line))

    # Loop over all children and write out lines
    def write_all(self,filehandle):

        waiting = [self]

        while len(waiting) != 0:

            # Get current line from waiting list
            current = waiting.pop(-1)

            # Write current line
            current.write_line(filehandle)

            # Add children of current line to waiting list
            waiting = waiting + current.children
