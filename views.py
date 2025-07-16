import os
import openai
from django.http import HttpResponse
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from chatbotappbianco.models import *
from bigptchatapp.logics import *
from .utils import send_message, logger

openai.api_key = os.environ.get("OPENAI_KEY")

class WhatsappChatbot(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        whatsapp_number = request.POST.get('From').split("whatsapp:")[-1]
        print(f"Sending the ChatGPT response to this number: {whatsapp_number}")
        obj1 = tbl_twilioconversation.objects.using("chatbotdb").filter(sender = whatsapp_number).order_by('-id')
        stringtheorm = tbl_twiliocontext.objects.using("chatbotdb").filter(owner = "bianco")
        companyprofile = tbl_twilioprefix.objects.using("chatbotdb").filter(owner = "bianco")
        datasuffix = tbl_twiliosuffix.objects.using("chatbotdb").filter(owner = "bianco")
        body = request.POST.get('Body', '')
        messages=[{"role":"system", "content": "Anda adalah AI assistant yang bertindak layaknya seorang receptionist hotel dari Bianco Costel."}]
        messages.append({"role": "user", "content": "Request terbaru user adalah : " + body + '. Periksa apakah request terbaru ini berhubungan dengan produk perhotelan Bianco Costel, atau merupakan kalimat salam dan permohonan (seperti contoh: Halo, Apa kabar, terima kasih, sampai jumpa, selamat pagi, mohon maaf, maaf dan sejenisnya), atau tidak ada hubungan sama sekali. Jika iya berhubungan kembalikan nilai 1, jika tidak sama sekali kembalikan nilai 0, jika kalimat salam kembalikan nilai 2. do not explain.'})
        response = openai.chat.completions.create(
                model="gpt-4.1-2025-04-14",
                messages=messages,
                max_tokens=32000,
                temperature=0.0,
                n=1,
                stop=None
            )
        chatgpt_response = response.choices[0].message.content if response.choices else "No choices found." 
        print(chatgpt_response)
        if chatgpt_response == "1":
            messages1=[{"role":"system", "content": "Anda adalah AI assistant yang bertindak layaknya seorang receptionist hotel dari Bianco Costel."}]       
            if companyprofile.count() > 0:
                messages1.append({"role": "user", "content": "Pahami data company profile berikut: " + str(companyprofile.last().prefix)})
                messages1.append({"role": "assistant", "content": "Acknowledge."})
            if stringtheorm.count() > 0:
                messages1.append({"role": "user", "content": "Pahami data json berikut: " + str(stringtheorm.last().context)})
                messages1.append({"role": "assistant", "content": "Acknowledge."})
            else:
                messages1.append({"role": "user", "content": "Tolong gunakan segala pengetahuanmu tentang perhotelan di Indonesia."})
                messages1.append({"role": "assistant", "content": "Acknowledge."})
            if obj1.count() > 0:
                a = 0
                for i in obj1:
                    if i.message != '' and i.response != '':
                        messages1.insert(3, {"role": "user", "content": i.message})
                        messages1.insert(4, {"role": "assistant", "content": i.response})
                    else:
                        pass
                    a = a + 1
                    if a == 5:
                        break 
            if datasuffix.count() > 0:
                messages1.append({"role": "user", "content": "Request terbaru user adalah : " + body + '. Cari jawaban menggunakan jawaban sebelumnya jika terkait atau gunakan data data dalam json. Jika terdapat rumus tuliskan tanpa Latex. Berikan respon tanpa reasoning kecuali diminta oleh user. Jangan beri emoji. ' + str(datasuffix.last().suffix)})
            else:
                messages1.append({"role": "user", "content": "Request terbaru user adalah : " + body + '. Cari jawaban menggunakan jawaban sebelumnya jika terkait atau gunakan data data dalam json. Jika terdapat rumus tuliskan tanpa Latex. Berikan respon tanpa reasoning kecuali diminta oleh user. Jangan beri emoji.'})
            response1 = openai.chat.completions.create(
                    model="gpt-4.1-2025-04-14",
                    messages=messages1,
                    max_tokens=32000,
                    temperature=0.0,
                    n=1,
                    stop=None
                )
            chatgpt_response1 = response1.choices[0].message.content if response1.choices else "No choices found." 
            messages1.append({"role": "assistant", "content": chatgpt_response1})
            messages1.append({"role": "user", "content": f"Hitung response: {chatgpt_response1} jika melebihi 1600 karakter ulangi response yang sama agar maksimal 1500 karakter, jika tidak melebihi maka kembalikan response tersebut saja. Jangan beri emoji. Jangan sebutkan kembali instruksi."})
            response2 = openai.chat.completions.create(
                    model="gpt-4.1-2025-04-14",
                    messages=messages1,
                    max_tokens=32000,
                    temperature=0.0,
                    n=1,
                    stop=None
                )
            chatgpt_response2 = response2.choices[0].message.content if response2.choices else "No choices found."
            try:
                with transaction.atomic():
                        conversation = tbl_twilioconversation.objects.using("chatbotdb").create(
                            sender=whatsapp_number,
                            message=body,
                            response=chatgpt_response2
                        )
                        conversation.save()     
                        logger.info(f"Conversation #{conversation.id} stored in database")
            except Exception as e:
                logger.error(f"Error storing conversation in database: {e}")
                return HttpResponse(status=500)
            send_message(whatsapp_number, chatgpt_response2)
        elif chatgpt_response == "0":
            messages2=[{"role":"system", "content": "Anda adalah AI assistant yang bertindak layaknya seorang receptionist hotel dari Bianco Costel."}]
            messages2.append({"role": "user", "content": "Request terbaru user adalah : " + body + '. Request ini sepertinya tidak ada hubungan dengan produk perhotelan Bianco Costel. Silakan membalas dengan bahasa yang sopan dan singkat bahwa request tersebut diluar topik dan minta user melakukan request ulang sesuai topik saja. Jangan beri emoji. do not explain.'})
            response3 = openai.chat.completions.create(
                    model="gpt-4.1-2025-04-14",
                    messages=messages2,
                    max_tokens=32000,
                    temperature=0.0,
                    n=1,
                    stop=None
                )
            chatgpt_response3 = response3.choices[0].message.content if response3.choices else "No choices found." 
            send_message(whatsapp_number, chatgpt_response3)
        elif chatgpt_response == "2":
            messages3=[{"role":"system", "content": "Anda adalah AI assistant yang bertindak layaknya seorang receptionist hotel dari Bianco Costel."}]
            messages3.append({"role": "user", "content": "Request terbaru user adalah : " + body + '. Request ini sepertinya adalah kalimat salam atau kalimat permohonan. Silakan membalas dengan bahasa yang sopan dan singkat sesuai salam atau permohonan yang diberikan. Jangan beri emoji. do not explain.'})
            response4 = openai.chat.completions.create(
                    model="gpt-4.1-2025-04-14",
                    messages=messages3,
                    max_tokens=32000,
                    temperature=0.0,
                    n=1,
                    stop=None
                )
            chatgpt_response4 = response4.choices[0].message.content if response4.choices else "No choices found." 
            send_message(whatsapp_number, chatgpt_response4)
        return HttpResponse('')