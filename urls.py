from django.urls import path
from . import views, cms

urlpatterns = [
    path("", cms.index, name="bianco_index"),
    path("<str:id>/setup/", cms.biancosetup, name="bianco_setup"),
    path("<str:id>/templates/", cms.biancotemplates, name="bianco_templates"),
    path("data/prefix/saved/", cms.instruksicpsaved),
    path("data/suffix/saved/", cms.instruksisuffixsaved),
    path("file/upload/", cms.fileuploadbianco, name="file_upload"),
    path("file/konversi/pdf/", cms.konversi_started_pdf),
    path("file/konversi/excel/", cms.konversi_started_excel),
    path("template/konversi/", cms.templatekonversi),
    path("template/sent/blast/", cms.sendblasttemplate),
    path("message/", views.WhatsappChatbot.as_view()),
    path("template/submit/text/", cms.contenttypetextapi),
    path("template/submit/media/", cms.contenttypemediaapi),
    path("template/get/status/", cms.get_template_status, name="get_template_status"),
    path("template/delete/<str:sid>/", cms.delete_template, name='delete_template'),
    path("template/get/content/<str:sid>/", cms.get_content_template, name='get_content_template'),
    path("template/get/approved/", cms.get_template_approved, name="get_template_approved"),
    path("template/get/approved/detail/<str:content_sid>/", cms.get_template_approved_detail, name="get_template_approved_detail"),
]