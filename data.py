import pandas as pd
import numpy as np
from config import engine
from datetime import datetime

year = datetime.now().strftime('%Y')

query_total_learners = """SELECT public.schools.name AS school_name, COUNT(public.learners_prod.id) AS total_girl_learners
FROM public.schools
JOIN public.learners_prod ON public.schools.id = public.learners_prod.school_id
WHERE date_part('YEAR', public.learners_prod.created_at) = '{}'
OR public.learners_prod.first_dose_at IS NULL 
OR public.learners_prod.second_dose_at IS NULL
GROUP BY public.schools.name;""".format(int(year))

district_query = """SELECT public.schools.name as school_name, public.schools.emis_number, public.subdistricts.name as subdistrict_name, public.districts.name as district_name, public.districts.province
FROM public.schools 
JOIN public.subdistricts ON public.schools.subdistrict = public.subdistricts.id
JOIN public.districts ON public.subdistricts.district = public.districts.id;"""

query = """SELECT public.logs_prod.* , public.schools.name as school_name 
FROM public.logs_prod
JOIN public.schools ON public.logs_prod.school_id = public.schools.id;"""

query_add = """SELECT public.additional_prod.*, public.schools.name as school_name 
FROM public.additional_prod
JOIN public.schools ON public.additional_prod.school_id = public.schools.id;"""


