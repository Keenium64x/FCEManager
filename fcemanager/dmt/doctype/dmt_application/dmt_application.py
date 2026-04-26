# Copyright (c) 2026, Keenan Solomon and contributors
# For license information, please see license.txt

# import frappe
from frappe.model.document import Document


class DMTApplication(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		an_fce_or_ufce_student: DF.Check
		booth_at_a_missionschurch_conference: DF.Check
		friend: DF.Check
		have_you_answered_gods_call_to_discipleship: DF.LongText | None
		other: DF.SmallText | None
		parentguardian: DF.Check
		pastor_church_member_or_spiritual_mentor: DF.Check
		referral_person_or_organisation: DF.Data | None
		small_text_rdfp: DF.SmallText | None
		social_media_post: DF.Check
		training_intake: DF.Link | None
		what_are_the_things_the_lord_is_teaching_you_at_the_moment: DF.SmallText | None
		what_are_your_expectations_for_this_training: DF.SmallText | None
		what_is_your_motivation_for_applying_for_this_training: DF.SmallText | None
	# end: auto-generated types

	pass
