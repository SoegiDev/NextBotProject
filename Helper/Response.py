class Response:

    @staticmethod
    def get_res(code, content, error):
        res = {"code": code, "data": content, "error": error}
        return res
