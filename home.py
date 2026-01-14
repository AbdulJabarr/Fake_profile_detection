import csv
import os
from difflib import SequenceMatcher
from datetime import datetime
from werkzeug.utils import secure_filename
# from sentence_similarity import sentence_similarity

import ar_master
from flask import Flask, render_template, flash, request, session, current_app, send_from_directory, redirect

app = Flask(__name__, static_folder="static")
app.config.from_object(__name__)
app.config['SECRET_KEY'] = '7d441f27d441f27567d441f2b6176a'
mm = ar_master.master_flask_code()


@app.route("/")
def homepage():
    return render_template('index.html')


@app.route("/user_home")
def user_home():
    user=session['username']
    qry="select * from tweet_details where matching='0'"
    data=mm.select_direct_query(qry)
    return render_template('user_home.html',items=data)

@app.route("/admin_home")
def admin_home():
    return render_template('admin_home.html')



@app.route("/admin", methods=['GET', 'POST'])
def admin():
    error = None

    if request.method == 'POST':
        un = request.form['uname']
        pa = request.form['pass']
        print(un)
        print(pa)
        pa = pa.strip()
        un = un.strip()
        if un == "admin" and pa == "admin":
            return render_template('admin_home.html', error=error)
        else:
            return render_template('admin.html', error=error)
    return render_template('admin.html')




@app.route("/user", methods=['GET', 'POST'])
def user():
    error = None
    if request.method == 'POST':
        un = request.form['email']
        pa = request.form['password']
        total = get_blocked_count(un)
        if total>=3:
            return render_template('user.html', msg="Account Blocked")
        usern = mm.select_direct_query("select * from user_details where email='" + str(un) + "' and password='" + str(pa) + "'")
        if usern:
            session['username'] = un
            return user_home()
        else:
            return render_template('user.html', error=error)
    return render_template('user.html')

def match_fake_profile(email,contact):
    file = 'profile_dataset.csv'
    current_aadhar=''
    account_contact = []
    account_email = []
    with open(file) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            t1 = row['aadhar'].lower().strip()
            t2 = row['contact'].lower().strip()
            t3 = row['email'].lower().strip()
            if t2==contact or t3==email:
                current_aadhar=t1
    with open(file) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            t1 = row['aadhar'].lower().strip()
            t2 = row['contact'].lower().strip()
            t3 = row['email'].lower().strip()
            if current_aadhar==t1:
                account_contact.append(t2)
                account_email.append(t3)
    print(account_contact)
    print(account_email)
    return account_contact,account_email







@app.route("/user_register", methods = ['GET', 'POST'])
def user_register():
    if request.method == 'POST':
        name = request.form['name']
        contact = request.form['contact']
        email = request.form['email']
        address = request.form['address']
        gender = request.form['gender']
        dob = request.form['dob']
        password = request.form['password']
        account_contact,account_email=match_fake_profile(email,contact)
        qry="select * from user_details where contact IN('"+str(contact)+"',"
        for x in account_contact:
            qry+="'"+x+"',"
        qry = ''.join(qry.rsplit(qry[-1], 1))
        qry += ")"
        ##############
        qry=qry+"or email IN('"+str(email)+"',"
        for x in account_email:
            qry += "'" + x + "',"
        qry = ''.join(qry.rsplit(qry[-1], 1))
        qry += ")"
        data=mm.select_direct_query(qry)
        if data:
            return render_template('user_register.html', msg='Already have an Account')
        else:
            maxin = mm.find_max_id("user_details")
            qry = ("insert into user_details values('" + str(maxin) + "','" + str(name) + "','" + str(
                contact) + "','" + str(email) + "','" + str(address) + "','" + str(gender) + "','" + str(
                dob) + "','" + str(password) + "','0','0')")
            result = mm.insert_query(qry)
        return render_template('user.html',flash_message=True,data="Success")
    return render_template('user_register.html')


@app.route("/user_friend_request", methods = ['GET', 'POST'])
def user_friend_request():
    if request.method == 'POST':
        username = request.form['username']
        dd=session['username']
        qry="select name,email from user_details where name='"+str(username)+"' and email NOT IN('"+str(dd)+"')"
        print(qry)
        data=mm.select_direct_query(qry)
        if data:
            return render_template('user_friend_request_1.html',items=data)
        else:
            return render_template('user_friend_request.html',msg='No User Found')
    return render_template('user_friend_request.html',msg='')





@app.route("/user_friend_request_2/<id>",methods = ['GET', 'POST'])
def user_friend_request_2(id):
    user=session['username']
    receiver=id
    maxin=mm.find_max_id("friends_details")
    mm.insert_query("insert into friends_details values('"+str(maxin)+"','"+str(user)+"','"+str(receiver)+"','1')")
    return render_template('user_friend_request.html', msg='Request Send')

def read_csv_file_data(subject):
    data=(subject.lower().strip()).split(' ')
    datalen=len((subject.lower().strip()).split(' '))
    file = 'static/dataset/data.csv'
    with open(file) as f:
        reader = csv.DictReader(f, delimiter=',')
        for row in reader:
            t1 = row['RSS News'].lower().strip()
            if t1 in data:
                return 1
        return 0







