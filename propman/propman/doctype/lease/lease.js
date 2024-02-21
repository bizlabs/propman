// Copyright (c) 2024, Bizlabs and contributors
// For license information, please see license.txt

frappe.ui.form.on("lease", {

    setup: function(frm){
        frm.set_query("inv_trigger", function() {
            return {
                filters: {
                    'parent': cur_frm.docname,
                    // 'name': '6349d22970',
                }
            };
        });
    },

	refresh(frm) {

        //for testing purposes
        frm.add_custom_button(__("daily process run"), function() {

            frappe.call({
                method: "propman.propman.doctype.daily_process_run.daily_process_run.manual_run",
                callback: function(response) {
                    // Handle the response here
                }
            });
        }).css({"color":"black", "background-color": "pink", "font-weight": "800"});

        end_date = new Date(frm.doc.lease_end);
        today = new Date();
        delta = Math.round(today.getTime() - end_date.getTime())/(1000*3600*24)
        var status = "Current", textcolor = 'white', bgcolor='green';
        if (delta > -45) {
            status = "Send Renewal"; textcolor = 'black'; bgcolor='yellow';
        }
        if (delta > -30) {
            status = "Expiring soon"; textcolor = 'black'; bgcolor='orange';
        }
        if (delta >= 0) {
            status = "Expired"; textcolor = 'white'; bgcolor='red';
        }

        if (frm.doc.action_que == "Renew") {
            if (frm.doc.renewal_draft) {
                frm.add_custom_button(__("Renewal in DRAFT"), function() {
                }).css({"color":"black", "background-color": "#B2FFFF", "font-weight": "800"});
            }
            else {
                frm.add_custom_button(__("Renewal in QUE"), function() {
                }).css({"color":"white", "background-color": "blue", "font-weight": "800"});
            }
        }
        else if (frm.doc.action_que == "Moveout") {

            if (frm.doc.moveout_draft) {
                frm.add_custom_button(__("Moveout in DRAFT"), function() {
                }).css({"color":"black", "background-color": "#D8BFD8", "font-weight": "800"});
            }
            else {
                frm.add_custom_button(__("Moveout in QUE"), function() {
                }).css({"color":"white", "background-color": "purple", "font-weight": "800"});
            }
        }


        frm.add_custom_button(__(status), function() {
            frappe.prompt([
                {
                    'fieldname': 'action',
                    'fieldtype': 'Select',
                    'label': 'Select Moveout or Renew',
                    'options': ['Moveout', 'Renew'],
                    'reqd': 1
                }
            ], function(values){
                if (values.action == "Renew") {
                    frm.set_value('action_que',"Renew")
                }
                else if (values.action == "Moveout") {
                    frm.set_value('action_que',"Moveout")
                }
                // frm.call(values.action,{'arg1':"my argument"})
        
            }, 'Moveout or Renew?', 'Submit');
        }).css({"color":textcolor, "background-color": bgcolor, "font-weight": "800"});
    },

    "latefee_policy": async function(frm) {

        let lfp_doc = frm.doc.latefee_policy;
        if (lfp_doc) {
            let lfp = await frappe.db.get_doc('late fee policy', lfp_doc);
            for (let lfs of lfp.late_fee_schedule) {
                let row = frm.add_child('late_fee_schedule', {
                    'grace_per':    lfs.grace_per,
                    'repeat_per':   lfs.repeat_per,
                    'pct':          lfs.pct,
                    'flat_fee':     lfs.flat_fee,
                });
            }
        frm.refresh_field('late_fee_schedule');
        }
	},

    onload: function(frm){

    },

});
