#!/usr/bin/env python3
# coding: utf-8
import time
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List
from uuid import uuid4

from flask import Blueprint, Flask, Response, abort, current_app, request
from flask.json import jsonify

GET_STATUS_CODE = 200
POST_STATUS_CODE = 200
JOB_STATUS = [
    "UNKNOWN",
    "QUEUED",
    "RUNNING",
    "COMPLETE",
    "FAILED",
    "CANCELING",
    "CANCELED",
]


# --- state ---


executor = ThreadPoolExecutor(max_workers=3)
job_map = {}
request_map = {}


# --- controller ---


app_bp = Blueprint("app", __name__)


@app_bp.route("/validate", methods=["POST"])
def validate() -> Response:
    req_id = str(uuid4())
    req_body = request.json or {}
    with current_app.app_context():
        request_map[req_id] = req_body

        # add job to queue
        job = executor.submit(base_job, req_body)
        job_map[req_id] = job

    response: Response = jsonify({"requestId": req_id})
    response.status_code = POST_STATUS_CODE

    return response


@app_bp.route("/<string:req_id>", methods=["GET"])
def get_results(req_id: str) -> Response:
    if req_id not in job_map:
        abort(400, "requestId not found")
    job = job_map[req_id]
    request = request_map[req_id]

    # check status
    status = "UNKNOWN"
    results = []
    if job.running():
        status = "RUNNING"
    elif job.cancelled():
        status = "CANCELED"
    elif job.done():
        # COMPLETE or FAILED
        if job.exception() is None:
            status = "COMPLETE"
            # TODO: The expected original results are a list of exceptions (or a exception), however here I assume the results are a list of dicts. (which means we need to write a wrapper)
            results = job.result()
        else:
            status = "FAILED"
            results = [{"err_msg": str(job.exception())}]

    response: Response = jsonify({
        "requestId": req_id,
        "request": request,
        "status": status,
        "results": results
    })
    response.status_code = GET_STATUS_CODE

    return response


@app_bp.route("/<string:req_id>/cancel", methods=["POST"])
def cancel(req_id: str) -> Response:
    if req_id not in job_map:
        abort(400, "requestId not found")
    job = job_map[req_id]
    try_cancel = job.cancel()
    if not try_cancel:
        abort(400, "Failed to cancel")
    response: Response = jsonify({"requestId": req_id})
    response.status_code = POST_STATUS_CODE

    return response


# --- job ---


def base_job(request: Dict[str, Any]) -> List[Dict[str, Any]]:  # type: ignore
    if "error" in request:
        error_job(request)
    else:
        return some_long_job(request)


def some_long_job(request: Dict[str, Any]) -> List[Dict[str, Any]]:
    time.sleep(60)

    return [{"key": k, "val": v} for k, v in request.items()]


def error_job(request: Dict[str, Any]) -> None:
    raise Exception(f"This is our implemented error: {request['error']}")


# --- app ---


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(app_bp)

    # for debug
    app.config["FLASK_ENV"] = "development"
    app.config["DEBUG"] = True
    app.config["TESTING"] = True

    return app


def main() -> None:
    app = create_app()
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True,
    )


if __name__ == "__main__":
    main()
