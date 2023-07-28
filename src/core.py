import numpy as np

class Spectrum:
    def __init__(self, name: str, nm: np.ndarray, br: np.ndarray):
        """
        Constructor of the class to work with single, continuous spectrum.
        
        Args:
        - name (str): human-readable identification. May include source (separated by "|")
        and additional info (separated by ":")
        - nm (np.array): list of wavelengths in nanometers
        - br (np.array): same-size list of linear physical property, representing "brightness"
        """
        self.name = name
        self.br = br
        self.nm = nm
        
    def convolve_with(self, filter):
        """
        Method that applies convolution to the spectrum with filter.
        """
        pass
    
    def color(self):
        """
        Method that determines the color of the spectrum.
        """
        pass