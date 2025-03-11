# Odoo Discount Constraints

## Overview
This module enhances discount management in Odoo by implementing constraints on discount values based on product pricing rules. It ensures accurate and controlled discounting across all Odoo editions (Community, Enterprise, and Odoo.sh).

## Key Features
✅ Automatically applies default discounts based on the product's pricelist.
✅ Ensures discounts remain within predefined limits.
✅ Implements real-time validation using `onchange` methods.
✅ Enforces strict constraints at the database level.
✅ Enhances accuracy and prevents unauthorized discounting.

## Methods Explained
### 🔄 `_onchange_field`
Triggered when `product_id` or `order_id.pricelist_id` changes, it:
- Fetches the corresponding pricelist item.
- Sets the default discount if none is provided.
- Ensures the discount falls within the defined range.
- Raises a `UserError` if the discount is invalid.

### ✅ `_check_discount_limits`
A constraint method that:
- Ensures the applied discount is within the allowed limits.
- Raises a `ValidationError` if the discount is out of range.
- Guarantees compliance with pricing policies.

## Installation Guide
1. Copy the module to your Odoo addons directory.
2. Restart the Odoo server.
3. Install the module from the Odoo Apps menu.

## How to Use
1. Navigate to the **Sales Order** form.
2. Select a **product** with an assigned **pricelist**.
3. The system will automatically apply and validate the discount.
4. If the discount is out of range, a warning will be displayed.

## Compatibility
🔹 Odoo **Community, Enterprise, and Odoo.sh**
🔹 Compatible with **Sales and Product modules**

## Author
👤 **Osama Nadeem**
📩 For support, suggestions, or contributions, feel free to reach out!

