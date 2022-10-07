from flask import Flask,render_template,request, flash,redirect, url_for, jsonify
from config_file import client
from models import *
import secrets
import datetime
from bson import ObjectId
# from datetime import datetime
from random import randint
import os
app = Flask(__name__)

app.secret_key='my_key'
UPLOAD_FOLDER = 'static/images/wellness/hs'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

UPLOAD_FOLDER_PERMISSION = 'static/images/wellness/permission_letter'
app.config['UPLOAD_FOLDER_PERMISSION'] = UPLOAD_FOLDER_PERMISSION

ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif','mp4'}

# @app.route("/")
# def buttonPage():
#     return render_template('button.html')
# @app.route("/launch",methods=['POST','GET'])
# def launchPage():
#     return render_template('launch.html')
@app.route("/")
def indexPage():
    return render_template('index.html')
# @app.route("/launch",methods=['POST','GET'])
# def launchPage():
#     return render_template('launch.html')

@app.route("/academicStaff",methods=['POST','GET'])
def academicStaffPage():
    return render_template('academic_staff.html')

@app.route("/codingStaff",methods=['POST','GET'])
def codingStaffPage():
    return render_template('coding_staff.html')

@app.route("/timetable",methods=['POST','GET'])
def timetablePage():
    return render_template('time_table_buttons.html')

@app.route("/timetable6A",methods=['POST','GET'])
def timetable6APage():
    return render_template('timetable/time_table_6a.html')

@app.route("/timetable6B",methods=['POST','GET'])
def timetable6BPage():
    return render_template('timetable/time_table_6b.html')

@app.route("/timetable7A",methods=['POST','GET'])
def timetable7APage():
    return render_template('timetable/time_table_7a.html')

@app.route("/timetable7B",methods=['POST','GET'])
def timetable7BPage():
    return render_template('timetable/time_table_7b.html')

@app.route("/timetable8A",methods=['POST','GET'])
def timetable8APage():
    return render_template('timetable/time_table_8a.html')

@app.route("/timetable8B",methods=['POST','GET'])
def timetable8BPage():
    return render_template('timetable/time_table_8b.html')

@app.route("/timetable9A1",methods=['POST','GET'])
def timetable9A1Page():
    return render_template('timetable/time_table_9a1.html')


@app.route("/timetable9A2",methods=['POST','GET'])
def timetable9A2Page():
    return render_template('timetable/time_table_9a2.html')

@app.route("/timetable9B1",methods=['POST','GET'])
def timetable9B1Page():
    return render_template('timetable/time_table_9b1.html')

@app.route("/timetable9B2",methods=['POST','GET'])
def timetable9B2Page():
    return render_template('timetable/time_table_9b2.html')

@app.route("/timetable10A",methods=['POST','GET'])
def timetable10APage():
    return render_template('timetable/time_table_10a.html')

@app.route("/timetable10B",methods=['POST','GET'])
def timetable10BPage():
    return render_template('timetable/time_table_10b.html')

@app.route('/houseMasterRegister',methods=['POST','GET'])
def houseMasterRegisterPage():
    houseMasterFirstName = request.form.get('houseMasterFirstName')
    houseMasterLastName = request.form.get('houseMasterLastName')
    houseClass = request.form.get('houseClass')
    emailId = request.form.get('emailId')
    phoneNumber = request.form.get('phoneNumber')
    refLink = secrets.token_urlsafe()
    password = request.form.get("password")
    houseMasterId = request.form.get('houseMasterId')
    compOfLeaves = 0
    paidLeaves = 6
    casualLeaves = 12
    status = 1
    createdOn = datetime.datetime.now()

    if request.method == 'POST':
        try:
            queryset = HouseMaster.objects(emailId__iexact=emailId)
            if queryset:
                flash("Email already Exists!!!")
                return render_template("teacher_register.html")
        except Exception as e:
            pass

        try:
            queryset = HouseMaster.objects(houseClass__iexact=houseClass)
            if queryset:
                flash("Already "+houseClass+" assigned to someone!!!")
                return render_template("teacher_register.html")
        except Exception as e:
            pass
        house_master = HouseMaster(
            houseMasterFirstName=houseMasterFirstName,
            houseMasterLastName=houseMasterLastName,
            houseClass=houseClass,
            emailId = emailId,
            phoneNumber = phoneNumber,
            refLink = refLink,
            houseMasterId = houseMasterId,
            compOfLeaves = compOfLeaves,
            paidLeaves = paidLeaves,
            casualLeaves = casualLeaves,
            password=password,
            status=status,
            createdOn=createdOn
            )
        house_details = house_master.save()
        if house_details:
            flash("Registration Successfully Completed!!!.")
            return redirect(url_for('houseMasterLoginPage'))
    else:
        return render_template("teacher_register.html")

@app.route('/houseMasterLogin',methods=['POST','GET'])
def houseMasterLoginPage():
    emailId = request.form.get('emailId')
    password = request.form.get('password')

    if emailId and password and request.method=='POST':
        try:
            get_logins = HouseMaster.objects.get(emailId__iexact=emailId,password__exact=password,status__in=[1])
            if get_logins:
                refLink = get_logins.refLink
                # house_master = get_logins.houseMasterFirstName +" "+ get_logins.houseMasterLastName
                # print(house_master)
                return redirect(url_for('studentAmountPage',refLink=refLink))
            else:
                flash("Invalid Credentials!!!")
                return render_template("teacher_login.html")
        except HouseMaster.DoesNotExist as e:
            flash("Invalid Credentials!!!")
            return render_template("teacher_login.html")

    return render_template('teacher_login.html')

