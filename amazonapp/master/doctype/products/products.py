# Copyright (c) 2025, Ujjawal and contributors
# For license information, please see license.txt

# import frappe
from frappe.website.website_generator import WebsiteGenerator

class Products(WebsiteGenerator):
    pass


import frappe

@frappe.whitelist()
def get_products(category=None):
    if category:
        # Fetch all products with required fields
        products = frappe.get_all("Products", fields=["*"], filters={"category": category})
    else:
        # Fetch all products with required fields
        products = frappe.get_all("Products", fields=["*"])

    # Fetch additional details (brand, model, etc.) for each product
    for product in products:
        if product.product_details:
            if product.category == "Electronics":
                electronics_details = frappe.get_doc("Electronics", product["product_details"])
                
                product["brand"] = electronics_details.brand
                product["model"] = electronics_details.model
                product["colour"] = electronics_details.colour
            elif product.category == "Clothing":
                clothing_details = frappe.get_doc("Clothing", product["product_details"])
                
                product["brand"] = clothing_details.brand
                product["material"] = clothing_details.material
                product["colour"] = clothing_details.colour
                product["size"] = clothing_details.size
            
    return products

@frappe.whitelist()
def get_product_details(product_name):
    try:
        product = frappe.get_doc("Products", product_name)
        if not product:
            return {"message": "Product not found"}
        
        product_details = {
            "name": product.name1,
            "price": product.price,
            "description": product.descreption,
            "category": product.category
        }
        
        if product.category == "Electronics":
            electronics_details = frappe.get_doc("Electronics", product.product_details)
            if not electronics_details:
                return {"message": "Electronics details not found"}
            
            product_details.update({
                "brand": electronics_details.brand,
                "model": electronics_details.model,
                "colour": electronics_details.colour,
                "storage": electronics_details.storage,
                "ram": electronics_details.ram,
                "warranty": electronics_details.warranty
            })
        elif product.category == "Clothing":
            clothing_details = frappe.get_doc("Clothing", product.product_details)
            if not clothing_details:
                return {"message": "Clothing details not found"}
            
            product_details.update({
                "brand": clothing_details.brand,
                "material": clothing_details.material,
                "colour": clothing_details.colour,
                "size": clothing_details.size
            })
        
        return product_details
    except Exception as e:
        logging.error(f"Error retrieving product details: {e}")
        return {"message": "Error fetching product details"}