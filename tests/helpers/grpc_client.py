import grpc
import payment_pb2
import payment_pb2_grpc


class PaymentClient:

    def __init__(self):
        self.channel = grpc.insecure_channel("localhost:50051")
        self.stub = payment_pb2_grpc.PaymentServiceStub(self.channel)

    def process_payment(self, order_id, trace_id):
        return self.stub.ProcessPayment(
            payment_pb2.PaymentRequest(
                order_id=order_id,
                trace_id=trace_id,
            )
        )
