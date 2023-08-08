"""reference: https://diffprivlib.readthedocs.io/en/latest/index.html"""
from src.diffPrivacy.geometricTruncated import GeometricTruncated
from src.diffPrivacy.exponential import Exponential
from src.diffPrivacy.gaussian import Gaussian
from src.diffPrivacy.laplace import Laplace
from src.diffPrivacy.snapping import Snapping
from src.diffPrivacy.staircase import Staircase
from src.diffPrivacy.uniform import Uniform

class DPMechFactory:

    def create_mechanism(self, name:str):
        """
         @brief Create and return a mechanism based on the name. This is used to create mechanisms that are specific to the simulation
         @param name Name of the mechanism to create
         @return An instance of the mechanism that is defined by the name passed in ( or None if none was defined
        """
        # This function is used to convert the name of the feature to a function.
        if name == 'Geometric truncated':
            mech = GeometricTruncated()
        elif name == 'Exponential':
            mech = Exponential()
        elif name == 'Gaussian':
            mech = Gaussian()
        elif name == 'Laplace':
            mech = Laplace()
        elif name == 'Snapping':
            mech = Snapping()
        elif name == 'Staircase':
            mech = Staircase()
        elif name == 'Uniform':
            mech = Uniform()
        return mech
