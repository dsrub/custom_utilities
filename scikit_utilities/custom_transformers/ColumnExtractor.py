from sklearn.base import TransformerMixin, BaseEstimator, ClassifierMixin
import numpy as np
import pandas as pd

class ColumnExtractor(BaseEstimator, TransformerMixin):
  def __init__(self, column=0):
      """Extract a column from a pandas.DataFrame
      
      Use this transformer at the beginning of a
      pipeline to extract the column of interest
      from a data frame.
      """
      self.column = column

  def fit_transform(self, X, y=None, **kwargs):
      self.fit(X, y, **kwargs)
      return self.transform(X)

  def transform(self, X, **kwargs):
      return X[:,self.column]

  def fit(self, X, y=None, **kwargs):
      return self