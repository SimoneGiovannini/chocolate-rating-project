from sklearn.base import TransformerMixin
from sklearn.pipeline import Pipeline

class CatEncoder(TransformerMixin):
    def __init__(self, enc_name='MEstimateEncoder', **kwargs):
        exec('from category_encoders import %s' % enc_name)
        exec('self.encoder = %s(**kwargs)' % enc_name)

    def fit(self, X, y=None):
        return self.encoder.fit(X, y)

    def transform(self, X, y=None):
        return self.encoder.transform(X, y)

    def set_params(self, **params):
        return self.encoder.set_params(**params)

    def get_params(self, **params):
        return self.encoder.get_params(**params)

def eval_mod(model, X_test, y_test):
    # Evaluate RMSE, MAE, R2 on test set
    import numpy as np
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

    y_pred = model.predict(X_test)

    print('RMSE:', np.sqrt(mean_squared_error(y_test, y_pred)))
    print('MAE:', mean_absolute_error(y_test, y_pred))
    print('R^2:', r2_score(y_test, y_pred))

def clip_model(model):
    # Force model predictions to be between 1 and 4
    class ClippedModel(model):
        def predict(self, X):
            pred = super().predict(X)
            pred = np.maximum(pred, 1.0)
            pred = np.minimum(pred, 4.0)
            return pred

    return ClippedModel