class Data:
   def __init__(self, start_date, end_date) -> None:
      self.df_learners = pd.read_sql_query(query_total_learners, engine)
      self.df_districts = pd.read_sql_query(district_query, engine)
      self.df_add = pd.read_sql_query(query_add, engine)
      self.df_main = pd.merge(self.df_districts, self.df_learners, on='school_name', how='left')
      self.df_main['total_girl_learners'] = self.df_main['total_girl_learners'].fillna(0)
      self.df_main['total_girl_learners'] = self.df_main['total_girl_learners'].astype('int')
      self.df_main['emis_number'] = self.df_main['emis_number'].astype('int')
      self.df_main['emis_number'] = self.df_main['emis_number'].astype('str')
      self.df_logs = pd.read_sql_query(query, engine)
      self.df_logs.set_index('created_at', inplace=True)
      self.df_add.set_index('created_at', inplace=True)
      self.df_logs = self.df_logs.loc[start_date: end_date, :]
      self.df_add = self.df_add.loc[start_date: end_date, :]
      self.format_data()



   def add_consent(self):
      now = pd.Timestamp('now')
      self.df_logs['dob'] = pd.to_datetime(self.df_logs['dob'], format='%Y-%m-%d')    # 1
      self.df_logs['dob'] = self.df_logs['dob'].where(self.df_logs['dob'] < now, self.df_logs['dob'] -  np.timedelta64(100, 'Y'))   # 2
      self.df_logs['age'] = (now - self.df_logs['dob']).astype('<m8[Y]')
      df_consent = self.df_logs[(self.df_logs.age >= 9) & (self.df_logs.type.eq(1))]. \
                  groupby('school_name')['learner_id'].nunique().reset_index()
      df_consent.rename(columns={'learner_id': 'consent >=9'}, inplace=True)
      self.df_main = pd.merge(self.df_main, df_consent, on='school_name', how='left')
      self.df_main['consent >=9'] = self.df_main['consent >=9'].fillna(0)
      self.df_main['consent >=9'] = self.df_main['consent >=9'].astype('int')

   def add_first_dose(self):
      df_first_dose = self.df_logs[self.df_logs.type.eq(2)]. \
                  groupby('school_name')['learner_id'].nunique().reset_index()
      df_first_dose.rename(columns={'learner_id': 'first_dose'}, inplace=True)
      self.df_main = pd.merge(self.df_main, df_first_dose, on='school_name', how='left')
      self.df_main['first_dose'] = self.df_main['first_dose'].fillna(0)
      self.df_main['first_dose'] = self.df_main['first_dose'].astype('int')

   def add_second_dose(self):
      df_second_dose = self.df_logs[self.df_logs.type.eq(3)]. \
                  groupby('school_name')['learner_id'].nunique().reset_index()
      df_second_dose.rename(columns={'learner_id': 'second_dose'}, inplace=True)
      self.df_main = pd.merge(self.df_main, df_second_dose, on='school_name', how='left')
      self.df_main['second_dose'] = self.df_main['second_dose'].fillna(0)
      self.df_main['second_dose'] = self.df_main['second_dose'].astype('int')

   def add_aefi(self):
      df_aefi = self.df_logs[self.df_logs.type.eq(4)]. \
                  groupby('school_name')['learner_id'].nunique().reset_index()
      df_aefi.rename(columns={'learner_id': 'aefi'}, inplace=True)
      self.df_main = pd.merge(self.df_main, df_aefi, on='school_name', how='left')
      self.df_main['aefi'] = self.df_main['aefi'].fillna(0)
      self.df_main['aefi'] = self.df_main['aefi'].astype('int')

   def add_absent(self):
      df_absent = self.df_logs[self.df_logs.type.eq(5)]. \
                  groupby('school_name')['learner_id'].nunique().reset_index()
      df_absent.rename(columns={'learner_id': 'absent'}, inplace=True)
      self.df_main = pd.merge(self.df_main, df_absent, on='school_name', how='left')
      self.df_main['absent'] = self.df_main['absent'].fillna(0)
      self.df_main['absent'] = self.df_main['absent'].astype('int')

   def add_left(self):
      df_left = self.df_logs[self.df_logs.type.eq(6)]. \
                  groupby('school_name')['learner_id'].nunique().reset_index()
      df_left.rename(columns={'learner_id': 'left'}, inplace=True)
      self.df_main = pd.merge(self.df_main, df_left, on='school_name', how='left')
      self.df_main['left'] = self.df_main['left'].fillna(0)
      self.df_main['left'] = self.df_main['left'].astype('int')

   def add_contra(self):
      df_contra = self.df_logs[self.df_logs.type.isin([10, 11])]. \
                  groupby('school_name')['learner_id'].nunique().reset_index()
      df_contra.rename(columns={'learner_id': 'contra'}, inplace=True)
      self.df_main = pd.merge(self.df_main, df_contra, on='school_name', how='left')
      self.df_main['contra'] = self.df_main['contra'].fillna(0)
      self.df_main['contra'] = self.df_main['contra'].astype('int')

   def add_underage(self):
      df_underage = self.df_logs[self.df_logs.age < 9]. \
                  groupby('school_name')['learner_id'].nunique().reset_index()
      df_underage.rename(columns={'learner_id': 'underage'}, inplace=True)
      self.df_main = pd.merge(self.df_main, df_underage, on='school_name', how='left')
      self.df_main['underage'] = self.df_main['underage'].fillna(0)
      self.df_main['underage'] = self.df_main['underage'].astype('int')

   def add_first_dose_9(self):
      df_first_dose_9 = self.df_logs[(self.df_logs.type.eq(2)) & (self.df_logs.age.eq(9))]. \
                  groupby('school_name')['learner_id'].nunique().reset_index()
      df_first_dose_9.rename(columns={'learner_id': 'first_dose_9'}, inplace=True)
      self.df_main = pd.merge(self.df_main, df_first_dose_9, on='school_name', how='left')
      self.df_main['first_dose_9'] = self.df_main['first_dose_9'].fillna(0)
      self.df_main['first_dose_9'] = self.df_main['first_dose_9'].astype('int')

   def add_first_dose_10(self):
      df_first_dose_10 = self.df_logs[(self.df_logs.type.eq(2)) & (self.df_logs.age.eq(10))]. \
                  groupby('school_name')['learner_id'].nunique().reset_index()
      df_first_dose_10.rename(columns={'learner_id': 'first_dose_10'}, inplace=True)
      self.df_main = pd.merge(self.df_main, df_first_dose_10, on='school_name', how='left')
      self.df_main['first_dose_10'] = self.df_main['first_dose_10'].fillna(0)
      self.df_main['first_dose_10'] = self.df_main['first_dose_10'].astype('int')

   def add_first_dose_11(self):
      df_first_dose_11 = self.df_logs[(self.df_logs.type.eq(2)) & (self.df_logs.age.eq(11))]. \
                  groupby('school_name')['learner_id'].nunique().reset_index()
      df_first_dose_11.rename(columns={'learner_id': 'first_dose_11'}, inplace=True)
      self.df_main = pd.merge(self.df_main, df_first_dose_11, on='school_name', how='left')
      self.df_main['first_dose_11'] = self.df_main['first_dose_11'].fillna(0)
      self.df_main['first_dose_11'] = self.df_main['first_dose_11'].astype('int')

   def add_first_dose_12(self):
      df_first_dose_12 = self.df_logs[(self.df_logs.type.eq(2)) & (self.df_logs.age.eq(12))]. \
                  groupby('school_name')['learner_id'].nunique().reset_index()
      df_first_dose_12.rename(columns={'learner_id': 'first_dose_12'}, inplace=True)
      self.df_main = pd.merge(self.df_main, df_first_dose_12, on='school_name', how='left')
      self.df_main['first_dose_12'] = self.df_main['first_dose_12'].fillna(0)
      self.df_main['first_dose_12'] = self.df_main['first_dose_12'].astype('int')

   def add_first_dose_13(self):
      df_first_dose_13 = self.df_logs[(self.df_logs.type.eq(2)) & (self.df_logs.age.eq(13))]. \
                  groupby('school_name')['learner_id'].nunique().reset_index()
      df_first_dose_13.rename(columns={'learner_id': 'first_dose_13'}, inplace=True)
      self.df_main = pd.merge(self.df_main, df_first_dose_13, on='school_name', how='left')
      self.df_main['first_dose_13'] = self.df_main['first_dose_13'].fillna(0)
      self.df_main['first_dose_13'] = self.df_main['first_dose_13'].astype('int')

   def add_first_dose_14(self):
      df_first_dose_14 = self.df_logs[(self.df_logs.type.eq(2)) & (self.df_logs.age.eq(14))]. \
                  groupby('school_name')['learner_id'].nunique().reset_index()
      df_first_dose_14.rename(columns={'learner_id': 'first_dose_14'}, inplace=True)
      self.df_main = pd.merge(self.df_main, df_first_dose_14, on='school_name', how='left')
      self.df_main['first_dose_14'] = self.df_main['first_dose_14'].fillna(0)
      self.df_main['first_dose_14'] = self.df_main['first_dose_14'].astype('int')

   def add_first_dose_15(self):
      df_first_dose_15 = self.df_logs[(self.df_logs.type.eq(2)) & (self.df_logs.age >= 15)]. \
                  groupby('school_name')['learner_id'].nunique().reset_index()
      df_first_dose_15.rename(columns={'learner_id': 'first_dose_15'}, inplace=True)
      self.df_main = pd.merge(self.df_main, df_first_dose_15, on='school_name', how='left')
      self.df_main['first_dose_15'] = self.df_main['first_dose_15'].fillna(0)
      self.df_main['first_dose_15'] = self.df_main['first_dose_15'].astype('int')

   def add_doses_used(self):
      df_doses_used = self.df_logs[(self.df_logs.type.eq(2)) | (self.df_logs.type.eq(3))]. \
                  groupby('school_name')['learner_id'].nunique().reset_index()
      df_doses_used.rename(columns={'learner_id': 'doses_used'}, inplace=True)
      self.df_main = pd.merge(self.df_main, df_doses_used, on='school_name', how='left')
      self.df_main['doses_used'] = self.df_main['doses_used'].fillna(0)
      self.df_main['doses_used'] = self.df_main['doses_used'].astype('int')

   def add_doses_wasted(self):
      df_doses_wasted = self.df_add.groupby('school_name')['dose_wasted'].sum().reset_index()
      df_doses_wasted.rename(columns={'dose_wasted': 'doses_wasted'}, inplace=True)
      self.df_main = pd.merge(self.df_main, df_doses_wasted, on='school_name', how='left')
      self.df_main['doses_wasted'] = self.df_main['doses_wasted'].fillna(0)
      self.df_main['doses_wasted'] = self.df_main['doses_wasted'].astype('int')


   def format_data(self):
      self.add_consent()
      self.add_first_dose()
      self.add_second_dose()
      self.add_aefi()
      self.add_absent()
      self.add_left()
      self.add_contra()
      self.add_underage()
      self.add_first_dose_9()
      self.add_first_dose_10()
      self.add_first_dose_11()
      self.add_first_dose_12()
      self.add_first_dose_13()
      self.add_first_dose_14()
      self.add_first_dose_15()
      self.add_doses_used()
      self.add_doses_wasted()

   def get_data(self):
      return self.df_main


   




      
