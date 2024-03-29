from general_handle.dbc import connection, cursor
from general_handle import output, string_handle, token_handle
import config

def viewall(token):
    if(token_handle.tokenadmin(token)):
        cursor.execute('select * from users_hide')
        rows = cursor.fetchall()
        cursor.execute("DESCRIBE users_hide")
        cols = cursor.fetchall()
        return output.tabletojson(cols, rows, config.Success)
    else:
        return output.error(config.not_permitted)

def createuser(token, StudentID, Password, Fullname, PhoneNumber, Specialization, Class, Admin):
    if (Admin != "0"):
        return output.error(config.not_permitted)
    if(token_handle.tokenadmin(token)):
        cursor.execute('select * from users where StudentID = "'+StudentID+'"')
        rows = cursor.fetchall()
        if(len(rows)>0):
            return output.error("Student ID already exist!")
        Password = string_handle.toMD5(StudentID+Password)
        token = "TOKEN"
        Expiry = '(select current_date() + interval '+str(config.default_Expiry)+' year)'
        query = "INSERT INTO users ( StudentID, Password, Fullname, PhoneNumber, Specialization, Class, Admin, token, Expiry) VALUES ('"+StudentID+"', '"+Password+"', '"+Fullname+"', '"+PhoneNumber+"', '"+Specialization+"', '"+Class+"', '"+Admin+"', '"+token+"', "+Expiry+")"
        print(query)
        cursor.execute(query)
        connection.commit()
        output.log(token_handle.tokentoStudentID(token), StudentID, "Create User")
        return output.ok(config.Success)
    else:
        return output.error(config.not_permitted)

def deluser(token, StudentID):
    if(token_handle.tokenadmin(token)):
        cursor.execute('select * from users where StudentID = "'+StudentID+'"')
        rows = cursor.fetchall()
        if(len(rows)>0):
            if(token_handle.StudentIDadmin(StudentID)):
                return output.error(config.not_permitted)
            query = "Select * from borrow where StudentID = '"+StudentID+"' and (status = 'borrowed' or status = 'wait')"
            cursor.execute(query)
            rows = cursor.fetchall()
            if(len(rows)>0):
                return output.strtojson('{"status": "ERROR", "data":[{"message": "Sinh viên còn tài liệu đang đợi mượn hoặc chưa trả!"}]}')
            query = "delete FROM borrow where StudentID = '"+StudentID+"'"
            cursor.execute(query)
            connection.commit()
            query = "delete FROM users where StudentID = '"+StudentID+"'"
            cursor.execute(query)
            connection.commit()
            output.log(token_handle.tokentoStudentID(token), StudentID, "Delete User" )
            return output.ok(config.Success)
        else:
            return output.error("Student ID does not exist!")
    else:
        return output.error(config.not_permitted)

def disableuser(token, StudentID):
    if(token_handle.tokenadmin(token)):
        cursor.execute('select * from users where StudentID = "'+StudentID+'"')
        rows = cursor.fetchall()
        if(len(rows)>0):
            if(rows[0][9]=='active'):
                if(token_handle.StudentIDadmin(StudentID)):
                    return output.error(config.not_permitted)
                query = "update users set status = 'disable' where StudentID = '"+StudentID+"'"
                cursor.execute(query)
                connection.commit()
                output.log(token_handle.tokentoStudentID(token), StudentID, "Disable User" )
                return output.ok("Disabled!")
            else:
                return output.error("Student has been disabled before!")
        else:
            return output.error("Student ID does not exist!")
    else:
        return output.error(config.not_permitted)

def activeuser(token, StudentID):
    if(token_handle.tokenadmin(token)):
        cursor.execute('select * from users where StudentID = "'+StudentID+'"')
        rows = cursor.fetchall()
        if(len(rows)>0):
            if(rows[0][9]=='disable'):
                if(token_handle.StudentIDadmin(StudentID)):
                    return output.error(config.not_permitted)
                query = "update users set status = 'active' where StudentID = '"+StudentID+"'"
                cursor.execute(query)
                connection.commit()
                output.log(token_handle.tokentoStudentID(token), StudentID, "Active User" )
                return output.ok("Actived!")
            else:
                return output.error("Student has been activated before!")
        else:
            return output.error("Student ID does not exist!")
    else:
        return output.error(config.not_permitted)

def update(token, StudentID, Password, Fullname, PhoneNumber, Specialization, Class, Admin):
    if(token_handle.StudentIDadmin(StudentID)):
        return output.error(config.not_permitted)
    if(Admin == "1"):
        return output.error(config.not_permitted)
    if(token_handle.tokenadmin(token)):
        cursor.execute('select * from users where StudentID = "'+StudentID+'"')
        rows = cursor.fetchall()
        if(len(rows)>0):
            Password = string_handle.toMD5(StudentID+Password)
            query = "update users set Password = '"+Password+"', Fullname = '"+Fullname+"', PhoneNumber = '"+PhoneNumber+"', Specialization = '"+Specialization+"', Class = '"+Class+"', Admin = "+Admin+" where StudentID = '"+StudentID+"'"
            # if Password == "":
            #     query = "update users set Fullname = '"+Fullname+"', PhoneNumber = '"+PhoneNumber+"', Specialization = '"+Specialization+"', Class = '"+Class+"', Expiry = '"+Expiry+"' where StudentID = '"+StudentID+"'"
            cursor.execute(query)
            connection.commit()
            output.log(token_handle.tokentoStudentID(token), StudentID, "Update User")
            return output.ok(config.Success)
        else:
            return output.error("Student ID does not exist!")
    else:
        return output.error(config.not_permitted)

def Extend(token, StudentID, Expiry):
    if(token_handle.StudentIDadmin(StudentID)):
        return output.error(config.not_permitted)
    if(token_handle.tokenadmin(token)):
        cursor.execute('select * from users where StudentID = "'+StudentID+'"')
        rows = cursor.fetchall()
        if(len(rows)>0):
            
            Expiry = 'DATE_ADD(Expiry, INTERVAL '+Expiry+' year)'
            query = "update users set Expiry = "+Expiry+" where StudentID = '"+StudentID+"'"
            # if Password == "":
            #     query = "update users set Fullname = '"+Fullname+"', PhoneNumber = '"+PhoneNumber+"', Specialization = '"+Specialization+"', Class = '"+Class+"', Expiry = '"+Expiry+"' where StudentID = '"+StudentID+"'"
            cursor.execute(query)
            connection.commit()
            output.log(token_handle.tokentoStudentID(token), StudentID, "Extend")
            return output.ok(config.Success)
        else:
            return output.error("Student ID does not exist!")
    else:
        return output.error(config.not_permitted)