# define Python user-defined exceptions

class Error(Exception):
    """Base class for other exceptions in this module"""
    pass

class ContainerError(Error):
    """Raised when an incorrect action is taken on a container or a container does not exist."""
    
    def __init__( self, message ):

        self.message = message

class FileConsistencyError(Error):
    """
    Raised when inconsistent data is present in the DakotaFile class.
    This could be that both sampling and parameter scan variables are present
    or that needed run configuration data is missing.
    """

    def __init__( self, message ):

        self.message = message

class WriteFileError(Error):
    """Raised when no data is available to write to a Dakota file."""

    def __init__( self, message ):

        self.message = message

class DakotaResultsError(Error):
    """Raised when there is an error filling the DAKOTA results object"""

    def __init__( self, message ):

        self.message = message

class DatasetError(Error):
    """
    Raised when dakota_class:add_variable is not passed an xarray Dataset
    or Dataset object contains incorrect information."""

    def __init__( self, message ):
        
        self. message = message

class VariableError(Error):
    """
    Raised by dakota_file when one tries to add an invalid variable to a file."""

    def __init__( self, message ):
        
        self. message = message
