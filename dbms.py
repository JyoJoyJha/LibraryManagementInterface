import mysql.connector
from datetime import date
from datetime import datetime
from datetime import timedelta
import random
import time

mydb=mysql.connector.connect(host="localhost", user="root", password="saanjysh", database="dbmsproject")

cur=mydb.cursor()

def memnew():
    insert_stmt="Insert into MEMBERS values (%s, %s, %s, %s, %s, %s)"
    memid=int(input("Member Identification Number(m_id): "))
    fname=input("First Name: ")
    lname=input("Last Name: ")
    dobinp=input("Date Of Birth (yyyy-mm-dd): ")
    dob= datetime.strptime(dobinp, "%Y-%m-%d")
    gen=input("Gender: ")
    phone=int(input("Phone Number: "))
    data=(memid, fname, lname, dob, gen, phone)

    try:
        cur.execute(insert_stmt, data)
        mydb.commit()
        print("Data Inserted")
    except:
        mydb.rollback()
        print("Data Not Inserted")
    
def booknew():
    insert_stmt="Insert into BOOKS (isbn, bname, author, publisher, edition) values (%s, %s, %s, %s, %s)"
    isbn=int(input("Enter ISBN of book: "))
    name=input("Name of the Book: ")
    author=input("Author: ")
    pub=input("Publisher: ")
    ed=int(input("Edition: "))
    data=(isbn, name, author, pub, ed)

    try:
        cur.execute(insert_stmt, data)
        mydb.commit()
        print("Data Inserted")
    except:
        mydb.rollback()
        print("Data Not Inserted")

def payfine():
    mid=int(input("Membership Identification Number(m_id): "))
    cur.execute("Select m_id, fine_amt from fine")
    famt=cur.fetchall()
    l=[]
    for i in famt:
        l.append(i[0])
    if mid in l:
        cur.execute("Select m_id, fine_amt from fine where m_id="+str(mid))
        famt=cur.fetchall()
        for i in famt:
            fineamt=i[1]
        print("Total fine to pay:",fineamt)
        if fineamt==0:
            print("No Fine to Pay")
        else:
            paying=int(input("Fine amount you will be paying: "))
            if paying>fineamt:
                    print("This amount can not be accepted")
            else:
                try:
                    cnum=int(input("Card Number: "))
                    cname=input("Name on Card: ")
                    ccvv= int(input("CVV: "))
                    randpin=random.randint(10000, 99999)
                    print("MESSAGE: Pin Generated:", randpin)
                    pinent=int(input("Enter Pin sent in the message in registered number: "))
                    time.sleep(2)
                    if pinent==randpin:
                        cur.execute("Update fine set fine_amt=fine_amt-"+str(paying)+" where m_id="+str(mid))
                        mydb.commit()
                        print("Transaction Successfull")
                    else:
                        print("Transaction Unsuccessfull")
                except:
                    mydb.rollback()
                    print("Trasaction Unsuccessfull ")
    else:
        print("No Fine to Pay")

def viewinfo():
    mid=int(input("Membership Identification Number(m_id): "))
    cur.execute("Select * from Members")
    mems = cur.fetchall()
    for i in mems:
        if i[0]==mid:
            print("Member Identification Number:", i[0])
            print("Name:", i[1], i[2])
            print("Date of Birth:", i[3])
            print("Gender:", i[4])
            print("Phone Number:", i[5])


def namechange():
    l=[];
    mid=int(input("Membership Identification Number(m_id): "))
    cur.execute("Select m_id, fname, lname from Members")
    mems = cur.fetchall()
    for i in mems:
        l.append(i)
    fnnew=input("First Name: ")
    lnnew=input("Last Name: ")
    for i in l:
        if i[0]==mid:
            stmt="Update MEMBERS set fname=%s, lname=%s where m_id=%s"
            data=(fnnew, lnnew, mid)
            try:
                cur.execute(stmt, data)
                mydb.commit()
                print("Name Updated Successfully")
            except:
                mydb.rollback()
                print("Update Not Possible")

def numchange():
    l=[];
    mid=int(input("Membership Identification Number(m_id): "))
    cur.execute("Select m_id, mphone from Members")
    mems = cur.fetchall()
    for i in mems:
        l.append(i)
    numnew=input("New Phone Number: ")
    for i in l:
        if i[0]==mid:
            stmt="Update MEMBERS set mphone=%s where m_id=%s"
            data=(numnew, mid)
            try:
                cur.execute(stmt, data)
                mydb.commit()
                print("Phone Number Updated Successfully")
            except:
                mydb.rollback()
                print("Update Not Possible")

