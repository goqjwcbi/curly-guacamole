from flask import render_template


@staticmethod
def error_page(error_code, error_desc):

    if error_desc == None:
        if error_code == 400:
            error_desc = "Bad Request"
        elif error_code == 401:
            error_desc = "Unauthorized"
        elif error_code == 403:
            error_desc = "Forbidden"
        elif error_code == 404:
            error_desc = "Not Found"
        elif error_code == 500:
            error_desc = "Internal Server Error"
        elif error_code == 503:
            error_desc = "Service Unavailable"

    return render_template("error.html", error_code=error_code, error_desc=error_desc)
