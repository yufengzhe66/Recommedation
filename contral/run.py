

from flask import Flask
from flask import abort
from flask import redirect
from flask import request,session
from flask import escape,flash
from flask import send_file
from flask import render_template,url_for



from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,SelectField,IntegerField,FloatField,FileField
from wtforms.validators import DataRequired,EqualTo,Length,NumberRange


import sys
sys.path.append(r"C:\Users\Dell\.spyder-py3\project_recommendation\base")
import sqlModel
import Pagination

import fileOperation

from datetime import datetime


app = Flask(__name__)

app.secret_key='itheima'


class userLoginForm(FlaskForm):
    username = StringField('username',validators=[DataRequired(),Length(min=4, max=25)])
    password = PasswordField('password',validators=[DataRequired()])
    submit = SubmitField('login')



class LoginForm(FlaskForm):
    username = StringField('username',validators=[DataRequired(),Length(min=4, max=25)])
    password = PasswordField('password',validators=[DataRequired()])
    submit = SubmitField('login')




class userRegisterForm(FlaskForm):
    gender = SelectField('gender',choices=[('男','男'),('女','女')])
    username = StringField('username',validators=[DataRequired(),Length(min=4,max=25)])
    password = PasswordField('password',validators=[DataRequired()])
    confirmpassword = PasswordField('confirmpassword',validators=[DataRequired(),EqualTo('password',message='Passwords must match')])
    age = IntegerField('age',validators=[DataRequired(),NumberRange(min=1,max=100)])
    submit = SubmitField('register')



class addBookForm(FlaskForm):
    bookname = StringField('name')
    bookprice = FloatField('price')
    bookauthor = StringField('author')
    booktype = StringField('type')
    bookpublishcorp = StringField('publishcorp')
    bookstock = IntegerField('stock')
    
    submit = SubmitField('Save')
  
    
    
class addressForm(FlaskForm):
    province = StringField('province')
    city = StringField('city')
    area = StringField('area')
    street = StringField('street')
    consignee = StringField('consignee')
    tel = IntegerField('tel')
    
    submit = SubmitField('添加收货地址')



@app.context_processor
def user_context_processor():
    user_id = session.get('u_id')
    if user_id:
        sqlsession = sqlModel.DBSession()
        user = sqlsession.query(sqlModel.User).filter(sqlModel.User.u_id == user_id).first()
        sqlsession.close()
        if user:
            return {'user':user}
    return {'user':None}
          
@app.context_processor
def admin_context_processor():
    admin_id = session.get('admin_id')
    if admin_id:
        sqlsession = sqlModel.DBSession()
        admin = sqlsession.query(sqlModel.admin).filter(sqlModel.admin.id == admin_id).first()
        sqlsession.close()
        if admin:
            return {'admin':admin}
    return {'admin':None}
    

"""
@app.context_processor
def book_context_processor():
    pass



@app.context_processor
def orderForm_context_processor():
    pass


"""

@app.route('/',methods=['POST','GET'])
def test():
    pass
    
    
    
    

@app.route('/addToorderform/bookid=<book_id>/amount=<amount>',methods=['POST','GET'])
def addToorderform(book_id,amount):
    userid = session.get('u_id')
    sqlsession = sqlModel.DBSession()
    today = datetime.today()
    orderformitem = sqlModel.OrderForm(u_id=userid,b_id=book_id,amount=amount,type=1,time=today)
    try:
        sqlsession.add(orderformitem)
        sqlsession.commit()
        sqlsession.query(sqlModel.Book).filter(book_id==sqlModel.Book.b_id).update({sqlModel.Book.b_stock:sqlModel.Book.b_stock-amount,sqlModel.Book.b_totalSold:sqlModel.Book.b_totalSold+amount})
        sqlsession.commit()
        sqlsession.close()
    except Exception as e:
        sqlsession.rollback() 
        sqlsession.close()
    return redirect(url_for('.userbooks'))




@app.route('/addtocart/<book_id>',methods=['POST','GET'])
def addtocart(book_id):
    if request.method == 'POST':
        amount = request.form.get('bookNum')
        userid = session.get('u_id')
        sqlsession = sqlModel.DBSession()
        book = sqlsession.query(sqlModel.Book).filter(sqlModel.Book.b_id==book_id).first()
        user = sqlsession.query(sqlModel.User).filter(sqlModel.User.u_id==userid).first()
        address = user.u_address
