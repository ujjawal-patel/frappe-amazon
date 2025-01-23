import frappe


def get_context(context):
    cart= frappe.get_all("Cart",filters={"user":frappe.session.user,"is_completed": False },fields="*")
    cart_items = frappe.get_all("Cart Items", filters={"parent": cart[0].name}, fields="*")
    context["cart"] = cart[0]
    context["items"]= cart_items
    context["user"]=frappe.session.user
    return context


    