@app.route('/houseMasterForgotPassword',methods=['POST','GET'])
def houseMasterForgotPasswordPage():
    emailId = request.form.get("emailId")
    newPassword = request.form.get("newPassword")
    confirmPassword = request.form.get("confirmPassword")
    

    if emailId and newPassword and confirmPassword and request.method=="POST":
        if newPassword==confirmPassword:
            get_master_info = HouseMaster.objects.get(emailId=emailId)
            # print(get_student_info["emailId"])
            if get_master_info.emailId:
                updated_password=get_master_info.update(
                    password=newPassword
                    )
                if updated_password:
                    flash("Password Successfully Changed")
                    return redirect(url_for('houseMasterLoginPage'))
            
        else:
            flash("Password Miss Matched")
            return render_template('teacher_forgot_password.html')
    
    return render_template('teacher_forgot_password.html')

@app.route("/houseMasterLogout",methods=['POST','GET'])
def houseMasterLogoutPage():
    return redirect(url_for('houseMasterLoginPage'))


@app.route("/studentAmount/<refLink>",methods=['POST','GET'])
def studentAmountPage(refLink):
    get_students_details = AmountBank.objects()
    
    students_list=[]
    student_dict={}
    count=0
    get_name = HouseMaster.objects.get(refLink=refLink)
    # print(get_name.houseMasterFirstName)
    houseMaster = get_name.houseMasterFirstName +" "+ get_name.houseMasterLastName
    for s in get_students_details:
        if s.refLink==refLink:
            # houseMasterName = get_students_details = AmountBank.objects.get()
            count=count+1
            student_dict={
                "rno":count,
                "studentName":s.studentName,
                "className":s.className,
                "studentTotalAmount":s.studentTotalAmount,
                "link":s.link,
                # "houseMasterName":houseMasterName
            }
            students_list.append(student_dict)
    return render_template('students_view.html',students_info=students_list,refLink=refLink,houseMaster=houseMaster)

@app.route("/studentRegister/<refLink>",methods=['POST','GET'])
def studentRegPage(refLink):
    studentName = request.form.get('studentName')
    className = request.form.get('className')
    studentTotalAmount = request.form.get('studentTotalAmount')
    link = secrets.token_urlsafe()
    status = 1
    createdOn = datetime.datetime.now()
    
    try:
        if request.method == 'POST':
            get_house_master = HouseMaster.objects.get(refLink=refLink)
            students_details = AmountBank(
                studentName=studentName,
                className=className,
                studentTotalAmount=studentTotalAmount,
                link=link,
                houseMasterName = get_house_master.houseMasterFirstName+" "+get_house_master.houseMasterLastName,
                refLink=get_house_master.refLink,
                status=status,
                createdOn = createdOn,
                
                )
            students_details_data= students_details.save()
            if students_details_data:
                flash("Successfully Registered!!!")
                return redirect(url_for('studentAmountPage',refLink=refLink))
            else:
                flash("Required fields are missing!!!")
                return render_template('student_register.html')
    except Exception as e:
        print(e)
    return render_template("student_register.html")



@app.route("/amountDebit/<link>",methods=['POST','GET'])
def amountDebitPage(link):
    debitAmount=request.form.get('debitAmount')
    reasonTaking = request.form.get('reasonTaking')
    takenDebitDate = request.form.get('takenDebitDate')
    amountDebitStatus=2
    createdOn = datetime.datetime.now()
    if request.method=="POST":
        get_data=AmountBank.objects.get(link=link)
        if get_data:
            refLink = get_data.refLink
            total_amount=get_data.studentTotalAmount
            debit_amount = total_amount - int(debitAmount)
            student_trans = StudentTransaction(
                studentId=ObjectId(get_data.id),
                studentName = get_data.studentName,
                debitAmount=debitAmount,
                reasonTaking=reasonTaking,
                takenDebitDate=takenDebitDate,
                amountDebitStatus=amountDebitStatus,
                link=get_data.link,
                createdOn=createdOn,
                )
            student_trans_save=student_trans.save()
            if student_trans_save: 
                student_credit=get_data.update(
                    studentTotalAmount=debit_amount
                    )
                if student_credit:
                    flash("{}, Successfully {} rupees Debited from your wallet".format(student_trans_save.studentName,debitAmount))
                    return redirect(url_for('studentAmountPage',refLink=refLink))
    return render_template('debit.html')

@app.route("/amountCredit/<link>",methods=['POST','GET'])
def amountCreditPage(link):
    creditAmount=request.form.get('creditAmount')
    takenCreditDate = request.form.get('takenCreditDate')
    amountCreditStatus=3
    createdOn = datetime.datetime.now()
    if request.method=="POST":
        get_data=AmountBank.objects.get(link=link)
        if get_data:
            refLink = get_data.refLink
            total_amount=get_data.studentTotalAmount
            credit_amount = total_amount + int(creditAmount)
            student_trans = StudentTransaction(
                studentId=ObjectId(get_data.id),
                studentName = get_data.studentName,
                creditAmount=creditAmount,
                takenCreditDate=takenCreditDate,
                amountCreditStatus=amountCreditStatus,
                link=get_data.link,
                createdOn=createdOn
                )
            student_trans_save=student_trans.save()
            if student_trans_save: 
                student_credit=get_data.update(
                    studentTotalAmount=credit_amount
                    )
                if student_credit:
                    flash("{}, Successfully {} rupess Credited to your wallet".format(student_trans_save.studentName,creditAmount))
                    return redirect(url_for('studentAmountPage',refLink=refLink))
    return render_template('credit.html')

