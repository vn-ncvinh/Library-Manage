from general_handle.dbc import cursor, connection
from general_handle import output, token_handle
import config


def add(token, Name, Description):
    if(token_handle.tokenadmin(token)):
        query="select * from category where Name = '"+Name+"' and Description = '"+Description+"'"
        cursor.execute(query)
        rows=cursor.fetchall()
        if(len(rows)>0):
            return output.error("Category already exist!")
        # try:
        query="INSERT INTO category (Name, Description) VALUES ('"+Name+"', '"+Description+"')"
        cursor.execute(query)
        connection.commit()
        query="select * from category_quantity where Name = '"+Name+"' and Description = '"+Description+"'"
        cursor.execute(query)
        rows = cursor.fetchall()
        cursor.execute("DESCRIBE category_quantity")
        cols = cursor.fetchall()
        output.log(token_handle.tokentoStudentID(token), rows[0][0], "Add Category!" )
        return output.tabletojson(cols, rows, config.Success)
        # except Exception as e:
        #     return output.error(str(e))
    else:
        return output.error(config.not_permitted)

def delete(token, ID):
    if(token_handle.tokenadmin(token)):
        query = "select * from category where ID = "+ID
        cursor.execute(query)
        rows=cursor.fetchall()
        if(len(rows)>0):
            query="Delete from category_documents where CategoryID = '"+ID+"'"
            cursor.execute(query)
            connection.commit()
            query="Delete from category where ID = '"+ID+"'"
            cursor.execute(query)
            connection.commit()
            output.log(token_handle.tokentoStudentID(token), ID, "Delete Category!" )
            return output.ok(config.Success)
        else:
            return output.error('Incorrect Category ID!')
    else:
        return output.error(config.not_permitted)

def update(token, ID, Name, Description):
    if(token_handle.tokenadmin(token)):
        query = "select * from category where ID = "+ID
        cursor.execute(query)
        rows=cursor.fetchall()
        if(len(rows)>0):
            query="Update category set Name = '"+Name+"', Description = '"+Description+"' where ID = '"+ID+"'"
            cursor.execute(query)
            connection.commit()
            output.log(token_handle.tokentoStudentID(token), ID, "Delete Category!" )
            return output.ok(config.Success)
        else:
            return output.error('Incorrect Category ID!')
    else:
        return output.error(config.not_permitted)