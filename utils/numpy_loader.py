import json
import numpy as np

from django.http import HttpResponse, JsonResponse

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        print("EEEE")
        if np.isscalar(obj):  # Check if it's a numpy scalar
            obj = obj.item()  # Convert to native Python type
        if isinstance(obj, float) and np.isnan(obj):
            return None
        if isinstance(obj, (np.floating, float)):
            return float(obj)
        if isinstance(obj, (np.integer, int)):
            return int(obj)
        else:
            return super(NumpyEncoder, self).default(obj)


def convert_np_values(data:dict):
    result = json.dumps(data, cls=NumpyEncoder).replace("NaN", "null")
    return  json.loads(result)
