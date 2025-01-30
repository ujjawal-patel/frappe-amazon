import frappe


def get_context(context):
    cart = frappe.get_all(
        "Cart", filters={"user": frappe.session.user}, fields=["name"]
    )
    cart_doc = frappe.get_doc("Cart", cart[0].get("name"))
    checkout = frappe.get_all(
        "Checkout", filters={"user": frappe.session.user}, fields="*"
    )
    if checkout:
        checkout_doc = frappe.get_doc("Checkout", checkout[0].get("name"))
    else:
        checkout_doc = None
    context["cart"] = cart[0]
    context["items"] = cart_doc
    context["checkout"] = checkout_doc

    return context
