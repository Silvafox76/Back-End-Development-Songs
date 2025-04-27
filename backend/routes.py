from . import app
import os
import json
import pymongo
from flask import jsonify, request, make_response, abort
from pymongo import MongoClient
from bson import json_util
import sys
from pymongo.results import InsertOneResult

# Load songs data
SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "songs.json")
songs_list: list = json.load(open(json_url))

# Setup MongoDB connection
mongodb_service = os.environ.get('MONGODB_SERVICE', '172.21.152.110')  # Your Host
mongodb_port = int(os.environ.get('MONGODB_PORT', 27017))              # Your Port
mongodb_username = os.environ.get('MONGODB_USERNAME', 'root')          # Your Username
mongodb_password = os.environ.get('MONGODB_PASSWORD', 'C2Xf6gqZeMb98vfgDO9nmwRA')  # Your Password

print(f'The value of MONGODB_SERVICE is: {mongodb_service}')

if mongodb_service is None:
    app.logger.error('Missing MongoDB server in the MONGODB_SERVICE variable')
    sys.exit(1)

# Full MongoDB connection URL
url = f"mongodb://{mongodb_username}:{mongodb_password}@{mongodb_service}:{mongodb_port}"

print(f"connecting to url: {url}")

try:
    client = MongoClient(url)
except pymongo.errors.OperationFailure as e:
    app.logger.error(f"Authentication error: {str(e)}")

db = client.band  # Use 'band' database
songs_collection = db.songs

# Reset songs collection
songs_collection.drop()
songs_collection.insert_many(songs_list)

# Utility to parse BSON/JSON
def parse_json(data):
    return json.loads(json_util.dumps(data))

######################################################################
# Routes
######################################################################

# Health check endpoint
@app.route("/health", methods=["GET"])
def healthz():
    return jsonify(dict(status="OK")), 200

# Count endpoint
@app.route("/count", methods=["GET"])
def count():
    """Return number of documents in the collection."""
    count = songs_collection.count_documents({})
    return {"count": count}, 200

# GET /song - List all songs
@app.route("/song", methods=["GET"])
def songs():
    results = list(songs_collection.find({}))
    print(results[0])  # Optional: helps during debug
    return {"songs": parse_json(results)}, 200

# GET /song/<id> - Get song by ID
@app.route("/song/<int:id>", methods=["GET"])
def get_song_by_id(id):
    song = songs_collection.find_one({"id": id})
    if not song:
        return {"message": f"song with id {id} not found"}, 404
    return parse_json(song), 200

# POST /song - Create a new song
@app.route("/song", methods=["POST"])
def create_song():
    song_in = request.json
    print(song_in["id"])
    # Check if song with same id already exists
    song = songs_collection.find_one({"id": song_in["id"]})
    if song:
        return {"Message": f"song with id {song_in['id']} already present"}, 302
    insert_id: InsertOneResult = songs_collection.insert_one(song_in)
    return {"inserted id": parse_json(insert_id.inserted_id)}, 201

# PUT /song/<id> - Update a song
@app.route("/song/<int:id>", methods=["PUT"])
def update_song(id):
    song_in = request.json
    song = songs_collection.find_one({"id": id})
    if song is None:
        return {"message": "song not found"}, 404
    updated_data = {"$set": song_in}
    result = songs_collection.update_one({"id": id}, updated_data)
    if result.modified_count == 0:
        return {"message": "song found, but nothing updated"}, 200
    else:
        return parse_json(songs_collection.find_one({"id": id})), 201

# DELETE /song/<id> - Delete a song
@app.route("/song/<int:id>", methods=["DELETE"])
def delete_song(id):
    result = songs_collection.delete_one({"id": id})
    if result.deleted_count == 0:
        return {"message": "song not found"}, 404
    else:
        return "", 204
