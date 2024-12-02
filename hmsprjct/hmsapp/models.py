# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
from datetime import datetime


class Ambulance(models.Model):
    ambulance_number = models.CharField(max_length=100)
    driver_name = models.CharField(max_length=100)
    attender = models.CharField(max_length=50)
    preferred_location = models.CharField(max_length=200)
    availability = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ambulance'


class AmbulanceAlerts(models.Model):
    patientid = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    doctorname = models.CharField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    relative_contact = models.CharField(max_length=255, blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    action_taken = models.CharField(max_length=255, blank=True, null=True)
    issue_registered = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    ambulance_id = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'ambulance_alerts'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class Bookingpatient(models.Model):
    patientid = models.CharField(max_length=255, blank=True, null=True)
    firstname = models.CharField(db_column='FirstName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=255)  # Field name made lowercase.
    email = models.CharField(max_length=255, blank=True, null=True)
    mobile = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    doctor_name = models.CharField(max_length=255, blank=True, null=True)
    reason = models.CharField(max_length=255, blank=True, null=True)
    date_book = models.DateTimeField(blank=True, null=True)
    time_book_start = models.CharField(max_length=100, blank=True, null=True)
    confirm = models.IntegerField()
    empcode = models.CharField(max_length=255)
    time_book_end = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'bookingpatient'


class Booktest(models.Model):
    book_time = models.CharField(max_length=255)
    docid = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'booktest'


class Complaints(models.Model):
    empcode = models.CharField(max_length=255)
    complaint = models.CharField(max_length=255, blank=True, null=True)
    date_reg = models.DateTimeField()
    action_comp = models.IntegerField()
    name = models.CharField(max_length=200)
    to_whom = models.CharField(max_length=200)
    remarks = models.CharField(max_length=100)
    reason = models.CharField(db_column='Reason', max_length=250)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'complaints'


class Department(models.Model):
    department = models.CharField(max_length=255)
    head = models.CharField(max_length=255, blank=True, null=True)
    start_time = models.CharField(max_length=100)
    end_time = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'department'


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class EmergencyAlerts(models.Model):
    patientid = models.CharField(max_length=100)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    firstname = models.CharField(max_length=255, blank=True, null=True)
    doctorname = models.CharField(max_length=100, blank=True, null=True)
    contact = models.CharField(max_length=50, blank=True, null=True)
    relative_contact = models.CharField(max_length=50, blank=True, null=True)
    date = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)
    action_taken = models.CharField(max_length=10, blank=True, null=True)
    issue_registered = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'emergency_alerts'


class Feedback(models.Model):
    patientid = models.CharField(max_length=500, blank=True, null=True)
    name = models.CharField(max_length=150, blank=True, null=True)
    mobile = models.CharField(max_length=100, blank=True, null=True)
    response = models.CharField(max_length=1000, blank=True, null=True)
    action_response = models.CharField(max_length=1000, blank=True, null=True)
    date_reg = models.CharField(max_length=255)
    date_action = models.CharField(max_length=255)
    mail_reg = models.CharField(max_length=255)
    approved_by = models.IntegerField(default=0)
    pending = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'feedback'


class HmsappDepartment(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'hmsapp_department'


class HospitalSupplimentries(models.Model):
    particulars = models.CharField(max_length=255)
    price = models.CharField(max_length=255, blank=True, null=True)
    stock = models.CharField(max_length=255)
    gst = models.CharField(db_column='GST', max_length=100)  # Field name made lowercase.
    remarks = models.CharField(max_length=500)

    class Meta:
        managed = False
        db_table = 'hospital_supplimentries'


class Ipbilling(models.Model):
    patientid = models.CharField(max_length=255)
    ipno = models.CharField(max_length=255, blank=True, null=True)
    department = models.IntegerField(blank=True, null=True)
    date_bill = models.CharField(max_length=255, blank=True, null=True)
    test_id = models.IntegerField(blank=True, null=True)
    room_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ipbilling'


class LabTest(models.Model):
    test_name = models.CharField(max_length=255, blank=True, null=True)
    price = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    staff_alloted = models.CharField(max_length=255, blank=True, null=True)
    duration = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'lab_test'


class Leaveregister(models.Model):
    empid = models.CharField(max_length=255)
    name = models.CharField(max_length=255)  # New field for employee name
    leave_requested = models.CharField(max_length=255, blank=True, null=True)  # Start Date
    leave_approved = models.CharField(max_length=255, blank=True, null=True)
    leave_status = models.CharField(max_length=255, blank=True, null=True, default="Pending")
    leave_approved_by = models.CharField(max_length=255, blank=True, null=True)
    department = models.IntegerField()  # Department ID
    return_date = models.CharField(max_length=250)  # End Date
    cancelled = models.IntegerField(default=0)  # 1 or 0
    reason = models.CharField(max_length=250)
    pending = models.IntegerField(default=1) # 1 or 0


    class Meta:
        managed = False
        db_table = 'leaveregister'


class Medicine(models.Model):
    medicine_name = models.CharField(max_length=200)
    price = models.CharField(max_length=200)
    stock = models.CharField(max_length=200)
    gst = models.CharField(db_column='GST', max_length=200)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'medicine'


class mortuary_table(models.Model):
    fullname = models.CharField(max_length=100)
    dod = models.DateField(null=True, blank=True)
    gender = models.CharField(
    max_length=10,  # Allow longer values like "Female"
    choices=[
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    ]
)
    cause_of_death = models.CharField(max_length=250)
    death_cert_num = models.CharField(max_length=100)
    mortuary_fee = models.FloatField()

    class Meta:
        db_table = 'mortuary_table'
    def __str__(self):
        return self.fullname

    
# class mortuary_table(models.Model):
#     fullname = models.CharField(max_length=100)
#     dod = models.DateField()
#     GENDER_CHOICES = [
#         ('M', 'Male'),
#         ('F', 'Female'),
#         ('O', 'Other'),  # Additional option for non-binary or other gender identities
#     ]
#     gender = models.CharField(
#         max_length=1,
#         choices=GENDER_CHOICES,
#     )
#     cause_of_death = models.CharField(max_length=250)
#     death_cert_num = models.CharField(max_length=100)
#     mortuary_fee = models.FloatField()

#     class Meta:
#         db_table = 'mortuary_table'

#     def __str__(self):
#         return self.fullname




class Opbilling(models.Model):
    patientid = models.CharField(max_length=255)
    opno = models.CharField(max_length=255, blank=True, null=True)
    department = models.IntegerField(blank=True, null=True)
    date_bill = models.CharField(max_length=255, blank=True, null=True)
    test_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'opbilling'


class patient_reports(models.Model):
    patient_id = models.CharField(max_length=100)
    doctor_id = models.ForeignKey('Staffdetails', on_delete=models.CASCADE, db_column='doctor_id')
    date = models.DateField()
    file_path = models.FileField(upload_to='reports/')  # Automatically saves in MEDIA_ROOT/reports/

    class Meta:
        db_table = 'patient_reports'


class PatientTest(models.Model):
    patientid = models.CharField(max_length=255)
    ipno = models.CharField(max_length=255)
    testid = models.CharField(max_length=255, blank=True, null=True)
    department = models.CharField(max_length=255, blank=True, null=True)
    test_results = models.CharField(max_length=255, blank=True, null=True)
    test_range_max = models.CharField(max_length=255, blank=True, null=True)
    test_range_min = models.CharField(max_length=255, blank=True, null=True)
    risk_level = models.CharField(max_length=255, blank=True, null=True)
    payment_status = models.CharField(max_length=100, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'patient_test'
        
class Patientdetails(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    patientid = models.CharField(max_length=255)
    regdate = models.CharField(max_length=150)
    docname = models.CharField(max_length=255, blank=True, null=True)
    empid = models.CharField(max_length=100)
    presc = models.CharField(max_length=255, blank=True, null=True)
    address = models.CharField(max_length=1000)
    phnumber = models.CharField(max_length=255)
    department = models.CharField(max_length=255)
    email = models.CharField(max_length=100)
    active = models.IntegerField()
    dob = models.CharField(max_length=50)
    occupation = models.CharField(max_length=255)
    guardian = models.CharField(max_length=255)
    nationality = models.CharField(max_length=100)
    mobnumber = models.CharField(max_length=50)
    documentsubmitted = models.CharField(max_length=100)
    gender = models.CharField(max_length=100)
    bloodgroup = models.CharField(max_length=50)
    maritialstatus = models.CharField(max_length=100)
    image = models.CharField(max_length=500)
    relativetype = models.CharField(max_length=200, blank=True, null=True)
    relativecontactnum = models.CharField(max_length=50, blank=True, null=True)
    patient_reports = models.CharField(max_length=250, blank=True, null=True, default="")

    class Meta:

        db_table = 'patientdetails'
        unique_together = (('id', 'patientid'),)






class Staffdetails(models.Model):
    title = models.CharField(max_length=100)
    firstname = models.CharField(db_column='FirstName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    lastname = models.CharField(db_column='LastName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    dob = models.DateTimeField(blank=True, null=True)
    gender = models.CharField(max_length=255, blank=True, null=True)
    nationality = models.CharField(max_length=255, blank=True, null=True)
    empcode = models.CharField(max_length=255, blank=True, null=True)
    contact_number = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    residential_address = models.CharField(max_length=255, blank=True, null=True)
    medical_icense_number = models.CharField(max_length=255, blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, blank=True, null=True)
    medical_school_attended = models.CharField(max_length=255, blank=True, null=True)
    year_of_graduation = models.DateTimeField(blank=True, null=True)
    residency_information = models.CharField(max_length=255, blank=True, null=True)
    board_certifications = models.CharField(max_length=255, blank=True, null=True)
    current_position = models.CharField(max_length=255, blank=True, null=True)
    current_employer = models.CharField(db_column='current_Employer', max_length=255, blank=True, null=True)  # Field name made lowercase.
    previous_positions = models.CharField(max_length=255, blank=True, null=True)
    years_of_experience = models.CharField(max_length=255, blank=True, null=True)
    starttime = models.CharField(max_length=50, blank=True, null=True)
    endtime = models.CharField(max_length=50)
    availability_oncall = models.CharField(max_length=255, blank=True, null=True)
    active = models.IntegerField()
    image = models.CharField(max_length=255, blank=True, null=True)
    class Meta:
        managed = False
        db_table = 'staffdetails'


class Supplier(models.Model):
    name = models.CharField(max_length=255)
    address = models.CharField(max_length=255, blank=True, null=True)
    contact = models.CharField(max_length=255, blank=True, null=True)
    contact2 = models.CharField(max_length=255, blank=True, null=True)
    gstno = models.CharField(max_length=255, blank=True, null=True)
    cgst = models.CharField(max_length=255, blank=True, null=True)
    sgst = models.CharField(max_length=255, blank=True, null=True)
    tds = models.CharField(max_length=100, blank=True, null=True)
    products = models.CharField(max_length=500, blank=True, null=True)
    files = models.CharField(max_length=150, blank=True, null=True)
    remarks = models.CharField(max_length=1000, blank=True, null=True)
    passed = models.IntegerField()
    phone_contact = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'supplier'


class Tblpatient(models.Model):
    fldpatientid = models.IntegerField(db_column='fldPatientID')  # Field name made lowercase.
    fldinstitutionname = models.IntegerField(db_column='fldInstitutionName', blank=True, null=True)  # Field name made lowercase.
    fldpatientregno = models.CharField(db_column='fldPatientRegNo', max_length=64, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    flddateregistration = models.DateField(db_column='fldDateRegistration', blank=True, null=True)  # Field name made lowercase.
    fldtitle = models.IntegerField(db_column='fldTitle', blank=True, null=True)  # Field name made lowercase.
    fldsex = models.IntegerField(db_column='fldSex', blank=True, null=True)  # Field name made lowercase.
    fldname = models.CharField(db_column='fldName', max_length=80, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    fldcurrentstatus = models.IntegerField(db_column='fldCurrentStatus', blank=True, null=True)  # Field name made lowercase.
    fldpatientstatus = models.IntegerField(db_column='fldPatientStatus', blank=True, null=True)  # Field name made lowercase.
    fldenrolledasother = models.IntegerField(db_column='fldEnrolledAsOther', blank=True, null=True)  # Field name made lowercase.
    flddeathdate = models.DateField(db_column='fldDeathDate', blank=True, null=True)  # Field name made lowercase.
    flddeathtime = models.IntegerField(db_column='fldDeathTime', blank=True, null=True)  # Field name made lowercase.
    flddeathtimestring = models.CharField(db_column='fldDeathTimeString', max_length=16, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    fldcauseofdeath = models.TextField(db_column='fldCauseOfDeath', blank=True, null=True)  # Field name made lowercase.
    fldiscertified = models.IntegerField(db_column='fldIsCertified', blank=True, null=True)  # Field name made lowercase.
    fldage = models.IntegerField(db_column='fldAge', blank=True, null=True)  # Field name made lowercase.
    fldagetype = models.IntegerField(db_column='fldAgeType', blank=True, null=True)  # Field name made lowercase.
    fldagelastmodifieddate = models.DateField(db_column='fldAgeLastModifiedDate', blank=True, null=True)  # Field name made lowercase.
    flddob = models.DateField(db_column='fldDOB', blank=True, null=True)  # Field name made lowercase.
    fldaddress1 = models.CharField(db_column='fldAddress1', max_length=256, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    fldaddress2 = models.CharField(db_column='fldAddress2', max_length=256, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    fldlocation = models.CharField(db_column='fldLocation', max_length=32, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    fldcity = models.CharField(db_column='fldCity', max_length=32, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    fldpincode = models.CharField(db_column='fldPinCode', max_length=8, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    fldstate = models.IntegerField(db_column='fldState', blank=True, null=True)  # Field name made lowercase.
    fldcountry = models.IntegerField(db_column='fldCountry', blank=True, null=True)  # Field name made lowercase.
    fldfathername = models.CharField(db_column='fldFatherName', max_length=80, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    fldspousename = models.CharField(db_column='fldSpouseName', max_length=64, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    fldreligionid = models.IntegerField(db_column='fldReligionID', blank=True, null=True)  # Field name made lowercase.
    fldbloodgroup = models.CharField(db_column='fldBloodGroup', max_length=8, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    fldmobileno = models.CharField(db_column='fldMobileNo', max_length=32, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    fldcontactno = models.CharField(db_column='fldContactNo', max_length=48, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    fldmaritalstatus = models.CharField(db_column='fldMaritalStatus', max_length=32, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    fldoccupation = models.CharField(db_column='fldOccupation', max_length=64, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    fldemailid = models.CharField(db_column='fldEmailID', max_length=272, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    fldopeningbalance = models.FloatField(db_column='fldOpeningBalance', blank=True, null=True)  # Field name made lowercase.
    fldphoto = models.TextField(db_column='fldPhoto', blank=True, null=True)  # Field name made lowercase.
    fldlastadmissiontype = models.IntegerField(db_column='fldLastAdmissionType', blank=True, null=True)  # Field name made lowercase.
    fldlastdischargedate = models.DateField(db_column='fldLastDischargeDate', blank=True, null=True)  # Field name made lowercase.
    fldclosingbalance = models.FloatField(db_column='fldClosingBalance', blank=True, null=True)  # Field name made lowercase.
    fldtaggedregno = models.IntegerField(db_column='fldTaggedRegNo', blank=True, null=True)  # Field name made lowercase.
    fldlastadmdate = models.DateField(db_column='fldLastAdmDate', blank=True, null=True)  # Field name made lowercase.
    flddonornumber = models.CharField(db_column='fldDonorNumber', max_length=32, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    fldisrejecteddonor = models.IntegerField(db_column='fldIsRejectedDonor', blank=True, null=True)  # Field name made lowercase.
    fldremovedefaultplanscheme = models.IntegerField(db_column='fldRemoveDefaultPlanScheme', blank=True, null=True)  # Field name made lowercase.
    fldicdcode = models.CharField(db_column='fldIcdCode', max_length=32, db_collation='latin1_swedish_ci', blank=True, null=True)  # Field name made lowercase.
    fldgeneratedno = models.IntegerField(db_column='fldGeneratedNo', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tblpatient'


class Tblpatienthospitaldetails(models.Model):
    fldid = models.IntegerField(db_column='fldID', primary_key=True)  # Field name made lowercase.
    fldpatientid = models.IntegerField(db_column='fldPatientID', blank=True, null=True)  # Field name made lowercase.
    fldadmissiontype = models.IntegerField(db_column='fldAdmissionType', blank=True, null=True)  # Field name made lowercase.
    fldage = models.IntegerField(db_column='fldAge', blank=True, null=True)  # Field name made lowercase.
    fldagetype = models.IntegerField(db_column='fldAgeType', blank=True, null=True)  # Field name made lowercase.
    fldstartdate = models.DateField(db_column='fldStartDate', blank=True, null=True)  # Field name made lowercase.
    fldstartdatetime = models.IntegerField(db_column='fldStartDateTime', blank=True, null=True)  # Field name made lowercase.
    fldstartdatetimestring = models.CharField(db_column='fldStartDateTimeString', max_length=16, blank=True, null=True)  # Field name made lowercase.
    fldenddate = models.DateField(db_column='fldEndDate', blank=True, null=True)  # Field name made lowercase.
    fldendtime = models.IntegerField(db_column='fldEndTime', blank=True, null=True)  # Field name made lowercase.
    fldendtimestring = models.CharField(db_column='fldEndTimeString', max_length=16, blank=True, null=True)  # Field name made lowercase.
    fldreferredby = models.IntegerField(db_column='fldReferredBy', blank=True, null=True)  # Field name made lowercase.
    fldconsultantid = models.IntegerField(db_column='fldConsultantID', blank=True, null=True)  # Field name made lowercase.
    flddiagnosisid = models.IntegerField(db_column='fldDiagnosisID', blank=True, null=True)  # Field name made lowercase.
    fldisended = models.IntegerField(db_column='fldIsEnded', blank=True, null=True)  # Field name made lowercase.
    fldcurrentdepartmentid = models.IntegerField(db_column='fldCurrentDepartmentId', blank=True, null=True)  # Field name made lowercase.
    fldcurrentunitid = models.IntegerField(db_column='fldCurrentUnitId', blank=True, null=True)  # Field name made lowercase.
    fldlastaction = models.IntegerField(db_column='fldLastAction', blank=True, null=True)  # Field name made lowercase.
    fldismlc = models.IntegerField(db_column='fldIsMLC', blank=True, null=True)  # Field name made lowercase.
    fldoppackage = models.IntegerField(db_column='fldOPPackage', blank=True, null=True)  # Field name made lowercase.
    fldpackagestatus = models.IntegerField(db_column='fldPackageStatus', blank=True, null=True)  # Field name made lowercase.
    tblsection = models.IntegerField(db_column='tblSection', blank=True, null=True)  # Field name made lowercase.
    fldisboughtindead = models.IntegerField(db_column='fldIsBoughtInDead', blank=True, null=True)  # Field name made lowercase.
    fldtype = models.IntegerField(db_column='fldType', blank=True, null=True)  # Field name made lowercase.
    fldwoundcertissued = models.IntegerField(db_column='fldWoundCertIssued', blank=True, null=True)  # Field name made lowercase.
    fldreportedtopolice = models.IntegerField(db_column='fldReportedtoPolice', blank=True, null=True)  # Field name made lowercase.
    fldpolicestation = models.CharField(db_column='fldPoliceStation', max_length=64, blank=True, null=True)  # Field name made lowercase.
    fldreportedby = models.CharField(db_column='fldReportedBy', max_length=64, blank=True, null=True)  # Field name made lowercase.
    roomtransferid = models.IntegerField(db_column='RoomTransferID', blank=True, null=True)  # Field name made lowercase.
    fldvalidtill = models.DateField(db_column='fldValidtill', blank=True, null=True)  # Field name made lowercase.
    fldipnumber = models.CharField(db_column='fldIPNumber', max_length=64, blank=True, null=True)  # Field name made lowercase.
    fldmasterrecid = models.IntegerField(db_column='fldMasterRecID', blank=True, null=True)  # Field name made lowercase.
    fldpackagebillserviceid = models.IntegerField(db_column='fldPackageBillServiceId', blank=True, null=True)  # Field name made lowercase.
    fldpatientipoppackages = models.IntegerField(db_column='fldPatientIPOPPackages', blank=True, null=True)  # Field name made lowercase.
    fldiscancelled = models.IntegerField(db_column='fldIscancelled', blank=True, null=True)  # Field name made lowercase.
    fldmlcservice = models.IntegerField(db_column='fldMLCService', blank=True, null=True)  # Field name made lowercase.
    fldwcservice = models.IntegerField(db_column='fldWCService', blank=True, null=True)  # Field name made lowercase.
    fldrtpservice = models.IntegerField(db_column='fldRTPService', blank=True, null=True)  # Field name made lowercase.
    fldpatientcategory = models.IntegerField(db_column='fldPatientcategory', blank=True, null=True)  # Field name made lowercase.
    fldpatientdetails = models.TextField(db_column='fldPatientDetails', blank=True, null=True)  # Field name made lowercase.
    fldmotherid = models.IntegerField(db_column='fldMotherID', blank=True, null=True)  # Field name made lowercase.
    flddontcolregcharge = models.IntegerField(db_column='fldDontColRegCharge', blank=True, null=True)  # Field name made lowercase.
    flddischargeadvice = models.TextField(db_column='fldDischargeadvice', blank=True, null=True)  # Field name made lowercase.
    flddeath = models.IntegerField(db_column='fldDeath', blank=True, null=True)  # Field name made lowercase.
    flddontshowinreport = models.IntegerField(db_column='fldDontShowInReport', blank=True, null=True)  # Field name made lowercase.
    fldistaggedadmission = models.IntegerField(db_column='fldIsTaggedAdmission', blank=True, null=True)  # Field name made lowercase.
    fldiscritical = models.IntegerField(db_column='fldIsCritical', blank=True, null=True)  # Field name made lowercase.
    fldisstudy = models.IntegerField(db_column='fldIsStudy', blank=True, null=True)  # Field name made lowercase.
    fldisnotify = models.IntegerField(db_column='fldIsNotify', blank=True, null=True)  # Field name made lowercase.
    fldisabnormal = models.IntegerField(db_column='fldIsAbNormal', blank=True, null=True)  # Field name made lowercase.
    fldopfilestatus = models.IntegerField(db_column='fldOPFileStatus', blank=True, null=True)  # Field name made lowercase.
    fldopfilestautsupdatedby = models.IntegerField(db_column='fldOPFileStautsUpdatedBy', blank=True, null=True)  # Field name made lowercase.
    fldipfilecurrentlocation = models.IntegerField(db_column='fldIPFileCurrentLocation', blank=True, null=True)  # Field name made lowercase.
    fldopfilesentdate = models.DateField(db_column='fldOpFileSentDate', blank=True, null=True)  # Field name made lowercase.
    fldopfilesenttime = models.IntegerField(db_column='fldOpfileSentTime', blank=True, null=True)  # Field name made lowercase.
    fldopfilesenttimestring = models.CharField(db_column='fldOpFileSentTimeString', max_length=16, blank=True, null=True)  # Field name made lowercase.
    fldopfilereturneddate = models.DateField(db_column='fldOpFileReturnedDate', blank=True, null=True)  # Field name made lowercase.
    fldopfilereturnedtime = models.IntegerField(db_column='fldOpFileReturnedTime', blank=True, null=True)  # Field name made lowercase.
    fldopfilereturnedtimestring = models.CharField(db_column='fldOpFileReturnedTimeString', max_length=16, blank=True, null=True)  # Field name made lowercase.
    fldisenrolledtoivf = models.IntegerField(db_column='fldIsEnrolledToIVF', blank=True, null=True)  # Field name made lowercase.
    flddischargesummaryinfo = models.TextField(db_column='fldDischargeSummaryInfo', blank=True, null=True)  # Field name made lowercase.
    fldtoken = models.CharField(db_column='fldToken', max_length=100, blank=True, null=True)  # Field name made lowercase.
    diffdates = models.CharField(max_length=100)
    subno = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'tblpatienthospitaldetails'


class TestImage(models.Model):
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase. The composite primary key (ID, image) found, that is not supported. The first column is selected.
    image = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'test_image'
        unique_together = (('id', 'image'),)


class Users(models.Model):
    firstname = models.CharField(max_length=255)
    lastname = models.CharField(max_length=255, blank=True, null=True)
    empid = models.CharField(max_length=255, blank=True, null=True)
    email = models.CharField(max_length=255, blank=True, null=True)
    mob = models.CharField(max_length=255, blank=True, null=True)
    designation = models.CharField(max_length=255, blank=True, null=True)
    station = models.CharField(max_length=255, blank=True, null=True)
    pass_field = models.CharField(db_column='pass', max_length=100)  # Field renamed because it was a Python reserved word.
    username = models.CharField(max_length=250)
    active = models.IntegerField()
    date_reg = models.CharField(max_length=100)
    department = models.IntegerField()
    date_approved = models.CharField(max_length=100)
    approved_by = models.CharField(max_length=200)
    cancelled = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'users'
