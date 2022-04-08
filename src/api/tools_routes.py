# -*- coding: utf-8 -*-
import json
from unittest import result

from fastapi import APIRouter, File, HTTPException, UploadFile
from loguru import logger
from xmltodict import parse as xml_parse
from xmltodict import unparse as xml_unparse
from benedict import benedict


router = APIRouter()

# csv conversion
# csv to json
@router.post("/csv-json", status_code=201)
async def csv_json(
    myfile: UploadFile = File(...),
) -> dict:

    # determine if file is of zero bytes
    # set file_type to a value
    if len(myfile.content_type) == 0:
        file_type = "unknown"
    else:
        file_type = myfile.content_type

    logger.info(f"file_name: {myfile.filename} file_type: {file_type}")

    file_named = myfile.filename
    # if document is not a json document, give http exception
    if file_named.endswith(".csv", 5) is not True:
        error_exception = (
            f"API requirs a JSON docuement, but file {myfile.filename} is {file_type}"
        )
        logger.critical(error_exception)
        raise HTTPException(status_code=400, detail=error_exception)

    return "test"

# json conversions
# json to xml
# json to toml
# json to yaml

@router.post(
    "/json-xml",
    status_code=201,
)
async def json_xml(
    myfile: UploadFile = File(...),
) -> dict:
    """
    convert json document to xml

    Returns:
        XML object
    """
    # determine if file is of zero bytes
    # set file_type to a value
    if len(myfile.content_type) == 0:
        file_type = "unknown"
    else:
        file_type = myfile.content_type

    logger.info(f"file_name: {myfile.filename} file_type: {file_type}")

    file_named = myfile.filename
    # if document is not a json document, give http exception
    if file_named.endswith(".json", 5) is not True:
        error_exception = (
            f"API requirs a JSON docuement, but file {myfile.filename} is {file_type}"
        )
        logger.critical(error_exception)
        raise HTTPException(status_code=400, detail=error_exception)

    try:
        # async method to get data from file upload
        content = await myfile.read()
        # create a dictionary with decoded content
        convert_to = benedict(content.decode("utf8"), format="json")
        # xml to json conversion with xmltodict
        result = convert_to.to_xml()
        # log information
        logger.info("file converted to JSON")
        logger.debug(result)
        return result

    except Exception as excp:
        logger.critical(f"error: {excp}")
        err = str(excp)
        # when error occurs output http exception
        if err.startswith("Extra data") is True or excp is not None:
            error_exception = f"The syntax of the object is not valid. Error: {excp}"
            raise HTTPException(status_code=400, detail=error_exception)

@router.post("/json-toml", status_code=201)
async def json_toml(
    myfile: UploadFile = File(...),
) -> dict:
    # determine if file is of zero bytes
    # set file_type to a value
    if len(myfile.content_type) == 0:
        file_type = "unknown"
    else:
        file_type = myfile.content_type

    logger.info(f"file_name: {myfile.filename} file_type: {file_type}")

    file_named = myfile.filename
    # if document is not a json document, give http exception
    if file_named.endswith(".json", 5) is not True:
        error_exception = (
            f"API requirs a JSON docuement, but file {myfile.filename} is {file_type}"
        )
        logger.critical(error_exception)
        raise HTTPException(status_code=400, detail=error_exception)

    return "test"


@router.post("/json-yaml", status_code=201)
async def json_yaml(
    myfile: UploadFile = File(...),
) -> dict:
    # determine if file is of zero bytes
    # set file_type to a value
    if len(myfile.content_type) == 0:
        file_type = "unknown"
    else:
        file_type = myfile.content_type

    logger.info(f"file_name: {myfile.filename} file_type: {file_type}")

    file_named = myfile.filename
    # if document is not a json document, give http exception
    if file_named.endswith(".json", 5) is not True:
        error_exception = (
            f"API requirs a JSON docuement, but file {myfile.filename} is {file_type}"
        )
        logger.critical(error_exception)
        raise HTTPException(status_code=400, detail=error_exception)

    return "test"



