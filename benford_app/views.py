from pyramid.view import view_config
from pyramid.response import Response
import pandas as pd
import numpy as np
import io
import json
from scipy import stats


def get_pvalue(df):
    first_digits = pd.Series([int(str(x)[0]) for x in df.iloc[:, 0].values if str(x)[0].isdigit()])
    freq_count = np.zeros(9)
    for i in range(1, 10):
        freq_count[i-1] = np.log10(1 + 1/i) * len(first_digits)
    observed_count = [len(first_digits[first_digits == i]) for i in range(1, 10)]
    chi_squared = np.sum((observed_count - freq_count)**2/freq_count)
    p_value = 1 - stats.chi2.cdf(chi_squared, 8)
    return p_value

@view_config(route_name='benford', request_method='POST')
def benford(request):
    if 'file' not in request.POST:
        return Response('No file was uploaded.', status=400)
    file = request.POST.get('file').file
    df = pd.read_csv(io.StringIO(file.read().decode('utf-8')))
    p_value = get_pvalue(df)
    if p_value > 0.05:
        result = {"follows": True, 'P_value': p_value}
    else:
        result = {"follows": False, 'P_value': p_value}
    return Response(json.dumps(result).encode('utf-8'), content_type='application/json')


@view_config(route_name='home')
def home(request):
    return Response('Welcome to Benford\'s Law app we have \\benford endpoint')
