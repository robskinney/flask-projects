def getFormVariable(request, variableName):
    return request.form.get(variableName, 0)

def getIntegerFormVariable(request, variableName):
    return int(request.form.get(variableName, 0))

def getFloatFormVariable(request, variableName):
    return float(request.form.get(variableName, 0))