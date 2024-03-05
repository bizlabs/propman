// Copyright (c) 2024, Bizlabs and contributors
// For license information, please see license.txt

frappe.ui.form.on("inv schedule", {
	refresh(frm) {
        frm.set_df_property('type', 'options', ['option a', 'option b']);
        frm.refresh_field('type');

	},
});
