app_name = "propman"
app_title = "Propman"
app_publisher = "Bizlabs"
app_description = "Property Management"
app_email = "doug@bizlabs.org"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/propman/css/propman.css"
# app_include_js = "/assets/propman/js/propman.js"

# include js, css files in header of web template
# web_include_css = "/assets/propman/css/propman.css"
# web_include_js = "/assets/propman/js/propman.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "propman/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "propman/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "propman.utils.jinja_methods",
# 	"filters": "propman.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "propman.install.before_install"
# after_install = "propman.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "propman.uninstall.before_uninstall"
# after_uninstall = "propman.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "propman.utils.before_app_install"
# after_app_install = "propman.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "propman.utils.before_app_uninstall"
# after_app_uninstall = "propman.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "propman.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
# 	}
# }

fixtures = [
    {"dt": "Workflow", "filters": [
        ["name", "=", "Lease Lifecycle"]
    ]},
    {"dt": "Workflow State", "filters": [
        ["workflow_state_name", "in", [
            "Renewal in Que",
            "Renewal needed",
            "Moveout complete",
            "Moveout vacated",
            "Moveout notice received",
            "Renewal received",
            "Renewal sent",
            "Archived",
            "Active",
            "Draft"
        ]]
    ]},
    {"dt": "Workflow Transition", "filters": [
        ["parent", "=", "Lease Lifecycle"]
    ]},
    {"dt": "Workflow Document State", "filters": [
        ["parent", "=", "Lease Lifecycle"]
    ]},
    {"dt": "Workflow Action Master", "filters": [
        ["workflow_action_name", "in", [
            "Start new lease",
            "Reset",
            "Archive",
            "Send renewal",
            "Finish moveout",
            "Moveout vacate",
            "Start moveout",
            "Start Renew",
            "Inspect",
            "Receive renewal"
        ]]
    ]},
    {"dt": "Accounting Dimension", "filters": [
        ["dimension_name", "in", ["lease", "building"]]
    ]}
]


# Scheduled Tasks
# ---------------

scheduler_events = {
	# "all": [
    #     "propman.propman.doctype.daily_process_run.daily_process_run.manual_run"
	# ],
	# "daily": [
	# 	"propman.tasks.daily"
	# ],
    "cron": {
        "0 1 * * *": [
            "propman.tasks.daily" # @ 1am
        ],
    },
	# "hourly": [
	# 	"propman.tasks.hourly"
	# ],
	# "weekly": [
	# 	"propman.tasks.weekly"
	# ],
	# "monthly": [
	# 	"propman.tasks.monthly"
	# ],
}

# Testing
# -------

# before_tests = "propman.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "propman.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "propman.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["propman.utils.before_request"]
# after_request = ["propman.utils.after_request"]

# Job Events
# ----------
# before_job = ["propman.utils.before_job"]
# after_job = ["propman.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"propman.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

