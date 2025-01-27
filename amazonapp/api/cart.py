import frappe

@frappe.whitelist()
def get_cart(user):
    return frappe.get_all("Cart", filters={"user": user}, fields=["*"])

@frappe.whitelist()
def get_cart_count():
  user= frappe.session.user
  try:
    cart = frappe.get_doc("Cart", {"user": user})
    if cart:
      return len(cart.items)
    else:
      return 0
  except Exception as e:
    frappe.log_error(e)
    return None

@frappe.whitelist()
def add_to_cart(name):
    user = frappe.session.user

    # Find or create an incomplete cart for the user
    cart = frappe.get_all("Cart", filters={"user": user, "is_completed": False}, fields=["name"])
    if cart:
        cart_name = cart[0].name
        
    else:
        cart_name= frappe.get_doc({
        "doctype": "Cart", 
        "user": user,
        "is_completed": False, 
        "total_items": 0, 
        "total_amount": 0
    }).insert().name

    # Check if the item already exists in the cart
    existing_item = frappe.get_all("Cart Items", filters={"parent": cart_name, "item": name}, fields=["name", "quantity"], limit=1)
    if existing_item:
        frappe.db.set_value("Cart Items", existing_item[0].name, "quantity", existing_item[0].quantity + 1)
    else:
        frappe.get_doc({
            "doctype": "Cart Items", 
            "parent": cart_name, 
            "parenttype": "Cart", 
            "parentfield": "items", 
            "item": name, 
            "quantity": 1
        }).insert()

    # Calculate total items and amount
    cart_items = frappe.get_all("Cart Items", filters={"parent": cart_name}, fields=["quantity", "price"])
    total_items = sum(item.quantity for item in cart_items)
    total_amount = sum(item.quantity * item.price for item in cart_items)

    # Update the Cart document with the new totals
    frappe.db.set_value("Cart", cart_name, {"total_items": total_items, "total_amount": total_amount})
    frappe.db.commit()

    return {"status": "success", "message": "Item added to cart", "cart": cart_name}

@frappe.whitelist()
def remove_item_from_cart(item_name):
    try:
        cart = frappe.get_doc("Cart", {"owner": frappe.session.user})
        cart.items = [item for item in cart.items if item.item != item_name]
        cart.total_amount = sum(item.price * item.quantity for item in cart.items)
        cart.total_items = sum(item.quantity for item in cart.items)
        cart.save()
        frappe.db.commit()
        return {"success": True, "new_total": cart.total_amount, "new_total_items": cart.total_items}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Failed to remove item from cart")
        return {"success": False, "message": "Failed to remove item from cart."}