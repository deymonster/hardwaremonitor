from fastapi import Depends, HTTPException, status, Request


def get_mongo_db(request: Request):
    return request.app.mongodb

