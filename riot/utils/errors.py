def err_code_to_err_msg(error_code: int) -> str:
    match error_code:
        case 400:
            return "Bad request"
        case 401:
            return "Unauthorized"
        case 403:
            return "Forbidden"
        case 404:
            return "Not found"
        case 405:
            return "Method Not Allowed"
        case 415:
            return "Unsupported Media Type"
        case 429:
            return "Rate Limit Exceeded"
        case 500:
            return "Internal Server Error"
        case 502:
            return "Bad Gateway"
        case 503:
            return "Service unavailable"
        case 504:
            return "Gateway Timeout"
        case _:
            return "Unknown Error"
