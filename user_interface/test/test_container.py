from container import Container
from exceptions import *
import os
import unittest

class TestContainer(unittest.TestCase):

    def test_make_container(self):
        
        # Declare a container
        top = Container('top',None)
        
    def test_give_child_attribute(self):

        top = Container('top')
        
        # Give it a child with a simple attribute
        child = Container('child',top,attribute=0)
        
    def test_get_depth(self):

        top   = Container('top')
        child = Container('child',top,attribute=0)
        
        # Check child is at level 1
        self.assertEqual(child.get_depth(), 1)

    def test_get_a_container_from_tree(self):
            
        top   = Container('top')
        child = Container('child',top,attribute=0)
        
        # Return child from top
        self.assertEqual(top.get('child'), child)

    def test_get_attribute_from_lower_in_tree(self):
        
        top   = Container('top')
        child = Container('child',top,attribute=0)
        
        # Get attribute of child from top
        self.assertEqual( top.get_attribute('child'), 0 )

    def test_set_attribute_lower_in_tree(self):

        top   = Container('top')
        child = Container('child',top,attribute=0)
        
        top.set_attribute('child',1)
        
        # Get attribute of child from top
        self.assertEqual( top.get_attribute('child'), 1 )

    def test_append_attribute_lower_in_tree(self):

        top   = Container('top')
        child = Container('child',top,attribute=[0])
        
        top.append_attribute('child',1)
        
        # Get attribute of child from top
        self.assertEqual( top.get_attribute('child'), [0,1] )

    def test_add_child_lower_in_tree(self):

        top   = Container('top')
        child = Container('child',top,attribute=[0])
        
        child2 = Container('child2',attribute=1)
        top.add_child('child',child2)
    
        self.assertEqual( child2.get_depth(), 2 )
        self.assertEqual( child2.parent, child )

    def test_append_attribute_not_list(self):

        top   = Container('top',attribute=1)
        top.append_attribute('top',5)

    def test_write_all(self):

        top   = Container('top')
        child = Container('child',top,attribute=[0])
        
        child2 = Container('child2',attribute=1)
        top.add_child('child',child2)
        
        fhandle = open('container_test.dat','w')
        top.write_all(fhandle)
        fhandle.close()
        
        fhandle = open('container_test.dat','r')
        line1 = fhandle.readline()
        line1 = line1.strip().split('=')
        
        self.assertEqual( line1[0].strip(), 'child' )
        self.assertEqual( line1[1].strip(), '0' )
        
        line2 = fhandle.readline()
        line2 = line2.strip().split('=')
        
        self.assertEqual( line2[0].strip(), 'child2' )
        self.assertEqual( line2[1].strip(), '1' )
        
        fhandle.close()
        os.remove('container_test.dat')

    # Create a structure with many layers
    def test_make_a_tree(self):

        top    = Container('top')
        child1 = Container('child1',attribute=1)
        child2 = Container('child2',attribute=2)
        child3 = Container('child3',attribute=3)
        child4 = Container('child4',attribute=4)
        child5 = Container('child5',attribute=5)
        
        top.add_child('top',child1)
        top.add_child('child1',child2)
        top.add_child('child2',child3)
        top.add_child('child3',child4)
        top.add_child('child4',child5)
        
        self.assertEqual( child5.get_depth(), 5 )
        self.assertEqual( child4.parent, child3 )
        self.assertEqual( top.get_attribute('child3'), 3 )
        self.assertEqual( top.get('child4'), child4 )

#######################################
# Failure tests
#######################################

    # Add a child beneath a container that does not exist
    def test_no_child_error(self):

        top   = Container('top')
        child = Container('child',attribute=1)
    
        with self.assertRaises(ContainerError):
            top.add_child('none',child)

    # Try to add a child which isn't a container
    def test_add_child_not_container(self):

        top   = Container('top')
        child = Container('child',attribute=1)
    
        with self.assertRaises(ContainerError):
            top.add_child('child',5)

    # Try to add_children where argument is not a container
    def test_add_children_not_container(self):

        top   = Container('top')
    
        with self.assertRaises(ContainerError):
            top.add_children(5)

    # Try to add_children where argument is a list with an entry not a container
    def test_add_children_list_not_container(self):

        top   = Container('top')
        child = Container('child',attribute=1)
        
        children = [ child, 5 ]
    
        with self.assertRaises(ContainerError):
            top.add_children(children)

    def test_get_attribute_failure(self):

        top   = Container('top')
    
        with self.assertRaises(ContainerError):
            top.get_attribute('none')

    def test_set_attribute_failure(self):

        top   = Container('top')
    
        with self.assertRaises(ContainerError):
            top.set_attribute('none',5)

    def test_append_attribute_missing_child_failure(self):

        top   = Container('top')
    
        with self.assertRaises(ContainerError):
            top.append_attribute('none',5)
