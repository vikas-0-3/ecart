from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.db.models import fields
from .models import Lead, Product, Contact, Social, Task, Contract, Sales, Deliveryboy, Logs, Profile, Documents, Knowledge, Social, Quotations, Quoteitem, Leave, Claim


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class LeadForm(forms.ModelForm):
    class Meta:
        model = Lead
        fields = [
            "company_name",
            "website",
            "email",
            "phone",
            "contact_person",
            "country",
            "state",
            "city",
            "czip",
            "title",
            "status",
            "source",
            "assigned_to",
            "addedby",
        ]

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = [
            "product_image",
            "product_name",
            "product_category",
            "height",
            "width",
            "product_weight",
            "product_color",
            "product_description",
            "product_price",
            "product_manufacture",
            "expirydate",
            "manufacture_price",
            "product_code",
            "product_warranty",
            "query_contact",
            "product_gurantee",
            "query_email",
            "addedby",
        ]

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = [
            "user_image",
            "full_name",
            "user_email",
            "user_phone",
            "user_position",
            "company_name",
            "company_location",
            "addedby",
        ]

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            "attachment",
            "title",
            "subject",
            "related_to",
            "deadline",
            "status",
            "description",
            "addedby",
        ]

class SalesForm(forms.ModelForm):
    class Meta:
        model = Sales
        fields =  [
            "quotation",
            "vendor",
            "vendor_price",
            "payment_mode",
            "our_price",
            "payment_status",
            "profit",
            "deliveryboy",
            "order_date",
            "delivery_date",
            "addedby",
        ]

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = [
            "attachment",
            "customer",
            "subject",
            "contract_value",
            "start_date",
            "end_date",
            "description",
            "addedby",
        ]

class DeliveryboyForm(forms.ModelForm):
    class Meta:
        model = Deliveryboy
        fields = [
            "user_image",
            "full_name",
            "user_email",
            "user_phone",
            "identity",
            "gender",
            "locality",
            "vehicle",
            "addedby",
        ]

class LogsForm(forms.ModelForm):
    class Meta:
        model = Logs
        fields = [
            "userid",
            "description",
            "profile_id",
        ]

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = [
            "userid",
            "user_image",
            "first_name",
            "last_name",
            "user_email",
            "user_phone",
            "dob",
            "gender",
            "points",
            "facebook",
            "instagram",
            "linkedin",
            "github",
            "about",
            "project",
            "address",
            "id_proof",
            "designation",
            "working_from",
            "working_to",

        ]

class DocumentsForm(forms.ModelForm):
    class Meta:
        model = Documents
        fields = [
            "document",
            "title",
            "addedby",
        ]

class KnowledgeForm(forms.ModelForm):
    class Meta:
        model = Knowledge
        fields = [
            "document",
            "title",
            "addedby",
        ]


class SocialForm(forms.ModelForm):
    class Meta:
        model = Social
        fields = [
            "facebook",
            "instagram",
            "linkedin",
            "github",
            "email",
            "phone",
            "website",
            "twitter",
        ]


class QuotationsForm(forms.ModelForm):
    class Meta:
        model = Quotations
        fields = [  
            "customer_name",
            "title",
            "note",
            "status",
            "discount",
            "shipping",
            "tax",
            "grand_total",
            "addedby",
        ]

class QuoteitemForm(forms.ModelForm):
    class Meta:
        model = Quoteitem
        fields = [  
            "quotation_id",
            "product_code",
            "product_name",
            "product_price",
            "product_quantity",
            "product_total",
        ]

class LEaveForm(forms.ModelForm):
    class Meta:
        model = Leave
        fields = [
            "purpose",
            "from_date",
            "to_date",
            "description",
            "status",
            "addedby",
        ]

class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = [
            "purpose",
            "title",
            "from_date",
            "to_date",
            "amount",
            "description",
            "status",
            "addedby",
        ]
