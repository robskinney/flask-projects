from flask import Blueprint, render_template, request, redirect, url_for

from gorillacarts.lib.objects import Cart
from gorillacarts.lib.utils import getFormVariable, getIntegerFormVariable, getFloatFormVariable
from gorillacarts.lib.db import *

gorillacarts = Blueprint(
    'gorillacarts',
    __name__,
    template_folder='templates'
)

@gorillacarts.route('/', methods=['GET'])
def index():
    return render_template('gorillacarts/index.html' )

# ------------------------------------------------------------------------------------
# Customer routes
# ------------------------------------------------------------------------------------

@gorillacarts.route("/customers", methods=["GET"])
def customers():
    if request.method == "GET":
        customer_list=Cart.getAllCustomers()
        return render_template('gorillacarts/customers/index.html',customers=customer_list)

@gorillacarts.route('/customers/create', methods=['GET'])
def customers_create():
    if request.method == "GET":
        return render_template('gorillacarts/customers/create.html')
    
@gorillacarts.route("/customers/<id>/update", methods=['GET'])
def customers_update(id):
    if request.method == "GET":
        customer=getCustomerById(id)
        return render_template('gorillacarts/customers/update.html',customer=customer )

@gorillacarts.route('/api/customers/create', methods=['POST'])
def api_customers_create():
    name = request.form.get("name", 0)
    zip = request.form.get("ZIP", 0)
    telephone = request.form.get("telephone", 0)
    email = request.form.get("email", 0)
    category = request.form.get("category", 0)

    saveCustomerDB(name, zip, telephone, email, category)

    return redirect(url_for('gorillacarts.customers'))

@gorillacarts.route("/api/customers/<id>/update", methods=["POST"])
def api_customers_update(id):
    zip = getFormVariable(request,"ZIP")
    telephone = getFormVariable(request,"Telephone")
    email = getFormVariable(request,"Email")
    category = getFormVariable(request,"Category")

    updateCustomerDB(id, zip, telephone, email, category)
    
    return redirect(url_for('gorillacarts.customers'))

@gorillacarts.route("/api/customers/<id>/delete", methods=['POST', 'DELETE', 'GET'])
def api_customers_delete(id):
    genDelete_DB("Customers","CustomerID",id)
    
    return redirect(url_for('gorillacarts.customers'))

# ------------------------------------------------------------------------------------
# Product routes
# ------------------------------------------------------------------------------------

@gorillacarts.route("/products", methods=["GET"]) # Decorator
def products():
    if request.method == "GET":
        product_list=Cart.getAllProducts()
        return render_template('gorillacarts/products/index.html',products=product_list)
    
@gorillacarts.route("/products/<id>", methods=['GET'])
def products_bom(id):
    if request.method == "GET":
        bom=getBOMByProductId(id)
        return render_template('gorillacarts/products/bom.html',bom=bom)
    
# ------------------------------------------------------------------------------------
# Material routes
# ------------------------------------------------------------------------------------

@gorillacarts.route("/materials", methods=["GET"]) # Decorator
def materials():
    if request.method == "GET":
        material_list=Cart.getAllMaterials()
        return render_template('gorillacarts/materials/index.html',materials=material_list)

@gorillacarts.route('/materials/create', methods=['GET'])
def materials_create():
    if request.method == "GET":
        supplier_list=Cart.getAllSuppliers()
        return render_template('gorillacarts/materials/create.html',suppliers=supplier_list)
    
@gorillacarts.route("/materials/<id>/update", methods=['GET'])
def materials_update(id):
    if request.method == "GET":
        material=getMaterialById(id)
        return render_template('gorillacarts/materials/update.html',material=material )
    
@gorillacarts.route('/api/materials/create', methods=['POST'])
def api_materials_create():
    if request.method == "POST":
        SWPartNo = request.form.get("SWPartNo", 0)
        SupplierPartNo = request.form.get("SupplierPartNo", 0)
        SupplierID = request.form.get("SupplierID", 0)
        ProductName = request.form.get("ProductName", 0)
        Price = request.form.get("Price", 0)
        QuantityAvailable = request.form.get("QuantityAvailable", 0)

        saveMaterialDB(SWPartNo,SupplierPartNo,SupplierID,ProductName,Price,QuantityAvailable)

        return redirect(url_for('gorillacarts.materials'))
    
@gorillacarts.route("/api/materials/<id>/update", methods=["POST"])
def api_materials_update(id):
    SupplierPartNo = getFormVariable(request,"SupplierPartNo")
    SupplierID = getIntegerFormVariable(request,"SupplierID")
    ProductName = getFormVariable(request,"ProductName")
    Price = getFormVariable(request,"Price")
    QuantityAvailable = getFloatFormVariable(request,"QuantityAvailable")

    updateMaterialDB(SupplierPartNo,SupplierID,ProductName,Price,QuantityAvailable,id)
    
    return redirect(url_for('gorillacarts.materials'))

@gorillacarts.route("/api/materials/<id>/delete", methods=['POST', 'DELETE', 'GET'])
def api_materials_delete(id):
    genDelete_DB("Materials","SWPartNo",id)
    
    return redirect(url_for('gorillacarts.materials'))