#        orderformitem =  sqlModel.OrderForm(u_id=userid,b_id=book_id,amount=amount)
        totalPrice=float(amount)*book.b_price
        sqlsession.close()
        return render_template('/userpayforbook.html',posts=book,amount=amount,totalPrice=totalPrice,address=address)

    
@app.route('/addTocommnet',methods = ['POST','GET'])
def addTocomment():
    if request.method == 'POST':
        userid = session.get('u_id')
        bookid = request.form.get('bookId')
        comment = request.form.get('content')
        starNum = request.form.get('starNum')
        rate = float(starNum)
        fileOperation.writeTofile(userid,bookid,rate)
        sqlsession = sqlModel.DBSession()
        sqlsession.query(sqlModel.OrderForm).filter(sqlModel.OrderForm.u_id==userid).filter(sqlModel.OrderForm.b_id==bookid).update({sqlModel.OrderForm.rate:rate , sqlModel.OrderForm.comment:comment},synchronize_session='fetch')
        
        sqlsession.commit()
        sqlsession.close()
        return redirect(url_for('.usertocomment',bookid=bookid))
        



    

   
@app.route('/addbooknum/<book_id>',methods=['GET','POST'])
def addbooknum(book_id):
    if request.method == 'POST':
        sqlsession = sqlModel.DBSession()
        amount = request.form.get('num')
        sqlsession.query(sqlModel.Book).filter(book_id==sqlModel.Book.b_id).update({sqlModel.Book.b_stock:sqlModel.Book.b_stock+amount})
        sqlsession.commit()
        return redirect(url_for('.editbook'))



@app.route('/index',methods=['POST','GET'])
def index():
    return render_template(('/index.html'))

@app.route('/changeadmininfo',methods=['POST','GET'])
def changeadmininfo():
    login_form = LoginForm()
    if request.method == 'POST':
        adminname=request.form.get('username')
        password=request.form.get('password')
        if login_form.validate_on_submit():
            sqlsession = sqlModel.DBSession()
            sqlsession.query(sqlModel.admin).filter(adminname==sqlModel.admin.name).update({sqlModel.admin.password:password})
            sqlsession.commit()
            sqlsession.close()
            flash("修改成功！！！")
    return render_template("/changeadmininfo.html",form=login_form)  
    
    


@app.route('/addbook',methods=['POST','GET'])
def addbook():
    bookForm = addBookForm()
    if request.method == 'POST':
        bookname = request.form.get('name')
        bookprice = request.form.get('price')
        bookauthor = request.form.get('author')
        booktype = request.form.get('type')
        bookpublishcorp = request.form.get('publishcorp')
        bookstock = request.form.get('stock')
        
                
        if bookForm.validate_on_submit():
           sqlsession = sqlModel.DBSession()
           book = sqlsession.query(sqlModel.Book).filter(sqlModel.Book.b_name==bookname).first() 
           if book:
               flash('此书已存在')
               sqlsession.close()
           else:    
               id=sqlsession.query(sqlModel.Book).count()+1
               today = datetime.today()
               item=sqlModel.Book(b_id=id,b_name=bookname,b_author=bookauthor,b_publish=bookpublishcorp,b_type=booktype,b_price=bookprice,b_stock=bookstock,b_totalSold=0,b_date=today)
               try:
                   sqlsession.add(item)
                   sqlsession.commit()
                   sqlsession.close()
                   flash('添加成功！')
               except Exception as e:
                   flash("添加失败！！！")
                   sqlsession.rollback() 
        else:
            flash("信息不完整！！！") 
    return render_template('/addbook.html',form=bookForm)


@app.route('/adminuserlist',methods=['GET','POST'])
def adminuserlist():
    sqlsession = sqlModel.DBSession()
    #从get方法中取得页码
    page = request.args.get('page', 1, type = int)
    #获取pagination对象
    pagination = sqlsession.query(sqlModel.User).order_by(sqlModel.User.u_id).paginate(page, per_page=10, error_out = False)

    #pagination对象的items方法返回当前页的内容列表
    sqlsession.close()
    posts = pagination.items
    return render_template('/adminuserlist.html',  posts=posts ,pagination=pagination)





@app.route('/userlogin',methods=['POST','GET'])
def userlogin():
    login_form = userLoginForm()
    if request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')
        if login_form.validate_on_submit():
            sqlsession = sqlModel.DBSession()
            user = sqlsession.query(sqlModel.User).filter(sqlModel.User.u_name==username).first()
            if not user:
                flash("此用户不存在")
            elif user.u_password==password:
                session['u_id'] = user.u_id
                return redirect(url_for('.userdata'))
            else:
                flash("用户名密码不匹配")
   
            sqlsession.close() 
        else:
            flash('参数有误')
    return render_template("/userlogin.html",form=login_form) 