@app.route("/viewStudentsTransactionReports/<link>",methods=['POST','GET'])
def viewStudentsTransactionReportsPage(link):
    if request.method=="GET":
        get_transaction=AmountBank.objects.get(link=link)
        if get_transaction.link==link:
            get_students_trans = StudentTransaction.objects(link=link).all()
            # print(get_students_trans)
            trans_list=[]
            trans_dict={}
            count=0
            for st in get_students_trans:
                count=count + 1
                if st.amountDebitStatus == 2 or st.amountCreditStatus== 3:
                    trans_dict={
                        "sno":count,
                        "debitAmount":st.debitAmount,
                        "reasonTaking":st.reasonTaking,
                        "takenDebitDate":st.takenDebitDate,
                        "amountDebitStatus":st.amountDebitStatus,
                        "creditAmount":st.creditAmount,
                        "takenCreditDate":st.takenCreditDate,
                        "amountCreditStatus":st.amountCreditStatus

                    }
                    trans_list.append(trans_dict)

        return render_template('student_reports.html',trans_list=trans_list,link=link)

@app.route("/viewStudentsTransactionDate/<link>",methods=['POST','GET'])
def viewStudentsTransactionDateReportsPage(link):
    if request.method=="POST":
        student_dict={}
        student_list=[]
        fromDate = request.form.get('fromDate')
        toDate = request.form.get('toDate')
        if fromDate and toDate and request.method=='POST':
            
            get_transaction=AmountBank.objects.get(link=link)
            if get_transaction.link==link:
                get_students_trans_details = StudentTransaction.objects.filter(link=link,createdOn__in=[fromDate,toDate])
                if get_students_trans_details:
                    
                    count = 0
                    for st in get_students_trans_details:
                        count=count+1
                        if st.amountDebitStatus == 2 or st.amountCreditStatus== 3:
                            student_dict={
                            "sno":count,
                            "debitAmount":st.debitAmount,
                            "reasonTaking":st.reasonTaking,
                            "takenDebitDate":st.takenDebitDate,
                            "amountDebitStatus":st.amountDebitStatus,
                            "creditAmount":st.creditAmount,
                            "takenCreditDate":st.takenCreditDate,
                            "amountCreditStatus":st.amountCreditStatus
                            }
                        student_list.append(student_dict)
    return render_template('student_reports.html',student_list=student_list,link=link)




@app.route("/updateStudentDetails/<link>",methods=['POST','GET'])
def updateStudentDetailsPage(link):
    studentName = request.form.get('studentName')
    className = request.form.get('className')
    studentTotalAmount = request.form.get('studentTotalAmount')
    # try:
    if request.method == 'POST':
        get_student = AmountBank.objects.get(link=link)
        get_house_master = HouseMaster.objects.get(refLink=get_student.refLink)
        students_details = get_student.update(
            studentName=studentName,
            className=className,
            studentTotalAmount=studentTotalAmount
            )
        if students_details:
            flash("Successfully Registered!!!")
            return redirect(url_for('studentAmountPage',refLink=get_student.refLink))
    # except Exception as e:
    #     print(e)            
        
    return render_template('update_student.html')

@app.route("/deleteStudentDetails/<link>",methods=['POST','GET'])
def deleteStudentDetailsPage(link):
    pass


@app.route("/applyLeaveLogin",methods=['POST','GET'])
def applyLeaveLoginPage():
    emailId = request.form.get('emailId')
    password = request.form.get('password')

    if emailId and password and request.method=='POST':
        try:
            get_logins = HouseMaster.objects.get(emailId__iexact=emailId,password__exact=password,status__in=[1])
            if get_logins:
                refLink = get_logins.refLink
                # house_master = get_logins.houseMasterFirstName +" "+ get_logins.houseMasterLastName
                # print(house_master)
                 
                
                return redirect(url_for('applyLeavePage',refLink=refLink))
            else:
                flash("Invalid Credentials!!!")
                return render_template("teacher_login.html")
        except HouseMaster.DoesNotExist as e:
            flash("Invalid Credentials!!!")
            return render_template("teacher_login.html")

    return render_template('teacher_login.html')

