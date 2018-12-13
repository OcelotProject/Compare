from numbers import Number
from numpy import isclose


_ = lambda x: isinstance(x, Number)

def similar(x, y):
    if _(x) and x == 0 and _(y) and y == 0:
        return True
    elif (_(x) and x == 0 and y is None) or (_(y) and y == 0 and x is None):
        return "missing"
    elif (_(x) and isclose(x, 0) and (y is None or y == 0)) or (_(y) and isclose(y, 0) and (x is None or x == 0)):
        return "roundoff"
    elif x is None or y is None:
        return False
    else:
        return isclose(x / (y or 1), 1., rtol=1e-04, atol=1e-06)


from .exchanges import compare_exchanges
from .indices import similarity_index, skipped_high_voltage_production_mixes
from .operators import missing_given, missing_model, in_both, calculate_similarities
from .utils import prepare_loaded_data, add_urls_if_needed
