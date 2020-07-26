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
        print(params)
        return self.encoder.set_params(**params)

# Utility function for evaluation
def eval_mod(model, X_test, y_test):
    import numpy as np
    from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
    
    y_pred = model.predict(X_test)
    
    print('RMSE:', np.sqrt(mean_squared_error(y_test, y_pred)))
    print('MAE:', mean_absolute_error(y_test, y_pred))
    print('R^2:', r2_score(y_test, y_pred))

# Evaluate encoders
def eval_encoders(model, X_train, y_train):
    from sklearn.preprocessing import StandardScaler
    from sklearn.compose import ColumnTransformer
    
    encoders = ['CatBoostEncoder', 'GLMMEncoder', 'JamesSteinEncoder', 
            'LeaveOneOutEncoder', 'MEstimateEncoder', 'TargetEncoder', 
            'BinaryEncoder', 'HashingEncoder', 'OrdinalEncoder']
    
    num_columns = ['Review Date', 'Cocoa Percent']
    
    num_enc = ColumnTransformer(
    transformers=[
        ('num', StandardScaler(), num_columns)],
    remainder='passthrough')
    
    scores = []
    for enc in encoders:
        pipeline = Pipeline([('cat_enc', CatEncoder(enc)), 
                             ('scaler', num_enc), 
                             ('mod', model)])
        pipeline.fit(X_train, y_train)
        y_pred = pipeline.predict(X_test)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        scores.append(rmse)
    
    return pd.Series(scores, index=encoders).sort_values()