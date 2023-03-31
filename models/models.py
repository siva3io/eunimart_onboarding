# -*- coding: utf-8 -*-

from odoo import models, fields, api
import pandas as pd
import numpy as np
import json
from scipy.stats import binom



class onboarding(models.Model):
    _name = 'onboarding.onboarding'
    _description = 'onboarding.onboarding'
    
    user_id = fields.Char()
    
    question_1 = fields.Boolean()
    question_5 = fields.Boolean()

    # solution_ids = fields.Many2one("onboarding.solution")   

    user = fields.Integer()
    crossborder = fields.Integer()
    warehouse = fields.Integer()
    shipping = fields.Integer()
    accounting = fields.Integer()
    social_commerce = fields.Integer()
    marketplaces = fields.Integer()
    trader = fields.Integer()
    retail = fields.Integer()
    manufacturer = fields.Integer()

    @api.model
    def create(self,vals):
        return super(onboarding,self).create(vals)

    def onboard(self,payload):
        df1 = pd.DataFrame([payload["q1"],payload["q2"],payload["q3"],payload["q4"],payload["q5"]],columns=['questions'])



        def caliberate(null_hypothesis,alpha=0.1,prob=0.7,n=5 ):
            p_value = []
            for i in range(1,20):
                temp = df1['questions'].sample(n=5)
                k = dict(temp.value_counts()).get(1,0)
                res = binomtest(k,n,prob)
                p_value.append(res.pvalue)
                #print(p_value)
            #print(p_value)
            for a_p_value in p_value:
                if a_p_value < alpha: #rejecting the null hypothesis
                    return 1-null_hypothesis
                return null_hypothesis 



        df = pd.read_csv('C:\odoo\custom\onboarding\data\data.csv')
        df.set_index('user',inplace=True)
        df_t = df.T
        for i in df_t.columns:
            df_t[i] = df_t[i].apply(caliberate)
        
        solution_df = df_t.T
        solution_df["user"]= [no for no in range(1,21)]
        solution_json = json.loads(solution_df.to_json(orient='records'))

        result = { 
            "user_id" : payload["user_id"],
            "crossborder" : solution_json[0]["crossborder"],
            "warehouse" : solution_json[0]["warehouse"],
            "shipping" : solution_json[0]["shipping"],
            "accounting" : solution_json[0]["accounting"] ,
            "social_commerce" : solution_json[0]["social_commerce"] ,
            "marketplaces" : solution_json[0]["marketplaces"],
            "trader" : solution_json[0]["trader"],
            "retail" : solution_json[0]["retail"],
            "manufacturer" : solution_json[0]["manufacturer"],
            
        }

        for element in solution_json:
            rec = self.env["onboarding.onboarding"].sudo().create({
                "user_id"    : payload["user_id"],
                "question_1" : payload["q1"],
                "question_2" : payload["q2"],
                "question_3" : payload["q3"],
                "question_4" : payload["q4"],
                "question_5" : payload["q5"],
                "user": element["user"],
                "crossborder" : element["crossborder"],
                "warehouse" : element["warehouse"],
                "shipping" : element["shipping"],
                "accounting" : element["accounting"] ,
                "social_commerce" : element["social_commerce"] ,
                "marketplaces" : element["marketplaces"],
                "trader" : element["trader"],
                "retail" : element["retail"],
                "manufacturer" : element["manufacturer"],
            })
        return result
    
# class onboardsolution(models.Model):
#     _name = "onboarding.solution"
#     _description = "onboarding.solution"

    
#     question_id = fields.One2many("onboarding.onboarding","solution_ids")

# class onboardquestions(models.Model):
#     _name = 'onboarding.questions'
#     _description = 'onboarding.questions'

#     question = fields.Text()

