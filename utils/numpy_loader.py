import json
import numpy as np

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, (np.floating, float)):
            return float(obj)
        if isinstance(obj, (np.int,np.int_)):
            return int(obj)
        if isinstance(obj, np.nan):
            return None
        return super(NumpyEncoder, self).default(obj)