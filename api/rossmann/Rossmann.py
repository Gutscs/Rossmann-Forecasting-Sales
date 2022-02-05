import pandas as pd
import numpy as np

import pickle
import inflection
import math
import datetime
import os

class Rossmann( object ):

    def __init__( self ):
        self.home_path = os.path.abspath('')
        self.competition_distance_scaler   = pickle.load( open( os.path.join(self.home_path, 'parameter/competition_distance_scaler.pkl'), 'rb' ) )                
        self.competition_time_month_scaler = pickle.load( open( os.path.join(self.home_path, 'parameter/competition_time_month_scaler.pkl'), 'rb' ) )
        self.promo_time_week_scaler        = pickle.load( open( os.path.join(self.home_path, 'parameter/promo_time_week_scaler.pkl'), 'rb' ) )
        self.year_scaler                   = pickle.load( open( os.path.join(self.home_path, 'parameter/year_scaler.pkl'), 'rb' ) )
        self.store_type_scaler             = pickle.load( open( os.path.join(self.home_path, 'parameter/store_type_scaler.pkl'), 'rb' ) )


    def data_cleaning( self, df1 ):
        ## 2.1. Rename Columns
        cols_old = ['Store', 'DayOfWeek', 'Date', 'Open', 'Promo', 'StateHoliday', 'SchoolHoliday', 'StoreType', 
                    'Assortment', 'CompetitionDistance', 'CompetitionOpenSinceMonth', 'CompetitionOpenSinceYear', 
                    'Promo2', 'Promo2SinceWeek', 'Promo2SinceYear', 'PromoInterval']

        snake_case = lambda x: inflection.underscore(x)
        cols_new = list( map(snake_case, cols_old) )

        # rename columns
        df1.columns = cols_new
    
        ## 2.3. Data Types
        # changing date to datetime type
        df1['date'] = pd.to_datetime(df1['date'])
        
        ## 2.5. Fillout NA
        # competition_distance  
        df1['competition_distance'].fillna(200000, inplace = True)
        
        # competition_open_since_year and competition_open_since_month
        df1['competition_open_since_year'].fillna( df1['date'].dt.year, inplace = True)
        df1['competition_open_since_month'].fillna( df1['date'].dt.month, inplace = True)
        
        # promo2_since_year and promo2_since_week
        df1['promo2_since_year'].fillna(df1['date'].dt.year, inplace = True)
        df1['promo2_since_week'].fillna(df1['date'].dt.isocalendar().week, inplace = True)
        
        # promo_interval
        df1['promo_interval'].fillna(0, inplace = True)

        # month map to help the operation
        month_map = {1 : 'Jan', 2 : 'Fev', 3 : 'Mar', 4 : 'Apr', 5 : 'May', 6 : 'Jun', 7 : 'Jul', 8 : 'Aug', 9 : 'Sept', 
                    10 : 'Oct', 11 : 'Nov', 12 : 'Dec'}

        df1['month_map'] = df1['date'].dt.month.map( month_map )
        df1['is_promo'] = df1[['promo_interval', 'month_map']].apply(lambda x: 0 if x['promo_interval'] == 0 else (1 if x['month_map'] in x['promo_interval'].split( "," ) else 0), axis = 1)
        
        ## 2.6. Change Data Types
        # competition data to int
        df1['competition_open_since_month'] = df1['competition_open_since_month'].astype( int )
        df1['competition_open_since_year'] = df1['competition_open_since_year'].astype( int )

        # promo data to int
        df1['promo2_since_week'] = df1['promo2_since_week'].astype( int )
        df1['promo2_since_year'] = df1['promo2_since_year'].astype( int )

        return df1
    

    def feature_engineering( self, df2 ): 
        # year
        df2['year'] = df2['date'].dt.year

        # month 
        df2['month'] = df2['date'].dt.month

        # day
        df2['day'] = df2['date'].dt.day

        # week of year
        df2['week_of_year'] = df2['date'].dt.isocalendar().week

        # year week
        df2['year_week'] = df2['date'].dt.strftime( '%Y-%W' )
        
        # competition since
        df2['competition_since'] = df2.apply(lambda x: 
            datetime.datetime(year = x['competition_open_since_year'], month = x['competition_open_since_month'], day = 1), axis = 1)

        # competition time month
        df2['competition_time_month'] = ( (df2['date'] - df2['competition_since']) / 30 ).apply( lambda x: x.days ).astype( int )

        # promo since
        df2['promo_since'] = df2['promo2_since_year'].astype( str ) + '-' + df2['promo2_since_week'].astype( str )
        df2['promo_since'] = df2['promo_since'].apply(lambda x: datetime.datetime.strptime(x + '-1', '%Y-%W-%w') - datetime.timedelta(days = 7))

        # promo time week
        df2['promo_time_week'] = ((df2['date'] - df2['promo_since'])/7).apply(lambda x: x.days).astype(int)

        # assortment
        assortment = {'a' : 'basic', 'b' : 'extra', 'c' : 'extended'}
        df2['assortment'] = df2['assortment'].map(assortment)

        # state holiday       
        state_holiday = {'a' : 'public_holiday', 'b' : 'easter_holiday', 'c' : 'christmas', '0' : 'regular_day'}
        df2['state_holiday'] = df2['state_holiday'].map(state_holiday)

        ## 4.1. Rows Filtering
        df2 = df2[ df2["open"] != 0 ]
        
        ## 4.2. Columns Selection
        df2 = df2.drop( columns = ['open', 'promo_interval', 'month_map'], axis = 1)

        return df2


    def data_preparation( self, df5 ):
        ## 6.2. Rescaling

        # Applying Robust Scaler to competition distance
        df5['competition_distance'] = self.competition_distance_scaler.transform( df5[['competition_distance']].values )

        # Applying Robust Scaler to competition time month
        df5['competition_time_month'] =  self.competition_time_month_scaler.fit_transform( df5[['competition_time_month']].values )

        # Applying Min-Max Scaler to promo time week
        df5['promo_time_week'] =  self.promo_time_week_scaler.fit_transform( df5[['promo_time_week']].values )

        # Applying Min-Max Scaler to year
        df5['year'] = self.year_scaler.fit_transform( df5[['year']].values )

        ### 6.3.1. Enconding
        # Applying One Hot Enconding to state_holiday
        df5 = pd.get_dummies(df5, prefix = ['state_holiday'], columns = ['state_holiday'])

        # Applyng Label Enconding to store_type
        df5['store_type'] = self.store_type_scaler.fit_transform( df5['store_type'] )

        # Applyng Ordinal Enconding to assortment
        assortment_dict = {'basic': 1, 'extra': 2, 'extended': 3}
        df5['assortment'] = df5['assortment'].map( assortment_dict )

        ### 6.3.3 Nature Transformation
        # month
        df5['month_sin'] = df5['month'].apply( lambda x: np.sin( x * ( 2. * np.pi/12 ) ) )
        df5['month_cos'] = df5['month'].apply( lambda x: np.cos( x * ( 2. * np.pi/12 ) ) )

        # day
        df5['day_sin'] = df5['day'].apply( lambda x: np.sin( x * ( 2. * np.pi/30 ) ) )
        df5['day_cos'] = df5['day'].apply( lambda x: np.cos( x * ( 2. * np.pi/30 ) ) )

        # day of week
        df5['day_of_week_sin'] = df5['day_of_week'].apply( lambda x: np.sin( x * ( 2. * np.pi/7 ) ) )
        df5['day_of_week_cos'] = df5['day_of_week'].apply( lambda x: np.cos( x * ( 2. * np.pi/7 ) ) )

        # week of year
        df5['week_of_year_sin'] = df5['week_of_year'].apply( lambda x: np.sin( x * ( 2. * np.pi/52 ) ) )
        df5['week_of_year_cos'] = df5['week_of_year'].apply( lambda x: np.cos( x * ( 2. * np.pi/52 ) ) )
        
        cols_selected = [ 'store', 'promo', 'store_type', 'assortment','competition_distance','competition_open_since_month',
            'competition_open_since_year','promo2','promo2_since_week','promo2_since_year','competition_time_month','promo_time_week',
            'month_cos','month_sin', 'day_sin','day_cos','day_of_week_sin','day_of_week_cos','week_of_year_cos','week_of_year_sin'  
        ]

        return df5[ cols_selected ]


    def get_prediction( self, model, original_data, test_data ):
        # prediction 
        pred = model.predict( test_data )

        # join pred into the original data
        original_data['prediction'] = np.expm1( pred )

        return original_data.to_json( orient='records', date_format='iso' )