@app.route("/user_post_tweet", methods = ['GET', 'POST'])
def user_post_tweet():
    if request.method == 'POST':
        from datetime import datetime
        now = datetime.now()
        dt_string = now.strftime("%Y_%m_%d")
        dr_time=now.strftime("%H:%M:%S")
        user = session['username']
        subject = request.form['subject']
        f = request.files['file']
        f.save(os.path.join("static/uploads/", secure_filename(f.filename)))
        match_result=read_csv_file_data(subject)
        print(match_result)
        maxin = mm.find_max_id("tweet_details")
        qry = ("insert into tweet_details values('" + str(maxin) + "','" + str(user) + "','" + str(subject) + "','"+str(dt_string)+"','"+str(dr_time)+"','" + str(f.filename) + "','0','0','"+str(match_result)+"')")
        result = mm.insert_query(qry)
        # print(result)
        return render_template('user_post_tweet.html',msg='Success')
    return render_template('user_post_tweet.html',msg='')



@app.route("/user_message", methods = ['GET', 'POST'])
def user_message():
    dd = session['username']
    qry = "select user,receiver from friends_details where user='" + str(dd) + "' and status='1' or receiver='" + str(dd) + "' and status='1'"
    # print(qry)
    data = mm.select_direct_query(qry)
    # print(data)
    friends=[]
    for x in data:
        if x[0]==dd:
            friends.append(x[1])
        else:
            friends.append(x[0])
    if request.method == 'POST':
        if data:
            return render_template('user_message.html',items=data)
        else:
            return render_template('user_message.html',msg='No User Found')
    return render_template('user_message.html',friends=friends,msg='')



@app.route("/user_message_1/<id>",methods = ['GET', 'POST'])
def user_message_1(id):
    session['receiver']=id
    user=session['username']
    qry="select * from chat_details where sender='"+str(user)+"'and receiver='"+str(id)+"' and report='"+str(user)+"' and status='0' or sender='"+str(id)+"'and receiver='"+str(user)+"' and report='"+str(id)+"' and status='0'"
    print(qry)
    data=mm.select_direct_query(qry)
    return render_template('user_message_1.html', items=data)

@app.route("/user_message_2",methods = ['GET', 'POST'])
def user_message_2():
    now = datetime.now()
    print(now)
    dt_string = now.strftime("%Y_%m_%d")
    dr_time = now.strftime("%H:%M:%S")
    receiver=session['receiver']
    sender=session['username']

    if request.method == 'POST':
        txt = request.form['txt']
        match_result = read_csv_file_data(txt)
        maxin = mm.find_max_id("chat_details")
        qry = ("insert into chat_details values('" + str(maxin) + "','" + str(sender) + "','" + str(receiver) + "','" + str(txt) + "','" + str(dt_string) + "','" + str(dr_time) + "','"+str(match_result)+"','" + str(
            sender) + "')")
        print(qry)
        result = mm.insert_query(qry)
    return user_message_1(receiver)

def get_blocked_count(dd):
    dd = dd
    total = 0
    qry = "select * from tweet_details where user='" + str(dd) + "' and matching='1'"
    data = mm.select_direct_query(qry)
    if len(data) != "":
        total = len(data)
    # print(total)
    qry1 = "select * from chat_details where report='" + str(dd) + "' and status='1'"
    data1 = mm.select_direct_query(qry1)
    if len(data1) != "":
        total += len(data1)
    qry1 = "select * from comments_details where sender='" + str(dd) + "' and 	match_result='1'"
    data1 = mm.select_direct_query(qry1)
    if len(data1) != "":
        total += len(data1)
    return total

@app.route("/user_blocked_alert", methods = ['GET', 'POST'])
def user_blocked_alert():
    user = session['username']
    total=get_blocked_count(user)
    return render_template('user_blocked_alert.html', total=total)

@app.route("/admin_blocked_user", methods = ['GET', 'POST'])
def admin_blocked_user():
    data=mm.select_direct_query("select * from user_details")
    print(data)
    mtc=[]
    for x in data:
        total=get_blocked_count(x[3])
        if total>=2:
            a1=list(x)
            a1.append(total)
            mtc.append(a1)
    print(mtc)

    return render_template('admin_blocked_user.html', items=mtc)


@app.route("/admin_fake_tweet")
def admin_fake_tweet():
    qry="select * from tweet_details where matching='1'"
    data=mm.select_direct_query(qry)
    return render_template('admin_fake_tweet.html',items=data)


@app.route("/admin_add_dataset", methods = ['GET', 'POST'])
def admin_add_dataset():
    if request.method == 'POST':

        f = request.files['file']
        f.save(os.path.join("static/dataset/data.csv"))
        return render_template('admin_add_dataset.html', msg="Success")
    return render_template('admin_add_dataset.html', msg="")



@app.route("/user_home_commends/<id>",methods = ['GET', 'POST'])
def user_home_commends(id):
    session['pid']=id
    qry="select * from comments_details where pid='"+str(id)+"'and  match_result='0'"
    data=mm.select_direct_query(qry)
    return render_template('user_home_commends.html', items=data)


@app.route("/user_home_commends_1",methods = ['GET', 'POST'])
def user_home_commends_1():
    now = datetime.now()
    print(now)
    dt_string = now.strftime("%Y_%m_%d")
    dr_time = now.strftime("%H:%M:%S")
    sender=session['username']
    pid=session['pid']

    if request.method == 'POST':
        txt = request.form['txt']
        match_result = read_csv_file_data(txt)
        maxin = mm.find_max_id("comments_details")
        qry = ("insert into comments_details values('" + str(maxin) + "','" + str(pid) + "','" + str(sender) + "','" + str(txt) + "','" + str(dt_string) + "','" + str(dr_time) + "','"+str(match_result)+"','0','0')")
        result = mm.insert_query(qry)
    return user_home_commends(pid)

if __name__ == '__main__':
    # app.run(debug=True, use_reloader=True)
    app.run(host='0.0.0.0', port=4700,debug=True, use_reloader=True)