# xml conversions
# xml to json
# xml to toml
# xml to yaml


@router.post("/xml-json", status_code=201)
async def xml_json(
    myfile: UploadFile = File(...),
) -> dict:
    """
    convert xml document to json

    Returns:
        json object
    """

    # determine if file has no content_type set
    # set file_type to a value
    if len(myfile.content_type) == 0:
        file_type = "unknown"
    else:
        file_type = myfile.content_type

    logger.info(f"file_name: {myfile.filename} file_type: {file_type}")

    file_named = myfile.filename
    # if document is not a xml document, give http exception
    if file_named.endswith(".xml", 4) is not True:
        error_exception = (
            f"API requires a XML docuement, but file {myfile.filename} is {file_type}"
        )
        logger.critical(error_exception)
        raise HTTPException(status_code=400, detail=error_exception)

    try:
        # async method to get data from file upload
        contents = await myfile.read()
        doc = contents.decode("utf-8")
        # xml to json conversion with xmltodict
        result = benedict.from_xml(doc, encoding="utf-8")
        # log information
        logger.info("file converted to JSON")
        logger.debug(result)
        return result

    except Exception as excp:
        logger.critical(f"error: {excp}")
        err = str(excp)
        # when error occurs output http exception
        if err.startswith("syntax error") is True or excp is not None:
            error_exception = f"The syntax of the object is not valid. Error: {excp}"
            raise HTTPException(status_code=400, detail=error_exception)


@router.post("/xml-toml", status_code=201)
async def xml_toml(
    myfile: UploadFile = File(...),
) -> dict:
    # determine if file is of zero bytes
    # set file_type to a value
    if len(myfile.content_type) == 0:
        file_type = "unknown"
    else:
        file_type = myfile.content_type

    logger.info(f"file_name: {myfile.filename} file_type: {file_type}")

    file_named = myfile.filename
    # if document is not a json document, give http exception
    if file_named.endswith(".xml", 5) is not True:
        error_exception = (
            f"API requirs a JSON docuement, but file {myfile.filename} is {file_type}"
        )
        logger.critical(error_exception)
        raise HTTPException(status_code=400, detail=error_exception)

    return "test"

@router.post("/xml-yaml", status_code=201)
async def xml_yaml(
    myfile: UploadFile = File(...),
) -> dict:
    # determine if file is of zero bytes
    # set file_type to a value
    if len(myfile.content_type) == 0:
        file_type = "unknown"
    else:
        file_type = myfile.content_type

    logger.info(f"file_name: {myfile.filename} file_type: {file_type}")

    file_named = myfile.filename
    # if document is not a json document, give http exception
    if file_named.endswith(".xml", 5) is not True:
        error_exception = (
            f"API requirs a JSON docuement, but file {myfile.filename} is {file_type}"
        )
        logger.critical(error_exception)
        raise HTTPException(status_code=400, detail=error_exception)

    return "test"

# toml conversions
# toml to xml
# toml to json
# toml to yaml
@router.post("/toml-xml", status_code=201)
async def toml_xml(
    myfile: UploadFile = File(...),
) -> dict:
    return "test"

@router.post("/toml-json", status_code=201)
async def toml_json(
    myfile: UploadFile = File(...),
) -> dict:
    return "test"

@router.post("/toml-yaml", status_code=201)
async def toml_yaml(
    myfile: UploadFile = File(...),
) -> dict:
    return "test"



# yaml conversions
# yaml to xml
# yaml to json
# yaml to toml
@router.post("/yaml-xml", status_code=201)
async def yaml_xml(
    myfile: UploadFile = File(...),
) -> dict:
    return "test"

@router.post("/yaml-json", status_code=201)
async def yaml_json(
    myfile: UploadFile = File(...),
) -> dict:
    return "test"

@router.post("/yaml-toml", status_code=201)
async def yaml_toml(
    myfile: UploadFile = File(...),
) -> dict:
    return "test"
