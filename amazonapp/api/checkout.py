import frappe
    
@frappe.whitelist()
def create_checkout():
    try:
        # Step 1: Fetch the user's cart items
        cart = frappe.get_all("Cart", filters={"user": frappe.session.user}, fields=["name"])
        cart_doc = frappe.get_doc("Cart",cart[0].get("name"))
       
        if not cart:
            return {"success": False, "message": "Your cart is empty."}


        is_checkout = frappe.get_all("Checkout",filters={"user":frappe.session.user,"order_created":False})
        if not is_checkout:      # # Step 2: Create a new Checkout document
            checkout_doc = frappe.get_doc({
                "doctype": "Checkout",
                "user": frappe.session.user,
                "cart": cart_doc.name,  
                "address": "",  
                "payment": ""  
            })


        # Save the Checkout document
            checkout_doc.insert()
            frappe.db.commit()

        

        return {
            "success": True,
            "message": "Checkout created successfully.",
            "checkout_id": "checkout_doc.name",
            "cart": "cart_doc",
            
        }

    except Exception as e:
        print(e,"************************")
        frappe.log_error(frappe.get_traceback(), "Checkout Creation Error")
        return {"success": False, "message": str(e)}

@frappe.whitelist()

def create_order(user, tracking_id):
    try:

        # Step 2: Fetch the user's checkout details
        checkout = frappe.get_all("Checkout", filters={"user": user}, fields="*")

        if not checkout:
            return {"success": False, "message": "No checkout found for this user."}

        checkout_doc = frappe.get_doc("Checkout", checkout[0].get("name"))

        # Step 3: Create a new Orders document
        order_doc = frappe.get_doc({
            "doctype": "Orders",
            "user": user,
            "checkout": checkout[0].get("name"),
            "tracking_id": tracking_id,
            "status": ""
        })
        order_doc.insert()
        frappe.db.commit()

        cart_doc = frappe.get_doc("Cart", checkout_doc.cart)
        cart_doc.is_completed = 1 
        cart_doc.save()
        checkout_doc.order_created = 1
        checkout_doc.save()
        frappe.db.commit()

        return {
            "success": True,
            "message": "Order created successfully.",
            "order_id": order_doc.name,
        }

    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Order Creation Error")
        return {"success": False, "message": str(e)}


