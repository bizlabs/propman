// Copyright (c) 2024, Bizlabs and contributors
// For license information, please see license.txt

frappe.ui.form.on("daily process run", {
	refresh(frm) {

            frm.add_custom_button(__('Run Process'), function(){

                frappe.call({
                    method: "propman.propman.doctype.daily_process_run.daily_process_run.manual_run",
                    callback: function(response) {
                        // Handle the response here
                    }
                });
                
            }, __("Test"));

	},
});
