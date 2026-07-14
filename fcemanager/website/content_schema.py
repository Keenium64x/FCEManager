"""Human-facing schema and approved defaults for flagship website content."""

from typing import Any


# =============================================================================
# region WEBSITE CONTENT SCHEMA
# =============================================================================


def field(
	key: str,
	label: str,
	default: str,
	section: str,
	fieldtype: str = "Data",
	description: str = "",
) -> dict[str, Any]:
	return {
		"fieldname": key,
		"label": label,
		"default": default,
		"section": section,
		"fieldtype": fieldtype,
		"description": description,
	}


PAGE_SCHEMAS: dict[str, dict[str, Any]] = {
	"global": {
		"label": "Whole website",
		"route": "/",
		"description": "Shared wording and contact details used across the header and footer.",
		"fields": [
			field("site.vision", "Vision statement", "Jesus Christ, making disciples through us, worldwide.", "Identity"),
			field("site.tagline", "Organisation tagline", "Making a Difference through Christ-centred Education and Training", "Identity"),
			field("site.support_place", "Support office location", "Pringle Bay, South Africa", "Contact details"),
			field("site.support_email", "Public email", "info@fce.org.za", "Contact details"),
			field("site.support_phone", "Public phone", "+27 28 125 0163", "Contact details"),
			field("footer.invitation", "Footer invitation", "Come and join us in the journey", "Footer"),
			field("footer.history", "Footer history line", "Serving through discipleship, education and training since 1990.", "Footer"),
		],
	},
	"home": {
		"label": "Homepage",
		"route": "/",
		"description": "The main public landing page and its conversion journey.",
		"fields": [
			field("hero.kicker", "Small heading", "Foundation for Cross-cultural Education", "Hero"),
			field("hero.line_1", "Headline line 1", "Jesus Christ,", "Hero"),
			field("hero.line_2", "Headline line 2", "making disciples", "Hero"),
			field("hero.line_3", "Headline line 3", "through us, worldwide.", "Hero"),
			field("hero.copy", "Introduction", "Come and join us in the journey. Through Christ-centred education and training, people are equipped to follow Jesus and impact families, communities and nations.", "Hero", "Small Text"),
			field("hero.image", "Hero image", "/assets/fcemanager/fce-website/media/home-hero.webp", "Hero", "Attach Image"),
			field("hero.primary_label", "Primary button", "Explore training", "Hero actions"),
			field("hero.primary_url", "Primary button destination", "/training", "Hero actions"),
			field("hero.secondary_label", "Secondary button", "Find your place", "Hero actions"),
			field("hero.secondary_url", "Secondary button destination", "/get-involved", "Hero actions"),
			field("journey.eyebrow", "Small heading", "A journey worth taking", "Journey invitation"),
			field("journey.title", "Heading", "Faith becomes visible when it begins to move.", "Journey invitation"),
			field("journey.copy", "Paragraph", "FCE does not invite people to watch mission from a distance. It forms disciples who live the truth, grow in community and take a faithful next step into God’s world.", "Journey invitation", "Small Text"),
			field("paths.eyebrow", "Small heading", "Your place in the story", "Participation journey"),
			field("paths.title", "Heading", "From knowing God to making Him known.", "Participation journey"),
			field("paths.copy", "Paragraph", "Discipleship moves outward. Follow the journey from formation, to community, to faithful participation in the mission.", "Participation journey", "Small Text"),
			field("story.caption", "Image caption", "Formation happens in life together.", "FCE story"),
			field("story.eyebrow", "Small heading", "Who we are", "FCE story"),
			field("story.title", "Heading", "Discipleship is not one programme. It is the life of FCE.", "FCE story"),
			field("story.copy", "Paragraph", "With a unique emphasis on discipleship and leadership, FCE develops each participant as a whole person. Character development and life skills are integrated through transformation and renewal of the mind.", "FCE story", "Small Text"),
			field("map.eyebrow", "Small heading", "One mission, many places", "Locations map"),
			field("map.title", "Heading", "Explore the FCE network.", "Locations map"),
			field("map.copy", "Paragraph", "Select a centre to meet the community, understand its focus and find a direct contact.", "Locations map", "Small Text"),
			field("prayer.eyebrow", "Small heading", "A daily rhythm of prayer", "Prayer invitation"),
			field("prayer.title", "Heading", "One community. One request. Every day of the month.", "Prayer invitation"),
			field("prayer.copy", "Paragraph", "Receive the FCE Prayer Calendar and stand with people, training and ministries across the network.", "Prayer invitation", "Small Text"),
			field("prayer.button", "Button label", "Request the prayer calendar", "Prayer invitation"),
		],
	},
	"training": {
		"label": "Training",
		"route": "/training",
		"description": "DMT explanation and application wording. Dates come from DMT Periods.",
		"fields": [
			field("hero.eyebrow", "Small heading", "The heartbeat of FCE", "Hero"),
			field("hero.title", "Heading", "Discipleship Mission Training", "Hero"),
			field("hero.copy", "Introduction", "Root your faith in the Bible, grow in a personal relationship with God and be equipped to disciple the nations.", "Hero", "Small Text"),
			field("hero.image", "Hero image", "/assets/fcemanager/fce-website/media/training-hero.webp", "Hero", "Attach Image"),
			field("intro.eyebrow", "Small heading", "More than a course", "Training introduction"),
			field("intro.title", "Heading", "It is not about where God fits into your story, but where you fit into God’s story.", "Training introduction"),
			field("intro.copy", "Paragraph", "DMT turns to God, His Word and His design for every sphere of life. Practical experiential learning invites a response: hear and do the truth, follow Jesus, walk in the Spirit and become a blessing to others.", "Training introduction", "Small Text"),
			field("pathways.eyebrow", "Small heading", "Training pathways", "Training pathways"),
			field("pathways.title", "Heading", "One discipleship journey, different depths.", "Training pathways"),
			field("pathways.copy", "Paragraph", "Choose the pathway that matches your experience, calling and next responsibility.", "Training pathways", "Small Text"),
			field("opportunities.eyebrow", "Small heading", "Upcoming DMT", "Upcoming training"),
			field("opportunities.title", "Heading", "Find the place and season for your next step.", "Upcoming training"),
			field("opportunities.copy", "Paragraph", "Current training periods are published directly by the FCE team. Choose a season, explore its locations and begin your application.", "Upcoming training", "Small Text"),
			field("apply.eyebrow", "Small heading", "Ready to apply?", "Application"),
			field("apply.title", "Heading", "Begin your DMT journey.", "Application"),
			field("apply.copy", "Paragraph", "Complete the secure FCE application form. Your submission goes directly to the team managing the training intakes above.", "Application", "Small Text"),
			field("apply.button", "Button label", "Start your application", "Application"),
		],
	},
	"about": {
		"label": "About FCE", "route": "/about", "description": "Identity, history, values and statement-of-faith framing.",
		"fields": [
			field("hero.eyebrow", "Small heading", "Who we are", "Hero"), field("hero.title", "Heading", "Jesus Christ, making disciples through us, worldwide.", "Hero"), field("hero.copy", "Introduction", "The Foundation for Cross-cultural Education is an international, inter-denominational, multi-ethnic, non-profit mission organisation.", "Hero", "Small Text"), field("hero.image", "Hero image", "/assets/fcemanager/fce-website/media/about-lens.webp", "Hero", "Attach Image"),
			field("story.eyebrow", "Small heading", "Our story", "History"), field("story.title", "Heading", "Equipping people to impact the nations since 1990.", "History"),
			field("values.eyebrow", "Small heading", "Discipleship is our DNA", "Values"), field("values.title", "Heading", "Follow Jesus. Be transformed. Go into the world.", "Values"), field("values.copy", "Paragraph", "These commitments shape FCE’s training, community life and service across every location.", "Values", "Small Text"),
			field("quote.text", "Featured quotation", "When God loved, He loved the world. God’s vision is a world vision and this is the vision He wants us to cherish.", "Featured quotation", "Small Text"), field("quote.copy", "Supporting paragraph", "FCE goes into the world to serve the body of Christ, train students for missions, establish a network of believers and prepare the church as the Bride of Christ.", "Featured quotation", "Small Text"),
			field("faith.eyebrow", "Small heading", "Statement of faith", "Statement of faith"), field("faith.title", "Heading", "The faith beneath the work.", "Statement of faith"), field("faith.copy", "Paragraph", "FCE is an international, inter-denominational, multi-ethnic, non-profit Christ-centred mission organisation.", "Statement of faith", "Small Text"),
		],
	},
	"locations": {"label": "Locations", "route": "/locations", "description": "Framing around the FCE location directory.", "fields": [field("hero.eyebrow", "Small heading", "Where we serve", "Hero"), field("hero.title", "Heading", "FCE communities across southern Africa", "Hero"), field("hero.copy", "Introduction", "Training centres, schools, camps and support teams carry one shared discipleship vision in distinct local settings.", "Hero", "Small Text"), field("hero.image", "Hero image", "/assets/fcemanager/fce-website/media/training-community.webp", "Hero", "Attach Image"), field("list.eyebrow", "Small heading", "Our locations", "Location list"), field("list.title", "Heading", "9 communities and contact points", "Location list"), field("list.copy", "Paragraph", "Connect directly with a location for training, camps, teacher development, local ministry or support.", "Location list", "Small Text")]},
	"get-involved": {"label": "Get involved", "route": "/get-involved", "description": "Prayer, volunteering, giving and participation framing.", "fields": [field("hero.eyebrow", "Small heading", "Get involved", "Hero"), field("hero.title", "Heading", "Pray. Serve. Give. Go.", "Hero"), field("hero.copy", "Introduction", "Stand with FCE communities through prayer, practical service, cross-cultural outreach and support for current projects.", "Hero", "Small Text"), field("hero.image", "Hero image", "/assets/fcemanager/fce-website/media/volunteer.webp", "Hero", "Attach Image"), field("ways.eyebrow", "Small heading", "Ways to join", "Ways to join"), field("ways.title", "Heading", "Find a practical next step.", "Ways to join"), field("ways.copy", "Paragraph", "Begin where your conviction, capacity and FCE’s current needs meet.", "Ways to join", "Small Text"), field("volunteer.title", "Heading", "Serve in a cross-cultural community.", "Volunteer feature"), field("volunteer.copy", "Paragraph", "FCE welcomes enquiries from people looking for volunteer and outreach opportunities. Share your skills, location and availability so the team can help you explore a suitable place to serve.", "Volunteer feature", "Small Text"), field("prayer.title", "Heading", "Stay connected to the daily life of the mission.", "Prayer feature"), field("prayer.copy", "Paragraph", "Receive the monthly FCE Prayer Calendar with one prayer request for each day.", "Prayer feature", "Small Text")]},
	"projects": {"label": "Projects", "route": "/projects", "description": "Project-support framing. Individual project entries remain structured source content for now.", "fields": [field("hero.eyebrow", "Small heading", "Practical support", "Hero"), field("hero.title", "Heading", "Help FCE accomplish practical projects in 2026.", "Hero"), field("hero.copy", "Introduction", "FCE’s practical projects give people a direct way to stand with the mission through advice, on-site help or financial support.", "Hero", "Small Text"), field("hero.image", "Hero image", "/assets/fcemanager/fce-website/media/project-education.webp", "Hero", "Attach Image"), field("support.eyebrow", "Small heading", "Three ways to help", "Project support"), field("support.title", "Heading", "Give advice. Serve practically. Support financially.", "Project support"), field("support.copy", "Paragraph", "Contact the responsible team before committing support so FCE can share the latest scope and need.", "Project support", "Small Text"), field("archive.title", "Archive heading", "Education and community transformation remain part of the story.", "Archive"), field("archive.copy", "Archive paragraph", "The source website includes past records for teacher-development work in Ethiopia and primary education support in Zambia. Ask FCE for verified reports and current outcomes.", "Archive", "Small Text")]},
	"resources": {"label": "Stories and resources", "route": "/resources", "description": "Resource-library framing.", "fields": [field("hero.eyebrow", "Small heading", "Stories and resources", "Hero"), field("hero.title", "Heading", "Keep learning. Keep praying. Remember the journey.", "Hero"), field("hero.copy", "Introduction", "Current resources and preserved organisational records remain discoverable without competing with FCE’s primary action pathways.", "Hero", "Small Text"), field("hero.image", "Hero image", "/assets/fcemanager/fce-website/media/prayer.webp", "Hero", "Attach Image"), field("library.eyebrow", "Small heading", "Resource library", "Library"), field("library.title", "Heading", "Useful now. Preserved for context.", "Library"), field("library.copy", "Paragraph", "Current resources lead to an action; archival records explain where FCE has been and are clearly marked when facts need verification.", "Library", "Small Text")]},
	"contact": {"label": "Contact", "route": "/contact", "description": "Contact-page framing; shared contact details are under Whole website.", "fields": [field("hero.eyebrow", "Small heading", "Contact FCE", "Hero"), field("hero.title", "Heading", "A conversation is a good place to begin.", "Hero"), field("hero.copy", "Introduction", "Ask about training, volunteering, prayer, a location or practical support. The support office will connect you with the right team.", "Hero", "Small Text"), field("hero.image", "Hero image", "/assets/fcemanager/fce-website/media/location-pringle.webp", "Hero", "Attach Image"), field("form.eyebrow", "Small heading", "Send an enquiry", "Enquiry form"), field("form.title", "Heading", "What would you like to know?", "Enquiry form"), field("form.copy", "Paragraph", "This first implementation opens your email client so FCE receives the message directly. A hosted form endpoint can replace it without changing the design.", "Enquiry form", "Small Text")]},
	"privacy": {"label": "Privacy policy", "route": "/privacy", "description": "Privacy-page introduction and review notice.", "fields": [field("hero.eyebrow", "Small heading", "Organisation", "Hero"), field("hero.title", "Heading", "Privacy and personal data.", "Hero"), field("hero.copy", "Introduction", "A preserved and clarified overview of FCE’s public privacy policy, last updated on the source site on 11 July 2021.", "Hero", "Small Text"), field("notice", "Review notice", "This redesign preserves the substance of the source policy while making it easier to read. Before production launch, legal review should reconcile the final hosting, analytics, forms and cookie-consent implementation with the complete policy.", "Policy notice", "Small Text")]},
}

