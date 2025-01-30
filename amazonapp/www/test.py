import frappe


def get_context(context):
    products = frappe.get_all("Products", fields=["*"])

    context["user"] = frappe.session.user
    return context
