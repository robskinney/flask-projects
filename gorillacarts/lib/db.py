from datetime import datetime
import sqlite3

import os

APP_ROOT = os.path.dirname(os.path.abspath(__file__))

########################################################################################

#-------------------------------------
# 1. DELETE Record from TB by column name and name
#-------------------------------------
def genDelete_DB(table,column,row):
    conn = sqlite3.connect(os.path.join(APP_ROOT,'Carts.db'))
    sql='DELETE FROM {} WHERE {} = ?'.format(table,column)
    cur = conn.cursor()
    cur.execute(sql, (row,))
    conn.commit()

#-------------------------------------
# 2. ADD CUSTOMERS TO DB
#-------------------------------------
def saveCustomerDB(name,zip,telephone,email,category):
    conn = sqlite3.connect(os.path.join(APP_ROOT,'Carts.db'))
    sql='INSERT INTO Customers (Name, ZIP, Telephone, Email, Category) values (?,?,?,?,?)'
    cur = conn.cursor()
    cur.execute(sql, (name,zip,telephone,email,category,))
    conn.commit()

#-------------------------------------
# 3. ADD SUPPLIER TO DB
#-------------------------------------
def saveSupplierDB(name,zip,telephone,email):
    conn = sqlite3.connect(os.path.join(APP_ROOT,'Carts.db'))
    sql='INSERT INTO Suppliers (Name, ZIP, Telephone, Email) values (?,?,?,?)'
    cur = conn.cursor()
    cur.execute(sql, (name,zip,telephone,email,))
    conn.commit()
    
#-------------------------------------
# 4. ADD MATERIAL TO DB
#-------------------------------------

def saveMaterialDB(SWPartNo,SupplierPartNo,SupplierID,ProductName,Price,QuantityAvailable):
    conn = sqlite3.connect(os.path.join(APP_ROOT,'Carts.db'))
    sql='INSERT INTO Materials (SWPartNo, SupplierPartNo, SupplierID, ProductName, Price, QuantityAvailable) values (?,?,?,?,?,?)'
    cur = conn.cursor()
    cur.execute(sql, (SWPartNo,SupplierPartNo,SupplierID,ProductName,Price,QuantityAvailable,))
    conn.commit()

#-------------------------------------
# 5. UPDATE MATERIAL TO DB
#-------------------------------------

def reduceMaterialDB(QuantityAvailable,SWPartNo):
    conn = sqlite3.connect(os.path.join(APP_ROOT,'Carts.db'))
    sql='UPDATE Materials SET QuantityAvailable = QuantityAvailable - ? WHERE SWPartNo = ?'
    cur = conn.cursor()
    cur.execute(sql, (QuantityAvailable,SWPartNo,))
    conn.commit()
    
#-------------------------------------
# 6. ADD ORDER TO DB
#-------------------------------------
def saveOrderDB(CustomerID,EmpID,Total,Zip):
    conn = sqlite3.connect(os.path.join(APP_ROOT,'Carts.db'))
    sql='INSERT INTO Orders (CustomerID,EmpID,Total,Date,Zip) values (?,?,?,?,?)'
    cur = conn.cursor()
    now = datetime.now()
    curdate = now.strftime("%d/%m/%Y %H:%M:%S")
    cur.execute(sql, (CustomerID,EmpID,Total,curdate,Zip,))
    conn.commit()
    return cur.lastrowid

#-------------------------------------
# 7. ADD ORDERDETAIL (PRODUCTS IN THE ORDER) TO DB
#-------------------------------------

def saveOrderDetailDB(OrderID, ProductID, Qty,AmtPayable):
    conn = sqlite3.connect(os.path.join(APP_ROOT,'Carts.db'))
    sql='INSERT INTO Order_Detail (OrderID, ProductID, Qty,AmtPayable) values (?,?,?,?)'
    cur = conn.cursor()
    cur.execute(sql, (OrderID, ProductID, Qty,AmtPayable,))
    conn.commit()

