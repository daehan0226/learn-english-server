import os
from flask_pymongo import PyMongo


mongo = PyMongo()


def gen_query(field, search_key, exact=0, insensitive_case=True):
    # {"$text": {"$search": search_key}}

    keyword = f"^{search_key}$" if exact else search_key
    query = {field: {"$regex": keyword}}
    if insensitive_case:  # to match upper and lower cases
        query[field]["$options"] = "i"

    return query


def gen_user_like_query(user_id):
    return {"userId": user_id, "active": 1}


def gen_in_query(field=None, values=None):
    return {field: {"$in": values}}


def gen_random_docs_query(count):
    return {"$sample": {"size": count}}


def gen_not_empty_array_query(field):
    return {f"{field}.0": {"$exists": "true"}}


def gen_not_include_query(field=None):
    return {field: {"$exists": False}}


def gen_include_query(field=None):
    return {field: {"$exists": True}}


def gen_return_fields_query(includes=None, excludes=None):
    query = {}
    if isinstance(includes, list):
        for field in includes:
            query[field] = 1
    if isinstance(excludes, list):
        for field in excludes:
            query[field] = 0

    return query


def gen_match_and_query(filters):
    return {"$match": {"$and": filters}}


def stringify_docs(docs):
    items = []
    for data in docs:
        item = {}
        for key, value in data.items():
            if key == "_id":
                value = str(value)
            if key == "created_time":
                from app.core.resource import json_serializer

                value = json_serializer(value)
            item[key] = value
        items.append(item)
    return items


def gen_collection_active_like_query(field_key=None, field_value=None):
    return {field_key: field_value, "active": 1}


def gen_user_active_like_query(user_id, field_key=None, field_value=None):
    return {field_key: field_value, "active": 1, "userId": user_id}


def gen_restrict_access_query():
    return {"is_public": 1}


def get_all_unique_field_values(field, query=None):
    query = {} if query is None else query
    return mongo.db.phrasal_verbs.distinct(field, query)


def remove_fiedl(field, query):
    mongo.db.phrasal_verbs.update_many(query, {"$unset": {field: ""}})
