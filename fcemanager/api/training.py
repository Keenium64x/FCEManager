"""Guest-safe website API for current DMT training periods."""

from collections import defaultdict
from typing import Any

import frappe
from frappe.utils import getdate, now_datetime, today


# =============================================================================
# region PUBLIC TRAINING CATALOGUE
# =============================================================================


@frappe.whitelist(allow_guest=True)
def get_public_training_periods() -> dict[str, Any]:
	"""Return non-expired DMT periods and their linked training centres."""
	periods = frappe.get_all(
		"DMT Period",
		filters={"end_date": [">=", today()]},
		fields=["name", "dmt_type", "start_date", "end_date", "duration"],
		order_by="start_date asc, name asc",
		ignore_permissions=True,
	)

	if not periods:
		return {"periods": [], "generated_at": now_datetime().isoformat()}

	period_names = [period.name for period in periods]
	intakes = frappe.get_all(
		"Training Intake",
		filters={"period": ["in", period_names]},
		fields=["period", "training_centre"],
		order_by="period asc, training_centre asc",
		ignore_permissions=True,
	)

	centre_names = sorted(
		{intake.training_centre for intake in intakes if intake.training_centre}
	)
	centres = (
		frappe.get_all(
			"Training Centre",
			filters={"name": ["in", centre_names]},
			fields=["name", "centre", "country", "adress"],
			ignore_permissions=True,
		)
		if centre_names
		else []
	)
	centres_by_name = {centre.name: centre for centre in centres}
	centres_by_period: dict[str, list[dict[str, str | None]]] = defaultdict(list)
	seen_links: set[tuple[str, str]] = set()

	for intake in intakes:
		link_key = (intake.period, intake.training_centre)
		centre = centres_by_name.get(intake.training_centre)
		if not centre or link_key in seen_links:
			continue
		seen_links.add(link_key)
		centres_by_period[intake.period].append(
			{
				"name": centre.name,
				"centre": centre.centre or centre.name,
				"country": centre.country,
				"address": centre.adress,
			}
		)

	public_periods = []
	for period in periods:
		public_periods.append(
			{
				"name": period.name,
				"dmt_type": period.dmt_type,
				"start_date": getdate(period.start_date).isoformat(),
				"end_date": getdate(period.end_date).isoformat(),
				"duration_seconds": period.duration,
				"centres": centres_by_period.get(period.name, []),
			}
		)

	return {
		"periods": public_periods,
		"generated_at": now_datetime().isoformat(),
	}


# endregion PUBLIC TRAINING CATALOGUE