#-------------------------------------
# 8. SELECT ONE CUSTOMER FROM DB
#-------------------------------------

def getCustomerById(customer_id):
    con = sqlite3.connect(os.path.join(APP_ROOT,'Carts.db'))
    con.row_factory = sqlite3.Row
    cursor = con.cursor()

    cursor.execute(
        'SELECT * FROM Customers WHERE CustomerID = ?;',
        (customer_id,)
    )

    row = cursor.fetchone()
    con.close()

    if row is None:
        return None

    return {
        "CustomerID": row["CustomerID"],
        "Name": row["Name"],
        "ZIP": row["ZIP"],
        "Telephone": row["Telephone"],
        "Email": row["Email"],
        "Category": row["Category"]
    }

#-------------------------------------
# 9. SELECT ONE MATERIAL FROM DB
#-------------------------------------

def getMaterialById(material_id):
    con = sqlite3.connect(os.path.join(APP_ROOT,'Carts.db'))
    con.row_factory = sqlite3.Row
    cursor = con.cursor()

    cursor.execute(
        'SELECT * FROM Materials WHERE SWPartNo = ?;',
        (material_id,)
    )

    row = cursor.fetchone()
    con.close()

    if row is None:
        return None

    return {
        "SWPartNo": row["SWPartNo"],
        "SupplierPartNo": row["SupplierPartNo"],
        "SupplierID": row["SupplierID"],
        "ProductName": row["ProductName"],
        "Price": row["Price"],
        "QuantityAvailable": row["QuantityAvailable"]
    }

#-------------------------------------
# 10. SELECT ONE SUPPLIER FROM DB
#-------------------------------------

def getSupplierById(supplier_id):
    con = sqlite3.connect(os.path.join(APP_ROOT,'Carts.db'))
    con.row_factory = sqlite3.Row
    cursor = con.cursor()

    cursor.execute(
        'SELECT * FROM Suppliers WHERE SupplierID = ?;',
        (supplier_id,)
    )

    row = cursor.fetchone()
    con.close()

    if row is None:
        return None

    return {
        "SupplierID": row["SupplierID"],
        "Name": row["Name"],
        "ZIP": row["ZIP"],
        "Telephone": row["Telephone"],
        "Email": row["Email"]
    }

#-------------------------------------
# 11. SELECT ONE ORDER FROM DB
#-------------------------------------

def getOrderById(order_id):
    con = sqlite3.connect(os.path.join(APP_ROOT,'Carts.db'))
    con.row_factory = sqlite3.Row
    cursor = con.cursor()

    cursor.execute(
        'SELECT * FROM Orders WHERE OrderID = ?;',
        (order_id,)
    )

    row = cursor.fetchone()
    con.close()

    if row is None:
        return None

    return {
        "OrderID": row["OrderID"],
        "CustomerID": row["CustomerID"],
        "EmpID": row["EmpID"],
        "Total": row["Total"],
        "Date": row["Date"],
        "ZIP": row["ZIP"]
    }

#-------------------------------------
# 12. GET ALL THE PRODUCTS INSIDE AN ORDER FROM DB
#-------------------------------------

def getOrderDetailsById(id):
    con = sqlite3.connect(os.path.join(APP_ROOT,'Carts.db'))
    con.row_factory = sqlite3.Row
    cursorObj = con.cursor()
    order = []
    cursorObj.execute('SELECT * FROM Order_Detail where OrderID = ?;',(id,))
    rows = cursorObj.fetchall()
    for individualRow in rows:
        cursorObj.execute('SELECT ProductName, Color FROM Products where ProductID = ?;',(individualRow[1],))
        row=cursorObj.fetchall()
        for i in row:
            b = {"OrderID": individualRow[0], "ProductName":i[0]+" ("+i[1]+")", "ProductID": individualRow[1], "Qty": individualRow[2], "AmtPayable": individualRow[3]}
            order.append(b)
    return order

#-------------------------------------
# 13. GET BOM FOR A PRODUCT FROM DB
#-------------------------------------

