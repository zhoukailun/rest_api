from fastapi.responses import JSONResponse
from fastapi import status


def response_create(count):
    return JSONResponse(
        content={"result": True, "count_succ": count, "messages": "Create data successfully."},
        status_code=status.HTTP_201_CREATED,
    )


def response_search(count, data):
    return JSONResponse(
        content={"result": True, "count_succ": count, "messages": "Search data successfully.", "data": data},
        status_code=status.HTTP_200_OK,
    )


def response_search_error(reason):
    return JSONResponse(
        content={"result": False, "messages": "Failed to search data. Reason: " + reason},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


def response_update(count):
    return JSONResponse(
        content={"result": True, "count_succ": count, "messages": "Update data successfully."},
        status_code=status.HTTP_201_CREATED,
    )


def response_update_error(count, reason):
    return JSONResponse(
        content={"result": False, "count_succ": count, "messages": "Update data interrupted. Reason: " + reason},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


def response_error(errors):
    return JSONResponse(
        content={"result": False, "messages": str(errors)},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


def response_error_asset_type():
    return JSONResponse(
        content={"result": False, "messages": "Unknown asset type."},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


def response_error_attribute():
    return JSONResponse(
        content={"result": False, "messages": "Asset type and fields provided not matching."},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


def response_empty_data():
    return JSONResponse(
        content={"result": False, "messages": "Empty data provided."},
        status_code=status.HTTP_400_BAD_REQUEST,
    )


def response_test(start, end):
    return JSONResponse(
        content={"result": True, "count_succ": int(end) - int(start), "messages": "Mock data {}-{} imported.".format(str(start), str(end))},
        status_code=status.HTTP_201_CREATED,
    )


def response_test_error(start):
    return JSONResponse(
        content={"result": False, "messages": "Mock data '{}' was already imported".format(str(start))},
        status_code=status.HTTP_400_BAD_REQUEST,
    )