from rest_framework.renderers import JSONRenderer


class APIJSONRenderer(JSONRenderer):
    base_format = {"message": ""}
    success_format = {"success": True, "meta": {}, **base_format}
    failure_format = {"success": False}

    def set_error_response(self, data):
        errors = data.get("errors")
        message = data.get("message")

        if errors:
            self.failure_format["error"] = errors
        else:
            self.failure_format["error"] = data

        self.base_format["message"] = message
        self.failure_format.update(**self.base_format)

    def get_proper_response(self, data):
        # TODO: paginated results will also be a single object so will have to adjust accordingly
        meta = dict()

        if isinstance(data, dict):
            if "meta" in data.keys():
                meta = data.pop("meta")

            if "errors" in data:
                self.set_error_response(data=data)
                return self.failure_format

            self.success_format.update(data=data, meta=meta)
            return self.success_format

        self.success_format.update(
            data={
                "results": data,
                "count": len(data) if data else 0
            }
        )
        return self.success_format

    def render(self, data, accepted_media_type=None, renderer_context=None):
        data = self.get_proper_response(data=data)

        return super().render(
            data=data,
            accepted_media_type=accepted_media_type,
            renderer_context=renderer_context,
        )


# from rest_framework import status
# class APIJSONRenderer(JSONRenderer):
#     def render(self, data, accepted_media_type=None, renderer_context=None):
#         status_code = renderer_context["response"].status_code
#         success = False

#         if status.is_success(code=status_code) or status.is_redirect(code=status_code):
#             success = True

#         if not data:
#             data = dict(status_code=status_code, success=success)
#             return super().render(data, accepted_media_type, renderer_context)

#         if isinstance(data, list):
#             data = {"results": data}
#         else:
#             if not data.get("results", []) and "results" not in data.keys() and success:
#                 data = {"results": [data]}

#         data.update(status_code=status_code, success=success)
#         return super().render(data, accepted_media_type, renderer_context)
