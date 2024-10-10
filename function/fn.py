"""A Crossplane composition function."""

import grpc
from crossplane.function import logging, resource, response
from crossplane.function.proto.v1 import run_function_pb2 as fnv1
from crossplane.function.proto.v1 import run_function_pb2_grpc as grpcv1


class FunctionRunner(grpcv1.FunctionRunnerService):
    """A FunctionRunner handles gRPC RunFunctionRequests."""

    def __init__(self):
        """Create a new FunctionRunner."""
        self.log = logging.get_logger()

    async def RunFunction(
        self, req: fnv1.RunFunctionRequest, _: grpc.aio.ServicerContext
    ) -> fnv1.RunFunctionResponse:
        """Run the function."""
        log = self.log.bind(tag=req.meta.tag)
        log.info("Running function")

        rsp = response.to(req)

        version = req.input["version"]
        region = req.observed.composite.resource["spec"]["region"]

        resource.update(
            rsp.desired.resources["bucket"],
            {
                "apiVersion": f"s3.aws.upbound.io/{version}",
                "kind": "Bucket",
                "spec": {
                    "forProvider": {"region": region},
                },
            },
        )

        return rsp
