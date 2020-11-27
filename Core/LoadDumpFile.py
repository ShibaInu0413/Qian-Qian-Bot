from os import getenv
from json import load, dump
from pymongo import MongoClient

MongoDB = MongoClient(getenv("MongoDB"))

def LoadJsonFile(filename: str) -> dict:
    with open(filename, "r", encoding="UTF-8") as JFile:
        return load(JFile)

def DumpJsonFile(filename: str, data: dict):
    with open(filename, "w", encoding="UTF-8") as JFile:
        dump(data, JFile, indent=4, ensure_ascii=False)