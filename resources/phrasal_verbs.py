# -*- coding: utf-8 -*-
from datetime import datetime
import traceback
from flask import request
from flask_restplus import Namespace, Resource, fields, reqparse

from core.db import mongo
from core.resource import CustomResource, response, json_serializer, json_serializer_all_datetime_keys
from core.utils import check_if_only_int_numbers_exist, token_required, parse_given_str_datetime_or_current_datetime


api = Namespace('phrasal-verbs', description='Phrasal_verbs related operations')

def get_only_verbs():
    verbs = mongo.db.phrasal_verbs.distinct("verb");
    return verbs

def get_phrasal_verbs(verb=None):
    query = {}
    if verb is not None:
        query["verb"] = verb

    phrasal_verbs = []
    for item in mongo.db.phrasal_verbs.find(query):
        phrasal_verb = {}
        for key, value in item.items():
            if key == '_id': 
                value = str(value)
            if key == 'created_time':
                value = json_serializer(value)
            
            phrasal_verb[key] = value
        phrasal_verbs.append(phrasal_verb)
    return phrasal_verbs

def upsert_phrasal_verbs(args):
    try:
        verb = args.verb
        particle = args.particle
        definitions = args.definitions
        sentences = args.sentences
        level = args.level
        is_public = args.is_public
        
        search_query = {"verb": verb}
        phrasal_verb_data = {}

        # old data
        if items := mongo.db.phrasal_verbs.find(search_query):
            for item in items:
                for key, value in item.items():
                    phrasal_verb_data[key] = value
        
        # new verb
        if phrasal_verb_data.get("verb") is None:
            phrasal_verb_data["verb"] = verb

        # first particle
        if phrasal_verb_data.get("particles") is None:
            phrasal_verb_data["particles"] = {}
        phrasal_verb_data["particles"][particle] = {
            "definitions": definitions,
            "sentences": sentences,
            "level": level,
            "is_public": is_public
        }
        
        mongo.db.phrasal_verbs.replace_one(search_query, phrasal_verb_data, upsert=True)

        return True
    except:
        traceback.print_exc()
        return False

def delete_phrasal_verbs():
    try:
        mongo.db.phrasal_verbs.delete_many({})
        return True
    except:
        traceback.print_exc()
        return False

parser_create = reqparse.RequestParser()
parser_create.add_argument('verb', type=str, required=True, help='Verb')
parser_create.add_argument('particle', type=str, required=True, help='Particle(adverb or preposition')
parser_create.add_argument('definitions', type=str, help='Definitions', action='append')
parser_create.add_argument('sentences', type=str, help='Sentences', action='append')
parser_create.add_argument('level', type=int, help='Learning level')
parser_create.add_argument('is_public', type=int, help='Public')

parser_search_verb = reqparse.RequestParser()
parser_search_verb.add_argument('only_verb', type=int, location="args")
parser_search_verb.add_argument('verb', type=str, help='Verb')

parser_search = reqparse.RequestParser()
parser_search.add_argument('particle', type=str, help='Particle(adverb or preposition', location="args")

@api.route('/')
class PhrasalVerbs(CustomResource):
    @api.doc('list of phrasal_verbs')
    @api.expect(parser_search_verb)
    @api.response(203, 'Phrasal verb does not exist')
    def get(self):
        '''List all phrasal verbs'''
        args = parser_search_verb.parse_args()
        if args['only_verb'] == 1:
            result = get_only_verbs()
        else:
            result = get_phrasal_verbs(verb=args["verb"])
        status = 200 if result else 203
        return self.send(status=status, result=result)
    
    @api.doc('add a phrasal verb')
    @api.expect(parser_create)
    @api.response(409, 'Duplicate phrasal verb')
    def post(self):
        '''Add an phrasal verb'''
        
        args = parser_create.parse_args()
        result = upsert_phrasal_verbs(args)
        status = 200 if result else 400
        
        return self.send(status=status)

    @api.doc('delete a phrasal verb')
    def delete(self):
        '''Delete an phrasal verb'''
        
        result = delete_phrasal_verbs()
        status = 200 if result else 400
        
        return self.send(status=status)

@api.route('/<string:verb>')
class PhrasalVerb(CustomResource):
    @api.doc('phrasal_verb')
    @api.response(203, 'Phrasal verb does not exist')
    @api.expect(parser_search)
    def get(self,verb):
        '''Get a phrasal verb'''
        args = parser_search.parse_args()     
        result = get_phrasal_verbs(verb=verb, particle=args["particle"])
        status = 200 if result else 203
        return self.send(status=status, result=result)