# ------------------------------------------------------------------------------------
# Supplier routes
# ------------------------------------------------------------------------------------

@gorillacarts.route("/suppliers", methods=["GET"]) # Decorator
def suppliers():
    if request.method == "GET":
        supplier_list=Cart.getAllSuppliers()
        return render_template('gorillacarts/suppliers/index.html',suppliers=supplier_list)

@gorillacarts.route('/suppliers/create', methods=['GET'])
def suppliers_create():
    if request.method == "GET":
        return render_template('gorillacarts/suppliers/create.html')
    
@gorillacarts.route("/suppliers/<id>/update", methods=['GET'])
def suppliers_update(id):
    if request.method == "GET":
        supplier=getSupplierById(id)
        return render_template('gorillacarts/suppliers/update.html',supplier=supplier )
    
@gorillacarts.route('/api/suppliers/create', methods=['POST'])
def api_suppliers_create():
    if request.method == "POST":
        name = request.form.get("name", 0)
        zip = request.form.get("ZIP", 0)
        telephone = request.form.get("telephone", 0)
        email = request.form.get("email", 0)

        saveSupplierDB(name, zip, telephone, email)

        return redirect(url_for('gorillacarts.suppliers'))
    
@gorillacarts.route("/api/suppliers/<id>/update", methods=["POST"])
def api_suppliers_update(id):
    zip = getFormVariable(request,"ZIP")
    telephone = getFormVariable(request,"Telephone")
    email = getFormVariable(request,"Email")

    updateSupplierDB(zip, telephone, email, id)
    
    return redirect(url_for('gorillacarts.suppliers'))

@gorillacarts.route("/api/suppliers/<id>/delete", methods=['POST', 'DELETE', 'GET'])
def api_suppliers_delete(id):
    genDelete_DB("Suppliers","SupplierID",id)
    
    return redirect(url_for('gorillacarts.suppliers'))

# ------------------------------------------------------------------------------------
# Order routes
# ------------------------------------------------------------------------------------

@gorillacarts.route("/orders", methods=["GET"]) # Decorator
def orders():
    if request.method == "GET":
        order_list=Cart.getAllOrders()
        return render_template('gorillacarts/orders/index.html',orders=order_list)

@gorillacarts.route("/orders/<id>", methods=['GET'])
def orders_details(id):
    if request.method == "GET":
        order=getOrderById(id)
        order_details=getOrderDetailsById(id)
        return render_template('gorillacarts/orders/details.html',order=order,order_details=order_details)
    
@gorillacarts.route('/orders/create', methods=['GET'])
def orders_create():
    if request.method == "GET":
        staff_list=Cart.getAllStaff()
        customer_list=Cart.getAllCustomers()
        product_list=Cart.getAllProducts()
        return render_template('gorillacarts/orders/create.html',staff=staff_list,customers=customer_list,products=product_list)