@app.route('/userlogout',methods=['GET','POST'])
def userlogout():
    session.clear()
    return redirect(url_for('.userlogin'))



@app.route('/editbook',methods=['POST','GET'])
def editbook():
    sqlsession = sqlModel.DBSession()
    #从get方法中取得页码
    page = request.args.get('page', 1, type = int)
    #获取pagination对象
    pagination = sqlsession.query(sqlModel.Book).order_by(sqlModel.Book.b_date.desc()).paginate(page, per_page=10, error_out = False)
    #pagination对象的items方法返回当前页的内容列表
    posts = pagination.items     
    sqlsession.close()
    return render_template('/editbook.html',  posts=posts ,pagination=pagination)




@app.route('/orderinfo',methods=['POST','GET'])
def orderinfo():  
    sqlsession = sqlModel.DBSession()
    #从get方法中取得页码
    page = request.args.get('page', 1, type = int)
    #获取pagination对象
    pagination = sqlsession.query(sqlModel.OrderForm.id,sqlModel.OrderForm.b_id,sqlModel.OrderForm.u_id,sqlModel.OrderForm.time,sqlModel.OrderForm.type,sqlModel.User.u_name,sqlModel.User.u_address,sqlModel.Book.b_name).join(sqlModel.User,sqlModel.User.u_id==sqlModel.OrderForm.u_id).join(sqlModel.Book,sqlModel.Book.b_id==sqlModel.OrderForm.b_id).order_by(sqlModel.OrderForm.time).paginate(page, per_page=10, error_out = False)
    
    #pagination对象的items方法返回当前页的内容列表
    sqlsession.close()
    posts = pagination.items
    return render_template('/orderinfo.html', posts=posts ,pagination=pagination)
   

  


@app.route('/useraddaddress',methods=['POST','GET'])
def useraddaddress():
    
    addressform = addressForm()
    if request.method == 'POST':
        province = request.form.get('province')
        city = request.form.get('city')
        area = request.form.get('area')
        street = request.form.get('street')
        realname = request.form.get('consignee')
        tel = request.form.get('tel')
        address=province+city+area+street
        u_id = session.get('u_id')
        if u_id:
           sqlsession = sqlModel.DBSession()
           sqlsession.query(sqlModel.User).filter(u_id==sqlModel.User.u_id).update({sqlModel.User.u_address:address, sqlModel.User.realname:realname, sqlModel.User.tel:tel})
           sqlsession.commit()
           sqlsession.close()
           flash('添加成功')
        else:
            flash('添加失败！')
    return render_template('/useraddaddress.html',form = addressform)
    
    


@app.route('/userbooks',methods=['POST','GET'])
def userbooks():
    sqlsession = sqlModel.DBSession()
    userid = session.get('u_id')
    page = request.args.get('page', 1, type = int)
    pagination = sqlsession.query(sqlModel.Book.b_id,sqlModel.Book.b_type,sqlModel.Book.b_author,sqlModel.Book.b_name,sqlModel.Book.b_price,sqlModel.Book.b_publish,sqlModel.OrderForm.rate).filter(sqlModel.OrderForm.u_id==userid ).filter(sqlModel.OrderForm.b_id==sqlModel.Book.b_id).order_by(sqlModel.OrderForm.time).paginate(page, per_page=10, error_out = False)
    
    #pagination对象的items方法返回当前页的内容列表
    sqlsession.close()
    posts = pagination.items
    
    
    return render_template('/userbooks.html', posts=posts ,pagination=pagination )
    





@app.route('/userbookindex',methods=['POST','GET'])
def userbookindex():
    sqlsession = sqlModel.DBSession()
    #从get方法中取得页码
    page = request.args.get('page', 1, type = int)
    #获取pagination对象
    pagination = sqlsession.query(sqlModel.Book).order_by(sqlModel.Book.b_date).paginate(page, per_page=10, error_out = False)

    #pagination对象的items方法返回当前页的内容列表
    sqlsession.close()
    posts = pagination.items
    return render_template('/userbookindex.html',  posts=posts ,pagination=pagination)
    