@app.route("/applyLeave/<refLink>",methods=['POST','GET'])
def applyLeavePage(refLink):
    if request.method == 'POST':
        trainerName = request.form.get('trainerName')
        leaveType = request.form.get('leaveType')
        fromDate = request.form.get('fromDate')
        toDate = request.form.get('toDate')
        hrEmail = request.form.get('hrEmail')
        accountEmail = request.form.get('accountEmail')
        managerEmail = request.form.get('managerEmail')
        reasonApply = request.form.get('reasonApply')
        applyDate = datetime.datetime.now()
        status = 1
        createdOn = datetime.datetime.now()

        if request.method == 'POST':
            get_data=HouseMaster.objects.get(refLink=refLink)
            leave_apply = ApplyLeave(
                trainerName=trainerName,
                leaveType = leaveType,
                fromDate = fromDate,
                toDate = toDate,
                hrEmail = hrEmail,
                accountEmail = accountEmail,
                managerEmail = managerEmail,
                reasonApply = reasonApply,
                houseMasterId = ObjectId(get_data.id),
                refLink = get_data.refLink,
                applyDate = applyDate,
                status = status,
                createdOn = createdOn
                )
            leaves_saved = leave_apply.save()
            if leaves_saved:
                from_date = datetime.datetime.strptime(leaves_saved.fromDate, "%Y-%m-%d")
                to_date = datetime.datetime.strptime(leaves_saved.toDate, "%Y-%m-%d")
                
                no_of_leaves = to_date - from_date
                # no_of_leaves
                print(f'Difference is {delta.days} days')

                # year_diff = (to_date.year - from_date.year)
                # month_diff = (to_date.month - from_date.month)
                # day_diff = (to_date.day - from_date.day)

                # print(year_diff,month_diff,day_diff)
                # day, month, year = (int(i) for i in leaves_saved.fromDate.split(' '))
                # print(day, month, year)
                # leaves_info = leaves_saved.fromDate - leaves_saved.toDate

                # print(leaves_info)
                # get_leaves=HouseMaster.objects.get(refLink=refLink)
                # if leaveType == get_leaves.casualLeaves:

                #     leaves_update = get_leaves.update(leaveType)
    leaves ={}
    if request.method == 'GET':
        get_leaves = HouseMaster.objects.get(refLink=refLink,status__in=[1])
        if get_leaves:
            leaves={
                "compOfLeaves":get_leaves.compOfLeaves,
                "paidLeaves":get_leaves.paidLeaves,
                "casualLeaves":get_leaves.casualLeaves,
                "totalLeaves" :get_leaves.compOfLeaves + get_leaves.paidLeaves + get_leaves.casualLeaves
            }


    return render_template('apply_leave.html',leaves=leaves)

@app.route('/wellness/hs/<filename>')
def send_uploaded_file(filename=''):
    from flask import send_from_directory
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)

@app.route('/wellness/permission_letter/<filename>')
def send_uploaded_file_pl(filename=''):
    from flask import send_from_directory
    return send_from_directory(app.config["UPLOAD_FOLDER_PERMISSION"], filename)


@app.route("/wellnessCenterRegistration",methods=['POST','GET'])
def wellnessCenterRegistrationPage():
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    emailId = request.form.get('emailId')
    phoneNumber = request.form.get('phoneNumber')
    password = request.form.get('password')
    hsRefLink = secrets.token_urlsafe()
    createdOn = datetime.datetime.now()
    status = 1
    if request.method == 'POST':
        try:
            queryset = WellnessCenterRegistration.objects(emailId__iexact=emailId)
            if queryset:
                flash("User already Exists!!")
                return render_template("wellness/health/hs_register.html")
        except Exception as e:
            pass
        add_well_data = WellnessCenterRegistration(
            firstName = firstName,
            lastName = lastName,
            emailId = emailId,
            phoneNumber = phoneNumber,
            password = password,
            hsRefLink = hsRefLink,
            createdOn = createdOn,
            status = status
            )
        hs_reg_data = add_well_data.save()
        hs_reg_id = str(hs_reg_data.id)
        if hs_reg_id:
            profilePic = request.files['profilePic']
            if profilePic.filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS:
                ext = profilePic.filename.rsplit('.',1)[1].lower()
                file_name = str(hs_reg_id)+"."+ext
                if not os.path.exists(app.config['UPLOAD_FOLDER']):
                    os.mkdir(app.config['UPLOAD_FOLDER'])
                profile = app.config['UPLOAD_FOLDER']
                profilePic.save(os.path.join(profile,file_name))
            hs_reg_data.update(profilePic=file_name)
        if hs_reg_data:
            flash("Registration Successfully Done!!")
            return redirect(url_for('wellnessCenterPage'))
        else:
            flash("Required fields are missing !!!")
            return render_template('wellness/health/hs_register.html')
    else:
        return render_template('wellness/health/hs_register.html')

@app.route("/wellnessCenter",methods=['POST','GET'])
def wellnessCenterPage():
    emailId = request.form.get('emailId')
    password = request.form.get('password')

    if emailId and password and request.method=='POST':
        try:
            get_hs_logins = WellnessCenterRegistration.objects.get(emailId__iexact=emailId,password__exact=password,status__in=[1])
            if get_hs_logins:
                hsRefLink = get_hs_logins.hsRefLink
                return redirect(url_for('wellnessCenterDashboardPage',hsRefLink=hsRefLink))
            else:
                flash("Invalid Credentials!!!")
                return render_template("wellness/health/hs_login.html")
        except WellnessCenterRegistration.DoesNotExist as e:
            flash("Invalid Credentials!!!")
            return render_template("wellness/health/hs_login.html")
    return render_template('wellness/health/hs_login.html')

@app.route('/wellnessHsForgotPassword',methods=['POST','GET'])
def wellnessHsForgotPasswordPage():
    emailId = request.form.get("emailId")
    newPassword = request.form.get("newPassword")
    confirmPassword = request.form.get("confirmPassword")
    

    if emailId and newPassword and confirmPassword and request.method=="POST":
        if newPassword==confirmPassword:
            get_hs_info = WellnessCenterRegistration.objects.get(emailId=emailId)
            if get_hs_info.emailId:
                updated_password=get_hs_info.update(
                    password=newPassword
                    )
                if updated_password:
                    flash("Password Successfully Changed")
                    return redirect(url_for('wellnessCenterPage'))
            
        else:
            flash("Password Miss Matched")
            return render_template('wellness/health/hs_forgot_password.html')
    
    return render_template('wellness/health/hs_forgot_password.html')

