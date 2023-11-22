"""A Crossplane composition function."""

import grpc
from crossplane.function import logging, response
from crossplane.function.proto.v1beta1 import run_function_pb2 as fnv1beta1
from crossplane.function.proto.v1beta1 import run_function_pb2_grpc as grpcv1beta1


class FunctionRunner(grpcv1beta1.FunctionRunnerService):
    """A FunctionRunner handles gRPC RunFunctionRequests."""

    def __init__(self):
        """Create a new FunctionRunner."""
        self.log = logging.get_logger()

    async def RunFunction(
        self, req: fnv1beta1.RunFunctionRequest, _: grpc.aio.ServicerContext
    ) -> fnv1beta1.RunFunctionResponse:
        """Run the function."""
        log = self.log.bind(tag=req.meta.tag)
        log.info("Running function")

        rsp = response.to(req)

        example = ""
        if "example" in req.input:
            example = req.input["example"]

        # TODO: Add your function logic here!
        response.normal(rsp, f"I was run with input {example}!")
        log.info("I was run!", input=example)

        return rsp