@gorillacarts.route("/api/orders/create", methods=["GET","POST"]) # Decorator - Now
def placeorder():
    if request.method == "POST": # When you fill out the form and click SUBMIT
        # C1) Run a CLASS method called getAllMovies().  Instaniation is not needed.
        staff_list=Cart.getAllStaff()
        customer_list=Cart.getAllCustomers()
        product_list=Cart.getAllProducts()
        order_list=Cart.getAllOrders()
        material_list=Cart.getAllMaterials()
        bom_list=Cart.getAllBOMs()

        # Get the value from the form object (it is a drop down menu)
        EmployeeID = request.form.get("EmployeeID", 0)
        CustomerID = request.form.get("CustomerID", 0)
        ProductID1 = request.form.get("ProductID1", 0)
        Quantity1 = request.form.get("quantity1", 0)
        ProductID2 = request.form.get("ProductID2", 0)
        Quantity2 = request.form.get("quantity2", 0)
        ProductID3 = request.form.get("ProductID3", 0)
        Quantity3 = request.form.get("quantity3", 0)
        ProductID4 = request.form.get("ProductID4", 0)
        Quantity4 = request.form.get("quantity4", 0)
        ProductID5 = request.form.get("ProductID5", 0)
        Quantity5 = request.form.get("quantity5", 0)

        #-------------------------------------
        # 1. VERIFY IF THE PLACED ORDER DOESN'T HAVE A PRODUCT WHOSE QUANTITY IS MORE THAN 10
        #-------------------------------------
        order = {}
        if ProductID1 != "" and Quantity1 != "":
            if ProductID1 not in order.keys():
                order[ProductID1] = int(Quantity1)
            else:
                order[ProductID1] = int(order[ProductID1])+int(Quantity1)
        if ProductID2 != "" and Quantity2 != "":
            if ProductID2 not in order.keys():
                order[ProductID2] = int(Quantity2)
            else:
                order[ProductID2] = int(order[ProductID2])+int(Quantity2)
        if ProductID3 != "" and Quantity3 != "":
            if ProductID3 not in order.keys():
                order[ProductID3] = int(Quantity3)
            else:
                order[ProductID3] = int(order[ProductID3])+int(Quantity3)
        if ProductID4 != "" and Quantity4 != "":
            if ProductID4 not in order.keys():
                order[ProductID4] = int(Quantity4)
            else:
                order[ProductID4] = int(order[ProductID4])+int(Quantity4)
        if ProductID5 != "" and Quantity5 != "":
            if ProductID5 not in order.keys():
                order[ProductID5] = int(Quantity5)
            else:
                order[ProductID5] = int(order[ProductID5])+int(Quantity5)
        total = 0
        c=0
        #THROWING AN ERROR MESSAGE IF THE PLACE ORDER PAGE DID NOT HAVE ANY ORDER; THAT IS NO PRODUCT WAS PLACE
        if len(order.keys()) == 0:
            c=1
            return render_template('gorillacarts/orders/create.html',errormessage="You have no items added, try again!",staff=staff_list,customers=customer_list,products=product_list)
        #CHECK IF ANY ONE PRODUCT HAS MORE THAN 10 PEICES ORDERED
        for i in order.keys():
            if int(order[i]) > 10:
                c=1
                return render_template('gorillacarts/orders/create.html',errormessage="You have more then 10 units of an item added, try again!",staff=staff_list,customers=customer_list,products=product_list)
                break

        #CREATING BOM FOR THE ORDER; THAT IS THE MATERIALS QUANTITY NEEDED TO PREPARE THE ORDER IS CALCULATED
        partslist = {}
        aorder = []
        for j in order.keys():
            for i in bom_list:
                if int(j) == i['ProductID']:
                    if i['PartNo'] in partslist.keys():
                        partslist[i['PartNo']] = float(partslist[i['PartNo']]) + (float(i['Quantity'])*float(order[j]))
                    else:
                        partslist[i['PartNo']]= (float(i['Quantity'])*float(order[j]))

        #CALCULATING THE POTERNIAL ORDER THAT CAN BE PLACED WITH THE CURRENT INVENTORY
        #THIS IS CALCULATED WITH REFERENCE TO THE ORDER PLACE SO THE POTENTIAL ORDER IS EQUAL OR LESSER THAN THE ACTUAL ORDER DEPEDNING  UPON THE MATERIALS AVIALABLE
        mlistCopy=material_list.copy()
        aorder={}
        clr=1
        for i in order.keys():
            pbom=getBOMByProductId(int(i))
            aorder[i]=0
            for j in range(order[i]):
                clr=1
                for k in mlistCopy:
                    for m in pbom:
                        if k['SWPartNo'] == m['PartNo']:
                            diff=float(k['QuantityAvailable'])-float(m['Quantity'])
                            if diff >= 0:
                                k['QuantityAvailable'] = float(k['QuantityAvailable']) - float(m['Quantity'])
                            else:
                                clr=0
                                break
                if clr == 1:
                    aorder[i]=aorder[i]+1

        #-------------------------------------
        # 2. VERIFY IF THERE IS MATERIAL IN STOCK TO MAKE THE PRODUCTS
        #-------------------------------------
        needmore = {}
        material_list=Cart.getAllMaterials()
        for i in partslist.keys():
            for j in material_list:
                if i == j["SWPartNo"] and (float(partslist[i])>float(j["QuantityAvailable"])):
                    needmore[j["SWPartNo"]] = float(partslist[i])-float(j["QuantityAvailable"])
                    c=1

        #THROWING AN ERROR MESSAGE WHEN THERE ARE NOT ENOUGH MATERIALS IN THE INVENTORY
        if c==1:
            return render_template('gorillacarts/orders/create.html',errormessage="Not enough materials in inventory, you need more:",errorpart2=needmore,errormessage2="With your current inventory, you can purchase:",errorpart3=aorder,staff=staff_list,customers=customer_list,products=product_list)

        #IF THERE IS ENOUGH MATERIAL IN THE INVENTORY THEN CALCULATE THE TOTAL PRICE OF THE ORDER AND PLACE THE ORDER
        if c==0:
            #[{'ProductID': 1, 'ProductName': 'Large Cart', 'Color': 'Red', 'Price': 119.99}, {'ProductID': 2, 'ProductName': 'Small Cart', 'Color': 'Blue', 'Price': 49.99}]
            for i in product_list:
                for j in order.keys():
                    if int(j) == i['ProductID']:
                        total += i['Price']*float(order[j])

            Zip=getCustomerById(CustomerID)["ZIP"]
            OrderID=saveOrderDB(CustomerID,EmployeeID,total,Zip)

            for i in product_list:
                 for j in order.keys():
                     if int(j) == i['ProductID']:
                         saveOrderDetailDB(OrderID,int(j),float(order[j]),float(order[j])*i['Price'])

            for i in partslist.keys():
                reduceMaterialDB(float(partslist[i]),i)
        
        return redirect(url_for('gorillacarts.orders'))

    else:
        # How could it have not been a GET or POST? I have no idea how that could have happened.
        return render_template('gorillacarts/orders/create.html',message='Something went wrong.')