@app.route("/dailySickRegister/<hsRefLink>",methods=['POST','GET'])
def dailySickRegisterPage(hsRefLink):
    studentName = request.form.get('studentName')
    className = request.form.get('className')
    rollNumber = request.form.get('rollNumber')
    diseaseName = request.form.get('diseaseName')
    date = request.form.get('date')
    time = request.form.get('time')
    day = request.form.get('day')
    medicineIssued = request.form.get('medicineIssued')
    studentRefLink = secrets.token_urlsafe()
    createdOn = datetime.datetime.now()

    status = 1
    
    if request.method == 'POST':
        hs_ref_link = WellnessCenterRegistration.objects.get(hsRefLink=hsRefLink)
        student_daily_sick = StudentDailySickRegistration(
            studentName=studentName,
            className=className,
            rollNumber=rollNumber,
            diseaseName=diseaseName,
            date=date,
            time=time,
            day=day,
            medicineIssued=medicineIssued,
            hsRefLink = hs_ref_link.hsRefLink,
            studentRefLink=studentRefLink,
            hsId = str(hs_ref_link.id),
            hsName = hs_ref_link.firstName+" "+hs_ref_link.lastName,
            createdOn=createdOn,
            status=status
            )
        student_daily_sick_info = student_daily_sick.save()
        student_sick_id = str(student_daily_sick_info.id)
        if student_sick_id:
            permissionLetter = request.files['permissionLetter']
            if permissionLetter.filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS:
                ext = permissionLetter.filename.rsplit('.',1)[1].lower()
                file_name = str(student_sick_id)+"."+ext
                if not os.path.exists(app.config['UPLOAD_FOLDER_PERMISSION']):
                    os.mkdir(app.config['UPLOAD_FOLDER_PERMISSION'])
                permssion_letter = app.config['UPLOAD_FOLDER_PERMISSION']
                permissionLetter.save(os.path.join(permssion_letter,file_name))
            student_daily_sick_info.update(permissionLetter=file_name)
        if student_daily_sick_info:
            flash("Sick Student details added Successfully!!")
            return redirect(url_for('wellnessCenterDashboardPage',hsRefLink=hsRefLink))
        else:
            flash("Required fields are missing !!!")
            return render_template('wellness/student/student_daily_sick_reg.html')

    return render_template('wellness/student/student_daily_sick_reg.html')

@app.route("/wellnessCenterDashboard/<hsRefLink>",methods=['POST','GET'])
def wellnessCenterDashboardPage(hsRefLink):
    if request.method=='GET':
        reports_count_list=[]
        
        sick_student_count = StudentDailySickRegistration.objects.count()
        sick_diet_reports = StudentSickDiet.objects.filter(status__in=[1],sickDietStatus__in=[1,2]).count()
        sick_obers_reports = StudentSickDiet.objects.filter(status__in=[1],sickDietStatus__in=[1]).count()
        sick_recovery_reports = StudentSickDiet.objects.filter(status__in=[1],sickDietStatus__in=[2]).count()
        get_hs_link = WellnessCenterRegistration.objects.get(hsRefLink=hsRefLink)
        get_students_count = StudentDetails.objects.count()
        # print(get_hs_link.hsRefLink)
        if True:
            reports_count_dict={
                "sickStudentCount":sick_student_count,
                "hsRefLink":get_hs_link.hsRefLink,
                "sickDietReport":sick_diet_reports,
                "sickDietObservation":sick_obers_reports,
                "sickDietRecovery":sick_recovery_reports,
                "totalStudentCount":get_students_count
            }
        return render_template('wellness/health/hs_wellness_dashboard.html',reports=reports_count_dict)

@app.route("/sickStudentsDetails",methods=['POST','GET'])
def sickStudentsDetailsPage():
    sick_student_list=[]
    sick_student_dict={}
    count=0
    if request.method=='GET':
        get_sick_students = StudentDailySickRegistration.objects.all()
        if get_sick_students:
            for ss in get_sick_students:
                count=count+1
                sick_student_dict={
                    "slNo":count,
                    "rlNo":ss.rollNumber,
                    "studentName":ss.studentName,
                    "className":ss.className,
                    "diseaseName":ss.diseaseName,
                    "date":ss.date,
                    "time":ss.time,
                    "day":ss.day,
                    "medicineIssued":ss.medicineIssued,
                    "medicineIssuedDate":ss.createdOn,
                    "permissionLetter":ss.permissionLetter,
                    "studentRefLink":ss.studentRefLink
                }
                sick_student_list.append(sick_student_dict)
        return render_template('wellness/student/student_sick_all_reports.html',sick_student_list=sick_student_list)

@app.route("/viewStudentSickPermissionLetter/<studentRefLink>",methods=['POST','GET'])
def viewStudentSickPermissionLetterPage(studentRefLink):
    if request.method=='GET':
        get_per_dict={}
        get_permission_letter = StudentDailySickRegistration.objects.get(studentRefLink=studentRefLink)
        if get_permission_letter:
            return "success"
