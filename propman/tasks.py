
import frappe


frappe.utils.logger.set_log_level("DEBUG")
logger = frappe.logger("propman", allow_site=False, file_count=10)


def daily():
    proc_run = frappe.new_doc("daily process run")
    proc_run.daily_run()
    logger.debug("finish execution of daily run")