SEO_DEFAULTS = {
	"home": ("FCE — Making disciples worldwide", "Foundation for Cross-cultural Education — Jesus Christ, making disciples through us, worldwide."),
	"about": ("About FCE", "Discover FCE’s identity, history, discipleship vision and statement of faith."),
	"training": ("Discipleship Mission Training", "Explore FCE Discipleship Mission Training pathways, current dates and application information."),
	"locations": ("FCE locations", "Find FCE communities, training centres and direct contact details across southern Africa."),
	"get-involved": ("Get involved with FCE", "Pray, volunteer, serve and support the work of FCE."),
	"projects": ("FCE projects", "Explore practical ways to support FCE projects and community transformation."),
	"resources": ("Resources and archive — FCE", "Find FCE prayer, training, education and historical resources."),
	"contact": ("Contact FCE", "Contact the FCE support office about training, service, prayer, projects or locations."),
	"privacy": ("Privacy policy — FCE", "Read how FCE handles personal information and website data."),
}

for _page_key, (_seo_title, _seo_description) in SEO_DEFAULTS.items():
	PAGE_SCHEMAS[_page_key]["fields"].extend(
		[
			field("seo.title", "Browser and search title", _seo_title, "Search and sharing"),
			field("seo.description", "Search and sharing description", _seo_description, "Search and sharing", "Small Text"),
		]
	)


ROUTE_TO_PAGE = {schema["route"]: key for key, schema in PAGE_SCHEMAS.items() if key != "global"}


def get_page_schema(page_key: str) -> dict[str, Any]:
	if page_key not in PAGE_SCHEMAS:
		raise KeyError(page_key)
	return PAGE_SCHEMAS[page_key]


def get_defaults(page_key: str) -> dict[str, str]:
	return {item["fieldname"]: item["default"] for item in get_page_schema(page_key)["fields"]}


def validate_content(page_key: str, values: dict[str, Any]) -> dict[str, str]:
	allowed = {item["fieldname"] for item in get_page_schema(page_key)["fields"]}
	return {key: str(value or "") for key, value in values.items() if key in allowed}


# endregion WEBSITE CONTENT SCHEMA
