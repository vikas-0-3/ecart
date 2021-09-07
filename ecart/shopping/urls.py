from typing import ValuesView
from django.urls import path, include
from shopping import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.dashboard, name="dashboard"),
    path('login', views.loginuser, name="login"),
    path('logout', views.logoutuser, name="logout"),
    path('register', views.register, name="register"),
    path('home', views.home, name="home"),

    path('email', views.email, name="email"),
    path('getMyEvents', views.getMyEvents, name="getMyEvents"),
    
    path('profile', views.profile, name="profile"),
    path('editprofile', views.editprofile, name="editprofile"),

    path('adduser', views.adduser, name="adduser"),
    path('userprofiles', views.userprofiles, name="userprofiles"),
    path('deleteuser/<id>', views.deleteuser, name="deleteuser"),
    path('edituserprofile/<id>', views.edituserprofile, name="edituserprofile"),

    

    path('calander', views.calander, name="calander"),

    path('chat', views.chat, name="chat"),
    path('send', views.send, name="send"),
    path('getMessages', views.getMessages, name="getMessages"),

    path('documents', views.documents, name="documents"),
    path('deletedoc/<id>', views.deletedoc, name="deletedoc"),

    path('knowledge', views.knowledge, name="knowledge"),
    path('deleteknowledge/<id>', views.deleteknowledge, name="deleteknowledge"),
    

    path('logs', views.logs, name="logs"),
    path('socialhandle', views.socialhandle, name="socialhandle"),


    path('contracts', views.contracts, name="contracts"),
    path('addcontract', views.addcontract, name="addcontract"),
    path('editcontract/<id>', views.editcontract, name="editcontract"),
    path('deletecontract/<id>', views.deletecontract, name="deletecontract"),

    path('sales', views.sales, name="sales"),
    path('addsale', views.addsale, name="addsale"),
    path('editsale/<id>', views.editsale, name="editsale"),
    path('deletesale/<id>', views.deletesale, name="deletesale"),

    path('contact', views.contact, name="contact"),
    path('addcontact', views.addcontact, name="addcontact"),
    path('editcontact/<id>', views.editcontact, name="editcontact"),
    path('deletecontact/<id>', views.deletecontact, name="deletecontact"),

    path('contactqrcode/<id>', views.contactqrcode, name="contactqrcode"),

    path('products', views.products, name="products"),
    path('addproduct', views.addproduct, name="addproduct"),
    path('editproduct/<id>', views.editproduct, name="editproduct"),
    path('deleteproduct/<id>', views.deleteproduct, name="deleteproduct"),

    path('lead', views.lead, name="lead"),
    path('addlead', views.addlead, name="addlead"),
    path('editlead/<id>', views.editlead, name="editlead"),
    path('deletelead/<id>', views.deletelead, name="deletelead"),

    path('tasks', views.tasks, name="tasks"),
    path('addtask', views.addtask, name="addtask"),
    path('edittask/<id>', views.edittask, name="edittask"),
    path('deletetask/<id>', views.deletetask, name="deletetask"),

    path('deliveryboy', views.deliveryboy, name="deliveryboy"),
    path('adddeliveryboy', views.adddeliveryboy, name="adddeliveryboy"),
    path('editdeliveryboy/<id>', views.editdeliveryboy, name="editdeliveryboy"),
    path('deletedeliveryboy/<id>', views.deletedeliveryboy, name="deletedeliveryboy"),

    path('quotation', views.quotation, name="quotation"),
    path('addquotation', views.addquotation, name="addquotation"),
    path('deletequotation/<id>', views.deletequotation, name="deletequotation"),
    path('viewquotation/<id>', views.viewquotation, name="viewquotation"),


    path('leave', views.leave, name="leave"),
    path('editleave/<id>', views.editleave, name="editleave"),
    path('deleteleave/<id>', views.deleteleave, name="deleteleave"),
    path('manageleave', views.manageleave, name="manageleave"),
    path('acceptleave/<id>', views.acceptleave, name="acceptleave"),
    path('declineleave/<id>', views.declineleave, name="declineleave"),

    
    path('claim', views.claim, name="claim"),
    path('editclaim/<id>', views.editclaim, name="editclaim"),
    path('deleteclaim/<id>', views.deleteclaim, name="deleteclaim"),
    path('manageclaim', views.manageclaim, name="manageclaim"),
    path('acceptclaim/<id>', views.acceptclaim, name="acceptclaim"),
    path('declineclaim/<id>', views.declineclaim, name="declineclaim"),
    
    
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT)


    