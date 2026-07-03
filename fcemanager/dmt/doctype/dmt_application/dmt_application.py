# Copyright (c) 2026, Keenan Solomon and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


# =============================================================================
# region APPLICATION
# =============================================================================


class DMTApplication(Document):
	# begin: auto-generated types
	# This code is auto-generated. Do not modify anything in this block.

	from typing import TYPE_CHECKING

	if TYPE_CHECKING:
		from frappe.types import DF

		applicant_full_name: DF.Data | None
		associated_with_local_church: DF.Literal["Yes", "No"]
		attend_with_spouse: DF.Literal["Yes", "No", "Maybe"]
		became_follower_of_christ: DF.LongText
		church_financial_support: DF.Literal["Yes", "No", "Not sure"]
		church_missionary_sending: DF.Literal["Yes", "No", "Not sure", "Not applicable"]
		currently_employed: DF.Literal["Yes", "No", "Self-employed"]
		date_of_birth: DF.Date
		date_work_ended: DF.Date | None
		date_work_started: DF.Date | None
		dependants_accompanying: DF.Data
		discipleship_calling: DF.LongText
		discipleship_support: DF.LongText
		email_address: DF.Data
		emergency_contact_address: DF.LongText
		emergency_contact_email: DF.Data
		emergency_contact_name: DF.Data
		emergency_contact_primary_phone: DF.Data
		emergency_contact_relationship: DF.Data
		emergency_contact_secondary_phone: DF.Data | None
		english_fluency: DF.Literal["Native speaker", "Fully fluent", "Working professional ability", "Limited working ability", "Basic conversational ability", "No fluency"]
		expectations_for_training: DF.LongText
		family_feelings_about_training: DF.LongText
		final_agreement: DF.Data
		financial_agreement: DF.Data
		first_name: DF.Data
		gender: DF.Literal["Female", "Male"]
		highest_grade_level: DF.Literal["12", "11", "10", "9", "Other"]
		hobbies: DF.LongText
		home_language: DF.Data
		local_church_address: DF.LongText | None
		local_church_denomination: DF.Data | None
		local_church_email: DF.Data | None
		local_church_involvement: DF.LongText | None
		local_church_name: DF.Data | None
		local_church_phone: DF.Data | None
		lord_teaching_now: DF.LongText
		main_responsibilities: DF.LongText | None
		marital_status: DF.Literal["Single", "Married", "Divorced", "Widowed"]
		middle_names: DF.Data | None
		motivation_for_applying: DF.LongText
		number_of_dependants: DF.Data
		occupation: DF.Data
		other_languages: DF.LongText | None
		pastor_approval: DF.Literal["Yes", "No", "Not sure"]
		pastor_minister_name: DF.Data | None
		payment_plan: DF.Literal["Pay 100% on day of registration", "Pay in monthly installments through training's duration"]
		physical_city: DF.Data | None
		physical_country: DF.Data | None
		physical_line_2: DF.Data | None
		physical_postal_code: DF.Data | None
		physical_state_province: DF.Data | None
		physical_street_address: DF.Data | None
		postal_city: DF.Data
		postal_code: DF.Data | None
		postal_country: DF.Data
		postal_line_2: DF.Data | None
		postal_state_province: DF.Data | None
		postal_street_address: DF.Data
		preferred_name: DF.Data | None
		primary_phone_number: DF.Data
		referral_person_or_organisation: DF.Data | None
		referral_type: DF.Literal["Parent/Guardian", "Friend", "An FCE or UFCE student", "Pastor, church member, or spiritual mentor", "Social media post", "Booth at a missions/church conference", "Other"]
		secondary_phone_number: DF.Data | None
		social_support_network: DF.LongText
		source_of_funds: DF.LongText
		spouse_date_of_birth: DF.Date
		spouse_name: DF.Data
		sufficient_financial_resources: DF.Literal["Yes", "No"]
		surname: DF.Data
		title: DF.Literal["Mr", "Mrs", "Ms", "Miss", "Dr"]
		training_intake: DF.Link | None
		training_intake_choice: DF.Literal["January 2027: DMT Foundation in Pringle Bay, South Africa", "April 2027: DMT Foundation in Okahandja, Namibia", "October 2027: DMT Foundation in Pringle Bay, South Africa", "DMT Extended (Invitation only)", "Not sure"]
		workplace_name: DF.Data | None
		years_of_membership: DF.Data | None
	# end: auto-generated types

	def validate(self):
		self.set_applicant_full_name()
		self.validate_required_agreements()
		self.set_legacy_field_values()

	def set_applicant_full_name(self):
		parts = [self.first_name, self.middle_names, self.surname]
		self.applicant_full_name = " ".join(part.strip() for part in parts if part and part.strip())

	def validate_required_agreements(self):
		for fieldname in ("financial_agreement", "final_agreement"):
			if (self.get(fieldname) or "").strip().lower() != "yes":
				label = frappe.get_meta(self.doctype).get_label(fieldname)
				frappe.throw(f'{label}: please type "Yes" to confirm agreement.')

	def set_legacy_field_values(self):
		self.what_is_your_motivation_for_applying_for_this_training = self.motivation_for_applying
		self.what_are_your_expectations_for_this_training = self.expectations_for_training
		self.when_and_how_did_you_become_a_follower_of_christ = self.became_follower_of_christ
		self.what_are_the_things_the_lord_is_teaching_you_at_the_moment = self.lord_teaching_now
		self.have_you_answered_gods_call_to_discipleship = self.discipleship_calling
		self.small_text_rdfp = self.hobbies


# endregion APPLICATION
