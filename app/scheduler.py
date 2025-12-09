import os
from datetime import date

from sqlalchemy import func
from taskiq import TaskiqScheduler
from taskiq_aio_pika import AioPikaBroker
from taskiq.schedule_sources import LabelScheduleSource

from app.database import SessionLocal
from app import models


RABBIT_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@localhost:5672/")

broker = AioPikaBroker(
    RABBIT_URL,
    exchange_name="report",
    queue_name="cmd_order",
)

scheduler = TaskiqScheduler(
    broker=broker,
    sources=[LabelScheduleSource(broker)],
)


def _build_reports_for_date(report_day: date) -> None:
    """Aggregate order_items into order_reports for a specific day."""
    db = SessionLocal()
    try:
        # Remove existing reports for the day to avoid duplicates
        db.query(models.OrderReport).filter(
            models.OrderReport.report_at == report_day
        ).delete()

        # Aggregate product counts per order_id
        subq = (
            db.query(
                models.Order.id.label("order_id"),
                func.date(models.Order.created_at).label("report_at"),
                func.sum(models.OrderItem.quantity).label("count_product"),
            )
            .join(models.OrderItem, models.OrderItem.order_id == models.Order.id)
            .filter(func.date(models.Order.created_at) == report_day)
            .group_by(models.Order.id, func.date(models.Order.created_at))
            .subquery()
        )

        rows = db.query(subq.c.report_at, subq.c.order_id, subq.c.count_product).all()
        for row in rows:
            report_at_val = row.report_at
            if isinstance(report_at_val, str):
                report_at_val = date.fromisoformat(report_at_val)

            db.add(
                models.OrderReport(
                    report_at=report_at_val,
                    order_id=row.order_id,
                    count_product=row.count_product or 0,
                )
            )
        db.commit()
    finally:
        db.close()


@broker.task(
    schedule=[
        {
            "cron": "*/1 * * * *",  # every minute
            "args": ["Cron_User"],
            "schedule_id": "greet_every_minute",
        }
    ]
)
async def my_scheduled_task(name: str) -> str:
    """Generate order reports for today and send acknowledgement."""
    today = date.today()
    _build_reports_for_date(today)
    return f"Scheduled hello to {name} at every minute! Generated report for {today}"

