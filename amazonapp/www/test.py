import frappe


def get_context(context):
    products = frappe.get_all("Products", fields=["*"])

    for product in products:
        if product.product_details:
            if product.category == "Electronics":
                electronics_details = frappe.get_doc(
                    "Electronics", product["product_details"]
                )
                product["brand"] = electronics_details.brand

            elif product.category == "Clothing":
                clothing_details = frappe.get_doc(
                    "Clothing", product["product_details"]
                )
                product["brand"] = clothing_details.brand

            elif product.category == "Stationary":
                stationary_details = frappe.get_doc(
                    "Stationary", product["product_details"]
                )
                product["brand"] = stationary_details.brand

    context["user"] = frappe.session.user
    context["products"] = products
    return context
