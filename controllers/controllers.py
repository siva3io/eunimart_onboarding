# -*- coding: utf-8 -*-
from odoo import http
import pandas as pd
import random

class Onboarding(http.Controller):

    # payload = {
    #     "user_id" : "string",
    #     "q1" : true,
    #     "q2" : false,
    #     "q3" : true,
    #     "q4" : false,
    #     "q5" : true,
    # }


    @http.route('/onboarding/calibrate', type="json", auth="public", cors="*", method=["POST"])
    def index(self, **kw):
        payload =  http.request.jsonrequest
        result = http.request.env["onboarding.onboarding"].sudo().onboard(payload)
        return result

    @http.route('/onboarding/questions', type="json", auth="public", cors="*", method=["GET"])
    def get_questions(self,**kw):
        payload = http.request.jsonrequest
        # questions = http.request.env["onboarding.questions"].sudo().search([])
        questions = ["Is your business revenue more than 10 cr?",
                    "Is this the first time you are using this platform?",
                    "Are you above 25 years of age?",
                    "Do you have a competitor in the market?",
                    "Are you on Netflix, youtube, hulu or any other streaming service?",
                    "Are you on Fb marketplace?"]
        return random.sample(questions,5)

    @http.route('/onboarding/response', type="json", auth="public", cors="*", method=["GET"])
    def get_response(self,**kw):
        #this will fetch the payload
        payload = http.request.jsonrequest
        user_id = payload["user_id"]
        response = http.request.env["onboarding.onboarding"].sudo().search([('user_id','=',user_id),('user','=',1)],limit=1)
        result = {"user_id" : payload["user_id"],
                  "crossborder": response.crossborder,
                  "warehouse": response.warehouse,
                  "shipping": response.shipping,
                  "accounting": response.accounting,
                  "social_commerce": response.social_commerce,
                  "marketplaces": response.marketplaces,
                  "trader": response.trader,
                  "retail": response.retail,
                  "manufacturer": response.manufacturer
                  }
        return result