@app.route("/addStudentSickDiet/<studentRefLink>",methods=['POST','GET'])
def addStudentSickDiet(studentRefLink):
    foodItem = request.form.get('foodItem')
    foodQuantity = request.form.get('foodQuantity')
    numberOfTimes = request.form.get('numberOfTimes')
    sickDietStudentRefLink = secrets.token_urlsafe()
    createdOn = datetime.datetime.now()
    status = 1
    if request.method == 'POST':
        get_student_info = StudentDailySickRegistration.objects.get(studentRefLink=studentRefLink)
        
        add_sick_details = StudentSickDiet(
            studentName = get_student_info.studentName,
            className = get_student_info.className,
            rollNumber = get_student_info.rollNumber,
            studentRefLink= get_student_info.studentRefLink,
            studentId = str(get_student_info.id),
            hsId = str(get_student_info.hsId.id),
            foodItem = foodItem,
            diseaseName = get_student_info.diseaseName,
            medicineIssued = get_student_info.medicineIssued,
            foodQuantity = foodQuantity,
            numberOfTimes = numberOfTimes,
            sickDietStudentRefLink = sickDietStudentRefLink,
            createdOn  = createdOn,
            status = status
            )
        added_sick_info = add_sick_details.save()
        if added_sick_info:
            sickDietStatus = 1
            dietAddedOn=datetime.datetime.now()
            update_sick_student = added_sick_info.update(
                sickDietStatus=sickDietStatus,
                dietAddedOn = dietAddedOn
            )
            if update_sick_student:
                
                return redirect(url_for('sickStudentsDetailsPage'))
    return render_template('wellness/student/student_sick_add_diet.html')

@app.route('/sickDietOverallReports',methods=['POST','GET'])
def sickDietOverallReportsPage():
    if request.method=='GET':
        sick_diet_overall = StudentSickDiet.objects(sickDietStatus__in=[1,2],status__in=[1])
        # print(sick_diet_overall.studentName)
        sick_students_list=[]
        sick_student_dict={}
        count=0
        for sick in sick_diet_overall:
            count=count+1
            sick_student_dict={
            "sNo":count,
            "studentName":sick.studentName,
            "className":sick.className,
            "rollNumber":sick.rollNumber,
            "diseaseName":sick.diseaseName,
            "medicineIssued":sick.medicineIssued,
            "status":sick.status,
            "sickDietStudentRefLink":sick.sickDietStudentRefLink,
            "sickDietStatus":sick.sickDietStatus
            }
            sick_students_list.append(sick_student_dict)
        return render_template('wellness/student/sick_diet_overall.html',sick_students_list=sick_students_list)



@app.route('/sickDietObservationReports',methods=['POST','GET'])
def sickDietObservationReportsPage():
    if request.method=='GET':
        sick_diet_overall = StudentSickDiet.objects(status__in=[1],sickDietStatus__in=[1])
        # print(sick_diet_overall.studentName)
        sick_students_list=[]
        sick_student_dict={}
        count=0
        for sick in sick_diet_overall:
            count=count+1
            sick_student_dict={
            "sNo":count,
            "studentName":sick.studentName,
            "className":sick.className,
            "rollNumber":sick.rollNumber,
            "diseaseName":sick.diseaseName,
            "medicineIssued":sick.medicineIssued,
            "status":sick.status
            # "sickDietStatus":sick.sickDietStatus,
            # "dietAddedOn":sick.dietAddedOn
            }
            sick_students_list.append(sick_student_dict)
        return render_template('wellness/student/sick_observation_reports.html',sick_students_list=sick_students_list)

@app.route('/sickDietRecoveryReports',methods=['POST','GET'])
def sickDietRecoveryReportsPage():
    if request.method=='GET':
        sick_diet_overall = StudentSickDiet.objects(status__in=[1],sickDietStatus__in=[2])
        # print(sick_diet_overall.studentName)
        sick_students_list=[]
        sick_student_dict={}
        count=0
        for sick in sick_diet_overall:
            count=count+1
            sick_student_dict={
            "sNo":count,
            "studentName":sick.studentName,
            "className":sick.className,
            "rollNumber":sick.rollNumber,
            "diseaseName":sick.diseaseName,
            "medicineIssued":sick.medicineIssued,
            "status":sick.status
            # "sickDietStatus":sick.sickDietStatus,
            # "dietAddedOn":sick.dietAddedOn
            }
            sick_students_list.append(sick_student_dict)
        return render_template('wellness/student/sick_recovery_reports.html',sick_students_list=sick_students_list)

@app.route("/recoveryStatus/<sickDietStudentRefLink>",methods=['POST','GET'])
def recoveryStatusPage(sickDietStudentRefLink):
    
    get_status = StudentSickDiet.objects.get(sickDietStudentRefLink__in=[sickDietStudentRefLink],status__in=[1])
    recoverdOn = datetime.datetime.now()
    sickDietStatus=2
    if get_status:
        update_status = get_status.update(sickDietStatus=sickDietStatus,recoverdOn=recoverdOn)
    return redirect(url_for('sickDietOverallReportsPage'))


@app.route("/classReports",methods=['POST','GET'])
def classReportsPage():
    return render_template('wellness/student/class_buttons.html')

@app.route("/studentsDetails",methods=['POST','GET'])
def studentsDetailsPage():
    student_list=[]
    students_dict={}
    count=0
    className = request.form.get('className')
    if request.method=='POST':
        get_students = StudentDetails.objects.filter(className=className)
        if get_students:
            for gs in get_students:
                count=count+1

                student_dict = {
                    "sl":count,
                    "studentName":gs.firstName+" "+gs.lastName,
                    "className":gs.className,
                    "rollNumber":gs.rollNumber,
                    "status":gs.status
                }
                student_list.append(student_dict)
        elif not get_students:
            # return"no data"
            pass
    return render_template('wellness/student/student_details.html',student_list=student_list)

