Odoo Sale Order Discount Module
Overview

This module enhances discount management in Odoo by providing a wizard-based discount selection system and implementing constraints on discount values based on product pricing rules. It ensures accurate and controlled discounting across all Odoo editions (Community, Enterprise, and Odoo.sh).
Key Features
Wizard-Based Discount Management

✅ Button in Sale Order Line Tree View: Opens a wizard for discount management.
✅ Create, Edit, or Select Discounts: Manage discounts directly within the wizard.
✅ New Discount Management Menu: Allows users to modify and manage discounts separately.
Discount Constraints & Pricelist Integration

✅ Automatically applies default discounts based on the product's pricelist.
✅ Ensures discounts remain within predefined limits to prevent unauthorized discounting.
✅ Implements real-time validation using onchange methods.
✅ Enforces strict constraints at the database level for accurate discounting.
Methods Explained
🔄 _onchange_field

Triggered when product_id or order_id.pricelist_id changes, it:

    Fetches the corresponding pricelist item.

    Sets the default discount if none is provided.

    Ensures the discount falls within the defined range.

    Raises a UserError if the discount is invalid.

✅ _check_discount_limits

A constraint method that:

    Ensures the applied discount is within the allowed limits.

    Raises a ValidationError if the discount is out of range.

    Guarantees compliance with pricing policies.

Installation Guide

    Copy the module to your Odoo addons directory.

    Restart the Odoo server.

    Install the module from the Odoo Apps menu.

How to Use

    Navigate to the Sales Order form.

    Select a product with an assigned pricelist.

    The system will automatically apply and validate the discount.

    If the discount is out of range, a warning will be displayed.

Compatibility

🔹 Odoo Community, Enterprise, and Odoo.sh
🔹 Works with Sales and Product modules
Author

👤 Osama Nadeem
📩 For support, suggestions, or contributions, feel free to reach out!
