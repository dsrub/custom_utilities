from sklearn.base import TransformerMixin, BaseEstimator, ClassifierMixin
import numpy as np
import pandas as pd



class InGroupImputation(BaseEstimator, TransformerMixin):
    """ Perform in-group imputation for feature preparation.

    Parameters
    ------------
    grouping_cols : list
    A list of the columns which define the groups by which you want to group by.
    Must be a list of integer values specifying the column locations.  Note this
    can be a single value (if grouping by a single column), or multiple values
    (if grouping by several columns).

    impute_col : int
    The column for desired imputation

    method : str
    The imputation method.  Can be "mean", "median", "mode".  The default is mean.

    Author : Douglas Rubin

    """
    def __init__(self, grouping_cols, impute_col, method = 'mean'):
        self.grouping_cols = grouping_cols
        self.impute_col = impute_col
        self.method = method

    def fit_transform(self, X, y=None, **kwargs):

        self.fit(X, y, **kwargs)
        return self.transform(X)

    def transform(self, X, **kwargs):


        ddd = pd.DataFrame(X, columns = self.col_names)

        ddd['new_code_column'] = ""
        for col in self.grouping_cols:
            ddd['new_code_column'] += ddd[col].astype(str)

        for i in range(self.res.shape[0]):
            ddd.loc[(ddd.new_code_column == self.res['merged'][i]) & ddd[self.impute_col].isnull(), self.impute_col] = self.res['new_col'][i]
            
        del ddd['new_code_column']
        
        return ddd.values

    def fit(self, X, y=None, **kwargs):
        self.grouping_cols = [str(y) for y in self.grouping_cols]
        self.impute_col = str(self.impute_col)

        self.col_names = [str(x) for x in range(X.shape[1])]
        dd = pd.DataFrame(X, columns = self.col_names)
        dd[self.impute_col]=pd.to_numeric(dd[self.impute_col], errors='coerce')

        if self.method == 'mean':
            res = dd.groupby(self.grouping_cols)[self.impute_col].mean()

        if self.method == 'median':
            res = dd.groupby(self.grouping_cols)[self.impute_col].median()
        
        res = res.reset_index(name='new_col')

        res['merged'] = ""
        for col in self.grouping_cols:
            res['merged'] += res[col].astype(str)

        self.res = res


        return self

