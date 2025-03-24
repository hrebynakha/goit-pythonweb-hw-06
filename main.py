import argparse
import os
import sys
import logging
from helpers import convert_args, capitalize, log_query_result
from crud.create import new_object
from crud.read import list_objects
from crud.mapping import MODEL_MAPPING
from crud.update import update_object
from crud.delete import delete_object

parser = argparse.ArgumentParser(
    description="""
Create \ Read \ Update \ Delete objects in database
"""
)
parser.add_argument("--action", "-a", type=str, help="Action for crud")
parser.add_argument("--model", "-m", type=str, help="Model")
parser.add_argument(
    "--columns",
    "-c",
    nargs="?",
    type=str,
    help="Columns to show",
    default=["id", "first_name", "last_name"],
)
parser.add_argument("--id", "-i", nargs="?", type=str, help="Object id")
parser.add_argument("rest", nargs=argparse.REMAINDER)

logging.basicConfig(
    format="%(asctime)s %(levelname)s %(message)s",
    level=logging.DEBUG,
    handlers=[logging.StreamHandler()],
)

logging.getLogger().setLevel(logging.INFO)


input_args = parser.parse_args()
logging.debug("Input args %s", input_args)
print(input_args.columns)
action, model_name, columns, object_id, rest = (
    input_args.action,
    capitalize(input_args.model),
    input_args.columns.split(","),
    input_args.id,
    convert_args(input_args.rest),
)
logging.debug("Processing action: %s model: %s ", action, model_name)
model = MODEL_MAPPING.get(model_name)
if not model:
    raise ValueError("Model not found.")

if action in ["create", "new", "add"]:
    result = new_object(model, **rest)
    log_query_result(result)
elif action in ["read", "list", "select", "lst"]:
    result = list_objects(model, columns_name=columns, **rest)
    log_query_result(result)
elif action in ["update", "upd", "renew", "re", "change", "cng"]:
    result = update_object(model, object_id=object_id, **rest)
    log_query_result(result)
elif action in ["delete", "remove", "del", "rm"]:
    result = delete_object(model, object_id=object_id)
    logging.info("Deleted object in DB")
else:
    logging.error("Not avaliable input action '%s'", action)
