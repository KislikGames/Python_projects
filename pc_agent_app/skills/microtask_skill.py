def run_earn_task(target_amount_rub: int, payout_details: str | None) -> str:
    if not payout_details:
        return (
            "Need payout details before proceeding (phone or bank card placeholder). "
            "No financial actions were executed."
        )

    return (
        f"Prepared a safe microtask plan to earn {target_amount_rub} RUB. "
        "Workflow: choose legal platform -> publish profile -> accept small task -> confirm payment received -> "
        f"request final user approval before transferring to: {payout_details}."
    )