@app.route("/studentAddBMI/<className>/<rollNumber>",methods=['POST','GET'])
def studentAddBMIPage(className,rollNumber):
    student_list=[]
    students_dict={}
    count=0
    get_students = StudentDetails.objects.get(rollNumber__in=[rollNumber],className__in=[className])
    
    if request.method=='POST':
        height = request.form.get('height')
        weight = request.form.get('weight')
        hemoglobin = request.form.get('hemoglobin')
        age = request.form.get('age')
        month = request.form.get('month')
        bmi_value = int(weight)/(int(height)/100)**2
        print(bmi_value)
        update_data = get_students.update(
            height=height,
            weight=weight,
            hemoglobin=hemoglobin,
            age = age,
            month=month,
            bmiValue=str(bmi_value),
            studentRefLink=secrets.token_urlsafe(),
            createdOn=datetime.datetime.now(),
            status=1
            )
        if update_data:

            flash("Successfully Added Height, Weight and Hemoglobin")
            return redirect(url_for('studentsClassDetailsPage',className=className))
    else:
        return render_template('wellness/student/add_height_weight.html')
@app.route("/studentsClassDetails/<className>")
def studentsClassDetailsPage(className):
    student_list=[]
    students_dict={}
    count=0
    # className = request.form.get('className')
    if request.method=='GET':
        get_students = StudentDetails.objects(className__in=[className])
    
        if get_students:
            for gs in get_students:
                count=count+1

                student_dict = {
                    "sl":count,
                    "studentName":gs.firstName+" "+gs.lastName,
                    "className":gs.className,
                    "rollNumber":gs.rollNumber,
                    "status":gs.status
                }
                student_list.append(student_dict)
    return render_template('wellness/student/class_student_details.html',student_list=student_list)

# @app.route("/class6aAdd/<rollNumber>",methods=['POST','GET'])
# def class6aAddPage(rollNumber):
#     student_list=[]
#     students_dict={}
#     count=0
#     get_students = StudentDetails.objects.get(rollNumber__in=[rollNumber],className__in=['6B'])
#     print(get_students.rollNumber)
#     if request.method=='POST':
#         height = request.form.get('height')
#         weight = request.form.get('weight')
#         hemoglobin = request.form.get('hemoglobin')
#         update_data = get_students.update(
#             height=height,
#             weight=weight,
#             hemoglobin=hemoglobin,
#             age = "12",
#             studentRefLink=secrets.token_urlsafe(),
#             createdOn=datetime.datetime.now(),
#             status=1
#             )
#         if update_data:
#             flash("Successfully Added Height, Weight and Hemoglobin")
#             return redirect(url_for('class6AViewPage'))
#     else:
#         return render_template('wellness/student/add_height_weight.html')


@app.route("/schoolVisit",methods=['POST'])
def schoolVisitPage():
    data_status = {"responseStatus": 0, "results": ""}
    firstname = request.json['firstname']
    lastname = request.json['lastname']
    reason = request.json['reason']
    mobile = request.json['mobile']
    # date = datetime.now()
    # time = datetime.now()
    status = 1
    if request.method == 'POST':
        # print(firstname,lastname,reason,mobile)
        visit_data = GateVisit(
            firstname = firstname,
            lastname = lastname,
            reason = reason,
            mobile = mobile,
            date = datetime.datetime.now(),
            time = datetime.datetime.now(),
            status = status
            )
        visted_info = visit_data.save()
        if visted_info:
            data_status["responseStatus"] = 201
            data_status["results"] = "success"
            return data_status
@app.route("/schoolVisitReports",methods=['POST'])
def schoolVisitReportsPage():
    if request.method=='GET':
        vistor_list = []
        vistor_dict = {}
        get_visitors = GateVisit.objects(status__in=[1])
        if get_visitors:
            for vi in get_visitors:
                vistor_dict = {
                "firstname":vi.firstname,
                "lastname":vi.lastname,
                "reason":vi.reason,
                "mobile":vi.mobile,
                "visited":vi.date
                }
            vistor_list.append(vistor_dict)

@app.route("/classTeacherLogin",methods=['POST','GET'])
def classTeacherLoginPage():
    emailId = request.form.get('emailId')
    password = request.form.get('password')

    if emailId and password and request.method=='POST':
        try:
            get_logins = ClassTeacherRegister.objects.get(emailId__iexact=emailId,password__exact=password,status__in=[1])
            if get_logins:
                classTeacherRefLink = get_logins.classTeacherRefLink
                className = get_logins.className
                return redirect(url_for('studentAttendanceDashboardPage',classTeacherRefLink=classTeacherRefLink))
            else:
                flash("Invalid Credentials!!!")
                return render_template("attendance/class_teacher_login.html")
        except HouseMaster.DoesNotExist as e:
            flash("Invalid Credentials!!!")
            return render_template("attendance/class_teacher_login.html")

    return render_template('attendance/class_teacher_login.html')

