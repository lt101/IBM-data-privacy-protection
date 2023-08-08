from src.masking.binning import Binning
from src.masking.dateTime import DateTime
from src.masking.generalization import Generalization
from src.masking.prefix import Prefix
from src.masking.shifting import Shifting

class MaskingFactory:
    def create_mechanism(self, name:str):
        """
         @brief Create mechanism based on name. This is used to create mechanisms that need to be added to the simulation
         @param name Name of the mechanism to create
         @return A subclass of : class : ` ~manticore. core. mechanism. Generalization ` or
        """
        # This function is used to set the user defined property of the object.
        if name == 'Generalization':
            mech = Generalization()
        elif name == 'Prefix preservation':
            mech = Prefix()
        elif name == 'Date or time':
            mech = DateTime()
        elif name == 'Binning':
            mech = Binning()
        elif name == 'Shifting':
            mech = Shifting()
        return mech