def getBOMByProductId(id):
    con = sqlite3.connect(os.path.join(APP_ROOT,'Carts.db'))
    con.row_factory = sqlite3.Row
    cursorObj = con.cursor()
    material = []
    cursorObj.execute('SELECT * FROM BOMs where ProductID = ?;',(id,))
    rows = cursorObj.fetchall()
    for individualRow in rows:
        cursorObj.execute('SELECT ProductName FROM Materials where SWPartNo = ?;',(individualRow[1],))
        row=cursorObj.fetchone()
        b = {"ProductID" : individualRow[0], "ProductName": row[0], "PartNo" : individualRow[1], "Quantity": individualRow[2]}
        material.append(b)
    return material

#-------------------------------------
# 14. GET THE PRODUCT NAME OF A PRODUCT FROM DB
#-------------------------------------

def getProductName(title):
    con = sqlite3.connect(os.path.join(APP_ROOT,'Carts.db'))
    con.row_factory = sqlite3.Row
    cursorObj = con.cursor()
    name = []
    cursorObj.execute('SELECT Name FROM Products where ProductID = ?;',(title,))
    rows = cursorObj.fetchall()
    for individualRow in rows:
        b = {"Name": individualRow[0]}
        name.append(b)
    return name

#-------------------------------------
# 15. UPDATE PERSONAL DETAILS OF A CUSTOMER FROM DB
#-------------------------------------
def updateCustomerDB(customerID,zip,telephone,email,category):
    conn = sqlite3.connect(os.path.join(APP_ROOT,'Carts.db'))

    #B. Write a SQL statement to insert a specific row (based on Title name)
    sql='UPDATE Customers set ZIP = ?, Telephone = ?, Email = ?, Category = ? WHERE CustomerID = ?'

    # B. Create a workspace (aka Cursor)
    cur = conn.cursor()

    # C. Run the SQL statement from above and pass it 1 parameter for each ?
    cur.execute(sql, (zip, telephone, email, category, customerID))

    # D. Save the changes
    conn.commit()

#-------------------------------------
# 16. UPDATE SUPPLIER DETAILS FROM DB
#-------------------------------------

def updateSupplierDB(zip,telephone,email,supplierid):
    conn = sqlite3.connect(os.path.join(APP_ROOT,'Carts.db'))

    #B. Write a SQL statement to insert a specific row (based on Title name)
    sql='UPDATE Suppliers set ZIP = ?, Telephone = ?, Email = ?  WHERE SupplierID = ?'

    # B. Create a workspace (aka Cursor)
    cur = conn.cursor()

    # C. Run the SQL statement from above and pass it 1 parameter for each ?
    cur.execute(sql, (zip, telephone, email, supplierid))

    # D. Save the changes
    conn.commit()

#-------------------------------------
# 15. UPDATE MATERIAL DETAILS IN THE DB
#-------------------------------------

def updateMaterialDB(SupplierPartNo,SupplierID,ProductName,Price,QuantityAvailable,SWPartNo):
    conn = sqlite3.connect(os.path.join(APP_ROOT,'Carts.db'))

    #B. Write a SQL statement to insert a specific row (based on Title name)
    sql='UPDATE Materials set SupplierPartNo = ?, SupplierID = ?, ProductName = ?, Price = ?, QuantityAvailable = ? WHERE SWPartNo = ?'

    # B. Create a workspace (aka Cursor)
    cur = conn.cursor()

    # C. Run the SQL statement from above and pass it 1 parameter for each ?
    cur.execute(sql, (SupplierPartNo,SupplierID,ProductName,Price,QuantityAvailable,SWPartNo,))

    # D. Save the changes
    conn.commit()
    
#-------------------------------------
# 16. DELETE CUSTOMER FROM DB by ID
#-------------------------------------

def delCustomer_DB(title):
    conn = sqlite3.connect(os.path.join(APP_ROOT,'Carts.db'))
    sql='DELETE FROM Customers WHERE CustomerID=?'
    cur = conn.cursor()
    cur.execute(sql, (title,))
    conn.commit()