@app.route("/classTeacherRegistration",methods=['POST','GET'])
def classTeacherRegAttendancePage():
    classTeacherFirstName = request.form.get('classTeacherFirstName')
    classTeacherLastName = request.form.get('classTeacherLastName')
    className = request.form.get('className')
    emailId = request.form.get('emailId')
    phoneNumber = request.form.get('phoneNumber')
    classTeacherRefLink = secrets.token_urlsafe()
    password = request.form.get("password")
    classTeacherId = request.form.get('classTeacherId')
    status = 1
    createdOn = datetime.datetime.now()

    if request.method == 'POST':
        try:
            queryset = ClassTeacherRegister.objects(emailId__iexact=emailId)
            if queryset:
                flash("Email already Exists!!!")
                return render_template("attendance/class_teacher_register.html")
        except Exception as e:
            pass

        try:
            queryset = ClassTeacherRegister.objects(className__iexact=className)
            if queryset:
                flash("Already "+houseClass+" assigned to someone!!!")
                return render_template("attendance/class_teacher_register.html")
        except Exception as e:
            pass
        class_teacher = ClassTeacherRegister(
            classTeacherFirstName=classTeacherFirstName,
            classTeacherLastName=classTeacherLastName,
            className=className,
            emailId = emailId,
            phoneNumber = phoneNumber,
            classTeacherRefLink = classTeacherRefLink,
            classTeacherId = classTeacherId,
            password=password,
            status=status,
            createdOn=createdOn
            )
        class_teacher_details = class_teacher.save()
        if class_teacher_details:
            flash("Class Teacher Registration Successfully Completed!!!.")
            return redirect(url_for('classTeacherLoginPage'))
    else:
        return render_template("attendance/class_teacher_register.html")
    return render_template('attendance/class_teacher_login.html')

@app.route('/classTeacherForgotPassword',methods=['POST','GET'])
def classTeacherForgotPasswordPage():
    emailId = request.form.get("emailId")
    newPassword = request.form.get("newPassword")
    confirmPassword = request.form.get("confirmPassword")
    

    if emailId and newPassword and confirmPassword and request.method=="POST":
        try:
            if newPassword==confirmPassword:
                get_master_info = ClassTeacherRegister.objects.get(emailId=emailId)
                # print(get_student_info["emailId"])
                if get_master_info.emailId:
                    updated_password=get_master_info.update(
                        password=newPassword
                        )
                    if updated_password:
                        flash("Password Successfully Changed")
                        return redirect(url_for('classTeacherLoginPage'))
                
            else:
                flash("Password Miss Matched")
                return render_template('attendance/class_teacher_forgot_password.html')
        except ClassTeacherRegister.DoesNotExist as e:
            flash("Email Id DoesNotExist")
            return render_template('attendance/class_teacher_forgot_password.html')
    
    return render_template('attendance/class_teacher_forgot_password.html')





@app.route("/studentAttendanceDashboard/<classTeacherRefLink>",methods=['POST','GET'])
def studentAttendanceDashboardPage(classTeacherRefLink):
    if request.method=='GET':
        student_attendance={}
        
        total_students = StudentAttendanceRegister.objects.count()
        # present_students = StudentAttendanceRegister.objects.filter(status__in=[1],attendenceStatus__in=[1]).count()
        # absent_students = StudentAttendanceRegister.objects.filter(status__in=[1],attendenceStatus__in=[2]).count()
        get_teacher_link = ClassTeacherRegister.objects.get(classTeacherRefLink=classTeacherRefLink)
        if True:
            student_attendance={
                "totalStudents":total_students,
                "classTeacherRefLink":get_teacher_link.classTeacherRefLink,
                "presentStudents":"present_students",
                "absentStudents":"absent_students",
            }
        return render_template('attendance/student_attendance_dashboard.html',student_attendance=student_attendance)

@app.route("/addStudents/<classTeacherRefLink>",methods=['POST','GET'])
def addStudentPage(classTeacherRefLink):
    firstName = request.form.get('firstName')
    lastName = request.form.get('lastName')
    className = request.form.get('className')
    rollNumber = request.form.get('rollNumber')
    classTeacherRefLink = classTeacherRefLink
    studentAttendanceLink = secrets.token_urlsafe()
    createdOn = datetime.datetime.now()
    status = 1
    attendanceStatus = 0

    if request.method == 'POST':
        try:
            queryset = StudentAttendanceRegister.objects(rollNumber__iexact=rollNumber)
            if queryset:
                flash("Already Roll Number Exists!!")
                return render_template("attendance/add_student.html")
        except Exception as e:
            pass
        add_student= StudentAttendanceRegister(
            firstName = firstName,
            lastName = lastName,
            className = className,
            rollNumber = rollNumber,
            classTeacherRefLink = classTeacherRefLink,
            studentAttendanceLink = studentAttendanceLink,
            createdOn = createdOn,
            status = status,
            attendanceStatus=attendanceStatus
            )
        add_student_info = add_student.save()
        if add_student_info:
            # get_class_teacher = add_student_info.classTeacherRefLink
            return redirect(url_for('studentAttendanceDashboardPage',classTeacherRefLink=classTeacherRefLink))

    return render_template('attendance/add_student.html')
@app.route("/studentAttendance/<classTeacherRefLink>",methods=['POST','GET'])
def studentAttendancePage(classTeacherRefLink):
    student_list=[]
    student_dict={}
    get_students=StudentAttendanceRegister.objects(status__in=[1]).order_by('rollNumber')
    if get_students:
        for gs in get_students:
            student_dict={
                "rollNumber":gs.rollNumber,
                "className":gs.className,
                "studentName":gs.firstName+" "+gs.lastName,
                "status":gs.status,
                "studentId":str(gs.id),
                "classTeacherRefLink":classTeacherRefLink,
                "studentAttendanceLink":gs.studentAttendanceLink,
                "attendanceStatus":gs.attendanceStatus

            }

            student_list.append(student_dict)

    return render_template('attendance/student_attendance_view.html',student_list=student_list)

# @app.route("/studentAttendancePost/<classTeacherRefLink>",methods=['POST','GET'])
# def studentAttendancePostPage(classTeacherRefLink):
#     get_student = StudentAttendanceRegister.objects.get

if __name__ == '__main__':
    app.run(debug=True, port=4000)
    # app.run(host='0.0.0.0',debug=True, port=4000)
