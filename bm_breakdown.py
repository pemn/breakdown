#!python
# create data pivot tables from a database
# input: bmf (vulcan block model), isis (vulcan database) or  csv (ascii)
# condition: optional expression to filter. syntax is vulcan or python (csv,isis)
# variables: variables to generate the pivot table in the breakdown format
# output: optional files to write the result, csv and/or xlsx
'''
usage: $0 input*bmf,csv,isis condition variables#variable:input#type=breakdown,count,sum,mean,min,max,var,std,sem,q1,q2,q3#weight:input output*csv,xlsx
'''
import sys
import pandas as pd
import numpy as np

from _gui import usage_gui, pd_get_dataframe, table_field, commalist

# magic character that will be the label separator
_LABEL = '='

def bm_breakdown(input_path, condition, vl_s):
  ''' 
  File entry point for the breakdown process
  Input: path to input file, condition string, variable list string
  Output: dataframe with result
  '''

  vl_a = commalist().parse(vl_s)
  print("# bm_breakdown", input_path)
  if input_path.lower().endswith('.isis'):
    idf = pd_get_dataframe(input_path, condition, table_field(vl_a[0][0], True))
    vl_a = table_field(vl_a)
  else:
    idf = pd_get_dataframe(input_path, condition, [_[0].split(_LABEL)[0] for _ in vl_a])

  return pd_breakdown(idf, vl_a)

def pd_breakdown(idf, vl_a):
  '''
  Main worker function for the breakdown process
  Input: dataframe with input data, 2d list of breakdown template
  Output: dataframe with result
  '''
  r = []

  vl_b = []
  vl_v = []

  col_b = []
  col_v = []

  for v in vl_a:
    # create a copy of the row to avoid modifing the input
    v = list(v)
    name = v[0]
    # handle alternative column names. Ex.: volume:total_volume
    if len(name) > name.find(_LABEL) > 0:
      v[0], name = name.split(_LABEL)

    if len(v) == 1 or v[1] == 'breakdown' or len(v[1]) == 0:
      vl_b.append(v[0])
      col_b.append(name)
    else:
      vl_v.append(list(v))
      col_v.append([name,v[1]])

  if len(vl_v) == 0 and len(vl_b) > 0:
    vl_v = [[_,"text","-"] for _ in vl_b]
    col_v = [[_,"text"] for _ in col_b]

  # the breakdown columns will become a multiindex instead of actual data on the output
  r_row = None
  if vl_b:
    r_row = []
    for gp,df in idf.groupby(vl_b):
      if not isinstance(gp, tuple):
        gp = [gp]
      r_row.append(gp)
      r.append(pd_breakdown_fn(df, vl_v))
    r_row = pd.MultiIndex.from_arrays(list(zip(*r_row)), names=col_b)
  else:
    r.append(pd_breakdown_fn(idf, vl_v))
  
  return(pd.DataFrame(r, index=r_row, columns=pd.MultiIndex.from_arrays(list(zip(*col_v)))))

def weighted_quantiles(a, q=[0.25], w=None):
    """
    Calculates percentiles associated with a (possibly weighted) array

    Parameters
    ----------
    a : array-like
        The input array from which to calculate percents
    q : array-like
        The percentiles to calculate (0.0 - 100.0)
    w : array-like, optional
        The weights to assign to values of a.  Equal weighting if None
        is specified

    Returns
    -------
    values : np.array
        The values associated with the specified percentiles.  
    """
    # Standardize and sort based on values in a
    q = np.array(q)
    if w is None:
        w = np.ones(a.size)
    vn = ~(np.isnan(a) | np.isnan(w))
    # early exit for fully masked data
    if not vn.any():
      return [None]
    a = a[vn]
    w = w[vn]
    idx = np.argsort(a)
    a_sort = a[idx]
    w_sort = w[idx]

    # Get the cumulative sum of weights
    ecdf = np.cumsum(w_sort)

    # Find the percentile index positions associated with the percentiles
    #p = q * (w.sum() - 1)
    p = q * (np.nansum(w) - 1)

    # Find the bounding indices (both low and high)
    idx_low = np.searchsorted(ecdf, p, side='right')
    idx_high = np.searchsorted(ecdf, p + 1, side='right')
    idx_high[idx_high > ecdf.size - 1] = ecdf.size - 1

    # Calculate the weights 
    weights_high = p - np.floor(p)
    weights_low = 1.0 - weights_high

    # Extract the low/high indexes and multiply by the corresponding weights
    x1 = np.take(a_sort, idx_low) * weights_low
    x2 = np.take(a_sort, idx_high) * weights_high

    # Return the average
    return np.add(x1, x2)

def pd_breakdown_fn(df, vl):
  '''
  Custom aggregation function to allow weighted mean, sum and quantiles
  If weight is not needed, calls standard pandas or numpy functions
  Text operation: use any text in the weight field as output
  '''
  r = []
  for a in vl:
    # early out of blank rows
    if len(a) == 0:
      continue
    name = a[0]
    mode = ""
    if len(a) > 1:
      mode = a[1]
    wt = []
    for w in a[2:]:
      if len(w) == 0:
        # trap blank values
        pass
      elif ',' in w:
        # handle the case where any weight is still comma separated
        wt.extend([_ for _ in w.split(',') if _ in df])
      elif w in df:
        wt.append(w)

    # handle the case where any weight is still comma separated
    v = None
    if mode == "text":
      # constant value, taken as raw text from the weight field
      if wt:
        v = ' '.join(wt)
      else:
        v = name
    elif name not in df:
      # trap special case: unknown var, will keep the default value of None
      pass
    elif wt and mode == "sum":
      # weighted sum
      v = np.nansum(np.prod([df[_].values for _ in [name] + wt], 0))
    elif wt and mode == "mean":
      # boolean indexing of non-nan values
      bi = ~ np.isnan(df[name].values)
      ws = np.prod([df[_].values[bi] for _ in wt], 0)
      if np.sum(ws) != 0:
        # weighted mean
        v = np.average(df[name].values[bi], None, ws)
    elif wt and mode in ["q1", "q2", "q3"]:
      q = (["q1", "q2", "q3"].index(mode) + 1) * 0.25
      v = weighted_quantiles(df[name].values, [q], np.prod([df[_].values for _ in wt], 0))[0]
    elif hasattr(pd.Series, mode):
      fn = eval('pd.Series.' + mode)
      v = fn(df[name])
    elif mode in ["q1", "q2", "q3"]:
      q = (["q1", "q2", "q3"].index(mode) + 1) * 0.25
      v = df[name].quantile(q)

    r.append(v)
  return(r)

def main(*args):
  odf = bm_breakdown(args[0], args[1], args[2])
  output = args[3]

  # screen
  if(odf.size > 0):
    print(odf.to_string(na_rep = ""))
    # Excel sheet
    if output.lower().endswith('.xlsx'):
      odf.to_excel(output)
    elif len(output) > 0:
      odf.reset_index(inplace=True)
      odf.columns = odf.columns.droplevel(1)
      odf.to_csv(output, index=False)
  else:
    print(output,"empty")

if __name__=="__main__" and sys.argv[0].endswith('bm_breakdown.py'):
  usage_gui(__doc__)