@app.route('/userdata',methods=['POST','GET'])
def userdata():
    userid = session.get('u_id')
    sqlsession = sqlModel.DBSession()
    book1=sqlsession.query(sqlModel.Book.b_id,sqlModel.Book.b_name,sqlModel.Book.b_stock).filter(sqlModel.Recommendation.u_id==userid).filter(sqlModel.Book.b_id==sqlModel.Recommendation.recommendation1).first()
    book2=sqlsession.query(sqlModel.Book.b_id,sqlModel.Book.b_name,sqlModel.Book.b_stock).filter(sqlModel.Recommendation.u_id==userid).filter(sqlModel.Book.b_id==sqlModel.Recommendation.recommendation2).first()
    book3=sqlsession.query(sqlModel.Book.b_id,sqlModel.Book.b_name,sqlModel.Book.b_stock).filter(sqlModel.Recommendation.u_id==userid).filter(sqlModel.Book.b_id==sqlModel.Recommendation.recommendation3).first()
    book4=sqlsession.query(sqlModel.Book.b_id,sqlModel.Book.b_name,sqlModel.Book.b_stock).filter(sqlModel.Recommendation.u_id==userid).filter(sqlModel.Book.b_id==sqlModel.Recommendation.recommendation4).first()
    book5=sqlsession.query(sqlModel.Book.b_id,sqlModel.Book.b_name,sqlModel.Book.b_stock).filter(sqlModel.Recommendation.u_id==userid).filter(sqlModel.Book.b_id==sqlModel.Recommendation.recommendation5).first()   
      
    return render_template('/userdata.html',book1=book1,book2=book2,book3=book3,book4=book4,book5=book5)


@app.route('/userpayforbook',methods=['POST','GET'])
def userpayforbook():
    
    return render_template('/userpayforbook.html')


@app.route('/userregister',methods=['POST','GET'])
def userregister():
    register_form = userRegisterForm()
   
    if request.method == 'POST':
        gender=request.form.get('gender')
        username=request.form.get('username')
        password=request.form.get('password')
 #       confirmpassword=request.form.get('confirmpassword')
        age = request.form.get('age')
 
        if register_form.validate_on_submit():
            sqlsession = sqlModel.DBSession()
            user = sqlsession.query(sqlModel.User).filter(sqlModel.User.u_name==username).first()   
            if user:
                flash('此用户名已被使用')
                sqlsession.close()
            else:    
                id=sqlsession.query(sqlModel.User).count()+1
                item=sqlModel.User(u_id=id,u_name=username,u_password=password,u_age=age,u_sex=gender,u_address='NULL')
                item1=sqlModel.Recommendation(u_id=id)
                try:
                    sqlsession.add(item)
                    sqlsession.commit()
                    sqlsession.add(item1)
                    sqlsession.commit()
                    sqlsession.close()
                except Exception as e:
                    flash("注册失败！！！")
                    sqlsession.rollback()
                context = { 'gender':gender,
                 'name':username,
                 'age':age
                  }
            
                return render_template("/userregistersuccess.html",**context)
        else:
            flash('参数有误')
    return render_template("/userregister.html",form=register_form)         
   

@app.route('/login',methods=['POST','GET'])    
def login():
    login_form = LoginForm()
    if request.method == 'POST':
        username=request.form.get('username')
        password=request.form.get('password')
        if login_form.validate_on_submit():
            sqlsession = sqlModel.DBSession()
            user = sqlsession.query(sqlModel.admin).filter(sqlModel.admin.name==username).first()
            if not user:
                flash("此用户不存在")
            elif user.password==password:
                session['admin_id'] = user.id
                return redirect(url_for('.index'))
            else:
                flash("用户名密码不匹配")
   
            sqlsession.close() 
        else:
            flash('参数有误')
    return render_template("/login.html",form=login_form)     



@app.route('/logout',methods=['GET','POST'])
def logout():
    session.clear()
    return redirect(url_for('.login'))





@app.route('/userregistersuccess',methods=['POST','GET'])
def userregistersuccess():
    return render_template('/userregistersuccess.html')


@app.route('/usertocomment/<bookid>',methods=['POST','GET'])
def usertocomment(bookid):
    userid = session.get('u_id')
    sqlsession = sqlModel.DBSession()
    book = sqlsession.query(sqlModel.Book).filter(sqlModel.Book.b_id==bookid).first()
    
    sqlsession.close()
    return render_template('/usertocomment.html',book=book)
    
    


@app.route('/user/<name>')
def sayHello(name):
    if name == 'baidu':
        return redirect('http://www.baidu.com')
    elif name == 'NO':
        return abort(401)
        
        
    return '<h1> Hello,%s </h1>' % name


   

if __name__ == '__main__':
    app.run(host="127.0.0.1", port=8080,debug=True)
    
