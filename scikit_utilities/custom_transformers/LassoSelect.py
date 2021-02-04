from sklearn.base import TransformerMixin, BaseEstimator, ClassifierMixin
import numpy as np

class LassoSelect(BaseEstimator, TransformerMixin):
    """ Performs a feature selection by tuning L1 regularization to obtain exactly
    n_features (user-specified) with coefficients not equal to zero.  The tuning is
    performed with a modified binary search.
    
    Note that this experimental and is not gauranteed to converge, especially if the 
    number of features with non-zero coefficients obtained with L1 regularization is 
    not monotic with the regularization strength (this is required for proper 
    performance of the binary search algorithm within the fit method).


    Parameters
    ------------
    estimator : an instantiated scikit estimator which allows for L1 regularization
    n_features :  int 


    Author : Douglas Rubin

    """
    def __init__(self, estimator, n_features=5):
        self.estimator = estimator
        self.n_features = n_features

    def fit_transform(self, X, y, **kwargs):
        self.fit(X, y, **kwargs)
        return self.transform(X)
    
    def transform(self, X, **kwargs):
        
        if type(X) == np.ndarray:
            return X[:, self.non_zero_coefs]
        
        elif type(X) == pandas.core.frame.DataFrame:
            return X.iloc[:, self.non_zero_coefs]


    def fit(self, X, y, low=1e-8, high=1e8, max_iters = 100, **kwargs):
        
        self.non_zero_coefs = self._feature_selec_binary_search(X, y, low, high, max_iters)
        
        ## compute support
        self.support_ = [False]*X.shape[1]
        for ind in self.non_zero_coefs:
            self.support_[ind] = True
        
        self.support_ = np.array(self.support_)

        return self
    
   
    def _feature_selec_binary_search(self, X, y, low, high, max_iters):
        
        if low == 0:
            low = 1e-10
        
        iters = 0
        while low <= high and iters <= max_iters:
            iters += 1
            mid = (low + high)/2

            if 'C' in self.estimator.__dict__.keys():
                self.estimator.C = mid
            else:
                self.estimator.alpha = mid

            coefs = self.estimator.fit(X, y).coef_.flatten()
            num_non_zero = sum(coefs != 0)

            if num_non_zero == self.n_features:
                return np.where(coefs != 0)[0]

            elif num_non_zero > self.n_features:
                if 'C' in self.estimator.__dict__.keys():
                    high = mid
                else:
                    low = mid
            else:
                if 'C' in self.estimator.__dict__.keys():
                    low = mid
                else:
                    high = mid
        
        raise Exception('LassoSelect failed to converge upon features to select')