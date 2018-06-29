from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages


def dv_sync(request):
    from main.models import Department, Employee
    import pymssql

    new_deps = 0
    new_emps = 0

    conn = pymssql.connect(
        host='srv-db-01\\nssql',
        user='anton',
        password='q1w2e3',
        database="Docsvision",
        as_dict=True,
        charset='cp1251')
    cursor = conn.cursor()
    cursor2 = conn.cursor()

    cursor.execute('SELECT deps.RowID, deps.ParentTreeRowID, deps.Name, deps.Manager, deps.FullName '
                   'FROM [dvtable_{7473F07F-11ED-4762-9F1E-7FF10808DDD1}] as deps '
                   'LEFT JOIN [dvtable_{7473F07F-11ED-4762-9F1E-7FF10808DDD1}] as deps2 ON deps2.RowID=deps.ParentTreeRowID '
                   'LEFT JOIN [dvtable_{7473F07F-11ED-4762-9F1E-7FF10808DDD1}] as deps3 ON deps3.RowID=deps2.ParentTreeRowID '
                   'WHERE deps.ParentTreeRowID=\'FBE0E660-2BAC-4D7A-B96F-C54EABBEC2C1\' or deps2.ParentTreeRowID=\'FBE0E660-2BAC-4D7A-B96F-C54EABBEC2C1\' '
                   ' or deps3.ParentTreeRowID=\'FBE0E660-2BAC-4D7A-B96F-C54EABBEC2C1\'')

    deps = Department.objects.all()
    for row in cursor:
        if deps.filter(dv_guid=row['RowID']).count() == 0:
            dep = Department(
                name=row['Name'],
                short_name=row['FullName'],
                dv_guid=row['RowID'],
            )
            dep.save()
            new_deps += 1
        else:
            dep = deps.get(dv_guid=row['RowID'])
            dep.name = row['Name']
            dep.short_name = row['FullName']
            dep.dv_guid = row['RowID']
            dep.save()

    cursor2.execute('SELECT DISTINCT emps.RowID, emps.ParentRowID, emps.FirstName, emps.MiddleName, emps.LastName, emps.SysAccountName, emps.Email, positions.Name, '
                    'CASE WHEN  exists (SELECT * FROM [dvtable_{A960E37B-F1BD-4981-858D-AE9706E0571E}] as groups '
                    'WHERE groups.EmployeeID=emps.RowID and groups.ParentRowID=\'248BA69F-05F6-46E4-B683-6761454925CD\') THEN 1 ELSE 0 END as Active '
                    'FROM [dvtable_{DBC8AE9D-C1D2-4D5E-978B-339D22B32482}] as emps '
                    'LEFT JOIN [dvtable_{CFDFE60A-21A8-4010-84E9-9D2DF348508C}] as positions ON positions.RowID=emps.Position '
                    'WHERE emps.ChangeServerID is not NULL')

    emps = Employee.objects.all()
    for row in cursor2:
        if emps.filter(dv_guid=row['RowID']).count() == 0:
            if deps.filter(dv_guid=row['ParentRowID']).count() > 0:
                emp = Employee(
                    dv_guid=row['RowID'],
                    first_name=row['FirstName'],
                    middle_name=row['MiddleName'],
                    last_name=row['LastName'],
                    account_name=row['SysAccountName'],
                    email=row['Email'],
                    position=row['Name'],
                    department=Department.objects.get(dv_guid=row['ParentRowID']),
                    active=True # row['Active'],
                )
                emp.save()
                new_emps += 1
        else:
            emp = emps.get(dv_guid=row['RowID'])
            emp.first_name = row['FirstName']
            emp.middle_name = row['MiddleName']
            emp.last_name = row['LastName']
            emp.account_name = row['SysAccountName']
            emp.email = row['Email']
            emp.position = row['Name']
            if deps.filter(dv_guid=row['ParentRowID']).count() > 0:
                emp.department = Department.objects.get(dv_guid=row['ParentRowID'])
            emp.active = True # row['Active']
            emp.save()

    cursor.execute('SELECT deps.RowID, deps.ParentTreeRowID, deps.Name, deps.Manager, deps.FullName '
                   'FROM [dvtable_{7473F07F-11ED-4762-9F1E-7FF10808DDD1}] as deps '
                   'LEFT JOIN [dvtable_{7473F07F-11ED-4762-9F1E-7FF10808DDD1}] as deps2 ON deps2.RowID=deps.ParentTreeRowID '
                   'LEFT JOIN [dvtable_{7473F07F-11ED-4762-9F1E-7FF10808DDD1}] as deps3 ON deps3.RowID=deps2.ParentTreeRowID '
                   'WHERE deps.ParentTreeRowID=\'FBE0E660-2BAC-4D7A-B96F-C54EABBEC2C1\' or deps2.ParentTreeRowID=\'FBE0E660-2BAC-4D7A-B96F-C54EABBEC2C1\' '
                   'or deps3.ParentTreeRowID=\'FBE0E660-2BAC-4D7A-B96F-C54EABBEC2C1\'')

    for row in cursor:
        dep = deps.get(dv_guid=row['RowID'])
        if str(row['ParentTreeRowID']) != 'fbe0e660-2bac-4d7a-b96f-c54eabbec2c1':
            dep.parent_department = deps.get(dv_guid=row['ParentTreeRowID'])
        if row['Manager'] is not None and str(row['Manager']) != '7f8468b0-a79d-48af-8023-c36b7e2c049f':
            dep.manager = emps.get(dv_guid=row['Manager'])
        dep.save()

    cursor.close()
    cursor2.close()
    return HttpResponse('new deps: '+str(new_deps)+'<br/>new emps: '+str(new_emps))