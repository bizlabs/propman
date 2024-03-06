// Copyright (c) 2024, Bizlabs and contributors
// For license information, please see license.txt

// frappe.ui.form.on('inv_schedule', {
// 	inv_schedule_add: function(frm) {
// 		var row = cur_frm.doc.items.length - 1;
// 		if (row == 0) {
// 			var last_date = frm.doc.last_date;
// 			var next_date = frm.doc.next_date;
// 			var period = frm.doc.period;
// 			var increment = frm.doc.increment;
// 			var amount = frm.doc.rent;
// 			var desc = "Rent";
// 			var account = xxx;
// 			var inv_status = xxx;

// 			frappe.model.set_value(cur_frm.doc.items[row].doctype, cur_frm.doc.items[row].name, "date", today);
// 		} 
// 	},
// 	hours: function(frm) {
// 		frappe.model.add_child(cur_frm.doc, "Time Tracking Table", "time_tracking_table");
// 	}

frappe.ui.form.on('inv schedule', {
    inv_schedule_add: function(frm, cdt, cdn) {
    item = locals[cdt][cdn];
    item.isnew = true;
    frm.refresh_field('inv_schedule');
   },
    "next_date": function(frm, cdt, cdn) {
    item = locals[cdt][cdn];
    item.isupdate = true;
    frm.refresh_field('inv_schedule');
   },
   "type": function(frm, cdt, cdn) {
   item = locals[cdt][cdn];
   
   frappe.call({
        method: "frappe.client.get",
        args: {doctype: "property manager settings", name: "property manager settings"},
        callback: function(r) {
            if(r.message){
                settings = r.message;          
                types = {
                    'Rent':settings.rent_income_acct,
                    'Deposit':settings.sec_dep_acct,
                    'Repairs':settings.tenant_charge_acct,
                }

                for (acct of settings.default_account) {
                    types[acct.charge_type] = acct.default_account;
                }
                // cur_frm.fields_dict.inv_schedule.grid.update_docfield_property("type","options",[""].concat(types))
                item.account = types[item.type];
                frm.refresh_field('inv_schedule');
            }
        }
    })
    
  },
   form_render: function(frm, cdt, cdn) {
   item = locals[cdt][cdn];
   if (item.desc == "Rent") {
    frappe.throw("Rent can only be changed from the 'Current Lease Parameters' in the lease form")
   }
//    frm.refresh_field('inv_schedule');
  },
});

// the following is for actions that only happen on transition to new workflow state.
// use match statement in lease.py to run workflow state specific code on every validation 
frappe.ui.form.on("lease", {
    after_workflow_action: function (frm) {
        switch (frm.doc.workflow_status) {
            case "Draft":
				frm.doc.auto_rent = false
				frm.doc.inv_status = "draft"
                break;
            case "Active":
				frm.doc.auto_rent = true
				frm.doc.inv_status = "submitted"
                frappe.msgprint("Here are draft invoice (if any) that you may want to submit now.  Press back button in browswer to return to the lease")
                // frappe.set_route("List", "Sales Invoice",{'lease':frm.doc.name, 'status':"Draft"});
                break;
            case "renew":
                break;
            case "Moveout complete":
                frm.doc.inv_status = 'draft';
                break;
            default:
        }
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
            // set options from settings xxx

            frappe.call(
                {
                    method: "frappe.client.get",
                    args: {doctype: "property manager settings", name: "property manager settings"},
                    callback: function(r) {
                        if(r.message){
                            settings = r.message;          
                            types = ['Rent','Deposit','Repairs','Other','Credit']
                            
                            for (acct of settings.default_account) {
                                types.push(acct.charge_type);
                            }
                            cur_frm.fields_dict.inv_schedule.grid.update_docfield_property("type","options",[""].concat(types))
                        }
                    }
                })
                
        end_date = new Date(frm.doc.lease_end);
        today = new Date();
        let delta = Math.round( (today.getTime() - end_date.getTime())/(1000*3600*24) );
        var status = "Current", textcolor = 'white', bgcolor='green';
        if (delta > -45) {
            textcolor = 'black'; bgcolor='yellow';
        }
        if (delta > -30) {
            textcolor = 'black'; bgcolor='orange';
        }
        status = "Expires " + -delta + " days"; 
        if (delta >= 0) {
            status = "Expired"; textcolor = 'white'; bgcolor='red';
        }


        frm.add_custom_button(__(status), function() {
            //do something here when button clicked
            // perhaps provide info re expiring lease? or ask user if they want to start renewal?
        }).css({"color":textcolor, "background-color": bgcolor, "font-weight": "800"});

        frm.add_custom_button(__(frm.doc.workflow_status), function() {
            //do something here when button clicked
        }).css({"color":"black", "background-color": "#73C2FB", "font-weight": "800"});

        frm.add_custom_button(__("Charges"), function() {
            // cnt = frappe.db.count("Sales Invoice");  # this just returning a promise
            frappe.set_route("List", "Sales Invoice",{'lease':frm.doc.name});
        }).css({"color":"black", "background-color": "#73C2FB", "font-weight": "800"});

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
    'next_date': function(frm) {
        copy_rent_schedule (frm);
    },
    'period': function(frm) {
        copy_rent_schedule (frm);
    },
    'increment': function(frm) {
        copy_rent_schedule (frm);
    },
    'rent': function(frm) {
        copy_rent_schedule (frm);
    },
    'deposit': function(frm) {
        update_deposit_ledger (frm);
    },
    'inv_status': function(frm) {
        copy_rent_schedule (frm);
    },


    onload: function(frm){
        copy_rent_schedule(frm);
    },

    
});

function update_deposit_ledger(frm) {
    rent_row = frm.doc.deposit_ledger.findIndex((item) => item.desc == "Original deposit");
    if (rent_row < 0) {
        frappe.model.get_value('property manager settings', 'property manager settings', 'settings', function(settings) {
            frm.add_child('deposit_ledger', {
                due_date: frm.doc.lease_start,
                status: "Draft",
                amount: frm.doc.deposit,
                desc: "Original deposit",
                account: settings.sec_dep_acct,
            });
            frm.refresh_field('deposit_ledger');
        });
    }
    else {
        // update all the fields...
        // frm.doc.deposit_ledger[rent_row].next_date = frm.doc.next_date; 
    }
}

function copy_rent_schedule (frm) {

    rent_row = frm.doc.inv_schedule.findIndex((item) => item.desc == "Rent");
    if (rent_row < 0) {

        frappe.model.get_value('property manager settings', 'property manager settings', 'settings', function(settings) {
            frm.add_child('inv_schedule', {
                last_date: frm.doc.last_date,
                next_date: frm.doc.next_date,
                period: frm.doc.period,
                increment: frm.doc.increment,
                amount: frm.doc.rent,
                desc: "Rent",
                account: settings.rent_income_acct,
                inv_status: settings.default_status,
            });
            frm.refresh_field('inv_schedule');
        });
    }
    else {

        frm.doc.inv_schedule[rent_row].next_date = frm.doc.next_date; 
        frm.doc.inv_schedule[rent_row].period = frm.doc.period;
        frm.doc.inv_schedule[rent_row].increment = frm.doc.increment;
        frm.doc.inv_schedule[rent_row].amount = frm.doc.rent;
        frm.doc.inv_schedule[rent_row].inv_status = frm.doc.inv_status;
        frm.refresh_field('inv_schedule');
    }
}