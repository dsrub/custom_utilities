from sklearn.base import TransformerMixin, BaseEstimator, ClassifierMixin
import numpy as np

class MultiColLabelEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, columns=None):

        # if columns=None, then fit/transform all the columns.  otherwise if a list is specified
        ## just fit those columns
        self.cols = columns

    def fit_transform(self, X, y=None, **kwargs):
        self.fit(X, y, **kwargs)
        return self.transform(X)

    def transform(self, X, **kwargs):
      ### perform mapping on each column
        f = np.vectorize(str)
        Z = f(np.copy(X))
        for col, d in zip(self.cols, self.dictionaries_):
            Z[:, col] =np.vectorize(d.get)(Z[:, col])

        return Z

    def fit(self, X, y=None, **kwargs):
        ## compute a dictionary mapping for each column to transform

        ## convert all elements of matrix to same type
        f = np.vectorize(str)  # or use a different name if you want to keep the original f
        X = f(X) 
        
        if self.cols is None:
            self.cols = np.arange(0,X.shape[1])      
      
        self.dictionaries_=[]
        for col in self.cols:
            uniques=np.unique(X[:,col])
            d = {x:y for x, y in zip(uniques, range(len(uniques)))}

            self.dictionaries_.append(d)


        return self