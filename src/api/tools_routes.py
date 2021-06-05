# -*- coding: utf-8 -*-
import json

from fastapi import APIRouter, File, HTTPException, UploadFile
from loguru import logger
from xmltodict import parse as xml_parse
from xmltodict import unparse as xml_unparse

router = APIRouter()


@router.post("/xml-json")
async def convert_xml(
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
        # xml to json conversion with xmltodict
        result = xml_parse(
            contents, encoding="utf-8", process_namespaces=True, xml_attribs=True
        )
        logger.info("file converted to JSON")
        return result

    except Exception as e:
        logger.critical(f"error: {e}")
        err = str(e)
        # when error occurs output http exception
        if err.startswith("syntax error") is True or e is not None:
            error_exception = f"The syntax of the object is not valid. Error: {e}"
            raise HTTPException(status_code=400, detail=error_exception)


@router.post("/json-xml")
async def convert_json(
    myfile: UploadFile = File(...),
) -> str:
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
        new_dict = json.loads(content.decode("utf8"))
        # xml to json conversion with xmltodict
        result = xml_unparse(new_dict, pretty=True)
        logger.info("file converted to JSON")
        return result

    except Exception as e:
        logger.critical(f"error: {e}")
        err = str(e)
        # when error occurs output http exception
        if err.startswith("Extra data") is True or e is not None:
            error_exception = f"The syntax of the object is not valid. Error: {e}"
            raise HTTPException(status_code=400, detail=error_exception)
