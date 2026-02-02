def eventcheck(name,date,host,description):
    error = ""
    msg=[]
    if not name:
        msg.append("Name is missing!")
    if len(name) > 25:
        msg.append("Name is too long!")
    if not date:
        msg.append("Date is missing!")
    if len(date) > 12:
        msg.append("Date is the incorrect length!")
    if not host:
        msg.append("Host is missing!")
    if len(host) > 20:
        msg.append("Host name is too long!")
    if not description:
        msg.append("Description is missing!")
    if len(description) > 255:
        msg.append("Description is too long!")
    #prints out message only if there's an error
    if len(msg) > 0:
        error=" \n".join(msg)
    return error

#same one as before, just different variables
def attendeecheck(name,email,comment):
    error = ""
    msg=[]
    if not name:
        msg.append("Name is missing!")
    if len(name) > 25:
        msg.append("Name is too long!")
    if not email:
        msg.append("Email is missing!")
    if len(email) > 100:
        msg.append("Email is too long!")
    if not comment:
        msg.append("Comment is missing!")
    if len(comment) > 255:
        msg.append("Comment is too long!")
    if len(msg) > 0:
        error=" \n".join(msg)
    return error