def bookissue():
    numbook=0
    mid=int(input("Membership Identification Number(m_id): "))
    isbn=int(input("ISBN Number: "))
    cur.execute("Select m_id, count(*) from issue i where i.return_stat='NR' group by m_id having i.m_id="+str(mid))
    countl=cur.fetchall()
    for i in countl:
        numbook=i[1]
    if numbook>=3:
        print("Maximum limit of issues attained")
    else:
        cur.execute("Select Status from books where isbn="+str(isbn))
        bstat=cur.fetchall()
        status= bstat[0][0]
    
        if status=='t':
            print("Book can not be issued")
            print("Please select another book")
        else:
            isda=input("Date of Issue (yyyy-mm-dd): ")
            issdate= datetime.strptime(isda, "%Y-%m-%d").date()
            retdatee = issdate + timedelta(days=21)
            stmt=("Insert into issue(m_id, ISBN, issue_date, return_date_e)"
            "values (%s, %s, %s, %s)")
            data=(mid, isbn, issdate, retdatee)
            try:
                cur.execute(stmt, data)
                mydb.commit()
                print("Book Issued Successfully")
            except:
                mydb.rollback()
                print("Book can not be issued")
                print("Please select another book")

def bookreturn():
    mid=int(input("Membership Identification Number(m_id): "))
    cur.execute("Select ISBN,bname,issue_date, return_date_e from issue i natural join books b where i.return_stat='NR' and b.status='t'and i.m_id="+str(mid))
    info=cur.fetchall()
    l=[]
    print("Books Currently Issued:")
    print("ISBN\t\t Book Name")
    for i in info:
        print(i[0],"\t", i[1])
        l.append(i[0])
    retisbn=int(input("ISBN of book to return: "))
    for i in info:
        if i[0]==retisbn:
            retdate_e =i[3]
            issdate=i[2]
            print("Issue Date: ",issdate)
            break;
    if retisbn in l:
        retdate=input("Return Date: ")
        stmt=("Update issue set return_date_a=%s, return_stat='R' where m_id=%s and isbn=%s and issue_date=%s")
        data=(retdate, mid, retisbn, issdate)
        try:
            cur.execute(stmt, data)
            mydb.commit()
            cur.execute("Update books set status='f' where isbn="+str(retisbn))
            mydb.commit()
            print("Book Returned Successfully")
        except:
            mydb.rollback()
            print("Unexpected Error!")
            print("Please try again later")
        retdate= datetime.strptime(retdate, "%Y-%m-%d").date()
        if (retdate>retdate_e):
            print("Fine is Imposed for Late Return")
            delta=(retdate-retdate_e).days
            fine=30*delta
            print("Fine Value: ", fine)
            try:
                cur.execute("Insert into Fine values ("+str(mid)+", "+str(fine)+")")
                mydb.commit()
            except:
                mydb.rollback()
                cur.execute("Update fine set fine_amt=fine_amt+"+str(fine)+" where m_id="+str(mid))
                mydb.commit()
    else:
        print("ISBN Entered Invalid")
        
def bookstat():
    print("Books Available:")
    print("ISBN\t\t Book Name")
    cur.execute("Select ISBN, bname from books")
    l=[]
    books=cur.fetchall()
    for i in books:
        print(i[0],"\t", i[1])
        l.append(i[0])
    isbn=int(input("ISBN of book: "))
    if isbn in l:
        cur.execute("Select isbn, status from books where isbn="+str(isbn))
        statusl=cur.fetchall()
        for i in statusl:
            status=i[1]
        if status=='t':
            print("Book is Taken")
        else:
            print("Book is Available")
    else:
        print("ISBN Entered Invalid")
    
ch=1;
while ch==1:
    print("WELCOME TO PERKINSONS LIBRARY\n")
    print("Main Menu:")
    print("MAINTENANCE\n\t1. New Member\n\t2. New Book Entry\n\t3. Fine Payment\n")
    print("MEMBERS\n\t4. View Information\n\t5. Change Name\n\t6. Change Number")
    print("BOOKS\n\t7. Book Issue\n\t8. Book Return\n\t9. Book Status")
    print("10. Exit")
    choice=int(input("Enter choice (1-9): "))
    if choice==1:
        memnew()
    elif choice==2:
        booknew()
    elif choice==3:
        payfine()
    elif choice==4:
        viewinfo()
    elif choice==5:
        namechange()
    elif choice==6:
        numchange()
    elif choice==7:
        bookissue()
    elif choice==8:
        bookreturn()
    elif choice==9:
        bookstat()
    elif choice==10:
        print("Thank You")
        print("We hope to see you again")
        break;
    else:
        print("Incorrect choice")
    print("Do You wish to continue?")
    ch=int(input("1 for Yes, 0 for No: "))

