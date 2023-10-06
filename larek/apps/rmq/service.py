import json
import logging

logger = logging.getLogger(__name__)


class RMQService:
    @staticmethod
    def consume_payment_message(ch, method, properties, body):
        logger.info(f"Consume new message with payload {body}")
        data = json.loads(body)

        try:
            from larek.apps.payment.models import Payment

            Payment.confirm_payment(data=data)
        except Exception:
            logger.exception(f"Updating payment {data=} into db error")

        ch.basic_ack(delivery_tag=method.delivery_tag)
