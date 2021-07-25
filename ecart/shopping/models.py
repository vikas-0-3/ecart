from django.db import models
from django.contrib.auth.models import User
from django.db.models.deletion import CASCADE, DO_NOTHING
from django.db.models.fields import NullBooleanField
# Create your models here.


class Lead(models.Model):
    company_name = models.CharField(max_length=200)
    website = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.BigIntegerField()
    contact_person = models.CharField(max_length=200)
    country = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    czip = models.BigIntegerField()
    title = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    source = models.CharField(max_length=200)
    assigned_to = models.CharField(max_length=200)
    addedby = models.ForeignKey(User, on_delete=models.CASCADE,)




class Product(models.Model):
    product_image = models.ImageField(upload_to='images/product', blank=True, null=True)
    product_name = models.CharField(max_length=200)
    product_category = models.CharField(max_length=200)
    height = models.IntegerField()
    width = models.IntegerField()
    product_weight = models.IntegerField()
    product_color = models.CharField(max_length=200)
    product_description = models.TextField()
    product_price = models.IntegerField()
    product_manufacture = models.CharField(max_length=200)
    expirydate = models.DateField()
    manufacture_price = models.IntegerField()
    product_code = models.CharField(max_length=200)
    product_warranty = models.IntegerField()
    query_contact = models.IntegerField()
    product_gurantee = models.IntegerField()
    query_email = models.EmailField()
    addedby = models.ForeignKey(User, on_delete=models.DO_NOTHING)

    def __str__(self):
        return str('%s %s %s' % (self.product_name, self.product_price, self.id))

    


class Contact(models.Model):
    user_image = models.ImageField(upload_to='images/contact', blank=True, null=True)
    full_name = models.CharField(max_length=200)
    user_email = models.EmailField()
    user_phone = models.BigIntegerField()
    user_position = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)    
    company_location = models.CharField(max_length=200)
    addedby = models.ForeignKey(User, on_delete=models.CASCADE,)
    def __str__(self):
        return str('%s %s %s' % (self.full_name, self.id, self.company_name))




class Task(models.Model):
    
    attachment = models.FileField(upload_to='taskfile', blank=True, null=True)
    title = models.CharField(max_length=200)
    subject = models.CharField(max_length=200)
    related_to = models.CharField(max_length=200)
    deadline = models.DateField()
    status = models.CharField(max_length=200)    
    description = models.TextField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    addedby = models.ForeignKey(User, on_delete=models.CASCADE,)

    # def __str__(self):
    #     return self.addedby


class Deliveryboy(models.Model):
    user_image = models.ImageField(upload_to='images/deliveryboy', blank=True, null=True)
    full_name = models.CharField(max_length=200)
    user_email = models.EmailField()
    user_phone = models.BigIntegerField()
    identity = models.FileField(upload_to='images/deliveryboy', blank=True, null=True)
    gender = models.CharField(max_length=200)
    locality = models.TextField(max_length=200)    
    vehicle = models.TextField(max_length=200)
    addedby = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    def __str__(self):
        return self.full_name

        

class Sales(models.Model):
    customer = models.ForeignKey(Contact, on_delete=DO_NOTHING)
    product = models.ForeignKey(Product, on_delete=DO_NOTHING)
    product_price = models.BigIntegerField()
    quantity = models.IntegerField()
    total = models.IntegerField()    
    gst = models.IntegerField()
    discount = models.IntegerField()
    grand_total = models.BigIntegerField()
    deliveryboy = models.ForeignKey(Deliveryboy, on_delete=DO_NOTHING)
    order_date = models.DateField()
    delivery_date = models.DateField()
    addedby = models.ForeignKey(User, on_delete=DO_NOTHING)


class Contract(models.Model):
    attachment = models.FileField(upload_to='contractsfile', blank=True, null=True)
    customer = models.ForeignKey(Contact, on_delete=DO_NOTHING)
    subject = models.CharField(max_length=200)
    contract_value = models.BigIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    description = models.TextField(max_length=300)
    addedby = models.ForeignKey(User, on_delete=DO_NOTHING,)




class Profile(models.Model):
    userid = models.ForeignKey(User, on_delete=models.CASCADE)
    user_image = models.ImageField(upload_to='images/profile', blank=True, null=True)
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    user_email = models.EmailField(null=True, blank=True)
    user_phone = models.BigIntegerField(null=True, blank=True)
    dob = models.DateField(null=True, blank=True)
    gender = models.CharField(max_length=200, null=True, blank=True)
    points = models.BigIntegerField(null=True, blank=True)
    facebook = models.TextField(max_length=500, null=True, blank=True)
    instagram = models.TextField(max_length=500, null=True, blank=True)
    linkedin = models.TextField(max_length=500, null=True, blank=True)
    github = models.TextField(max_length=500, null=True, blank=True)
    about = models.TextField(max_length=1000, null=True, blank=True)
    project = models.CharField(max_length=200 ,default=False, blank=True)
    address = models.TextField(max_length=500, null=True, blank=True)
    id_proof = models.FileField(upload_to='images/profile/ids', blank=True, null=True)
    designation = models.CharField(max_length=200, null=True, blank=True)
    working_from = models.TimeField(null=True, blank=True)
    working_to = models.TimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.id


class Logs(models.Model):
    userid = models.ForeignKey(User, on_delete=DO_NOTHING,)
    description = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)
    profile_id = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, null=True)

class Documents(models.Model):
    document = models.FileField(upload_to='Documents/document', blank=True, null=True)
    title = models.CharField(max_length=200)
    addedby = models.ForeignKey(User, on_delete=DO_NOTHING,)

class Knowledge(models.Model):
    document = models.FileField(upload_to='Documents/knowledge', blank=True, null=True)
    title = models.CharField(max_length=200)
    addedby = models.ForeignKey(User, on_delete=DO_NOTHING,)


class Social(models.Model):
    facebook = models.TextField(max_length=500, null=True, blank=True)
    instagram = models.TextField(max_length=500, null=True, blank=True)
    linkedin = models.TextField(max_length=500, null=True, blank=True)
    github = models.TextField(max_length=500, null=True, blank=True)
    email = models.TextField(max_length=500, null=True, blank=True)
    phone = models.TextField(max_length=500, null=True, blank=True)
