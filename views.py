import os
import openai
from django.http import HttpResponse
from django.db import transaction
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from .models import *
from .logics import *
from .utils import *

openai.api_key = os.environ.get("OPENAI_KEY")

class WhatsappChatbot(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        whatsapp_number = request.POST.get('From').split("whatsapp:")[-1]
        obj1 = tbl_twilioconversation.objects.using("chatbotdb").filter(sender = whatsapp_number).order_by('-id')
        stringtheorm = tbl_twiliocontext.objects.using("chatbotdb").filter(owner = "hotel")
        companyprofile = tbl_twilioprefix.objects.using("chatbotdb").filter(owner = "hotel")
        datasuffix = tbl_twiliosuffix.objects.using("chatbotdb").filter(owner = "hotel")
        system = "You are an AI assistant acting as a hotel receptionist."
        body = request.POST.get('Body', '')
        messages=[{"role":"system", "content": system}]
        messages.append({"role": "user", "content": "User's latest request is: " + body + '. Check whether the latest request is related to hotel products, a greeting or polite expression (such as: Hello, How are you, Thank you, Goodbye, Good morning, Sorry, Excuse me, etc.), or completely unrelated. If it is hotel-related, return 1. If it is a greeting or polite phrase, return 2. If it is completely unrelated, return 0. Do not explain.'})
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
            messages1=[{"role":"system", "content": system}]       
            if companyprofile.count() > 0:
                messages1.append({"role": "user", "content": "Understand the following company profile data: " + str(companyprofile.last().prefix)})
                messages1.append({"role": "assistant", "content": "Acknowledge."})
            if stringtheorm.count() > 0:
                messages1.append({"role": "user", "content": "Understand the following JSON data: " + str(stringtheorm.last().context)})
                messages1.append({"role": "assistant", "content": "Acknowledge."})
            else:
                messages1.append({"role": "user", "content": "Please use all your knowledge about the hospitality industry."})
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
                messages1.append({"role": "user", "content": f"User's latest request is: {body}. Search for the answer using previous responses if relevant, or use the data in the JSON. If there is a formula, write it without LaTeX. Respond without reasoning unless requested by the user. Do not include emojis. " + str(datasuffix.last().suffix)})
            else:
                messages1.append({"role": "user", "content": f"User's latest request is: {body}. Search for the answer using previous responses if relevant, or use the data in the JSON. If there is a formula, write it without LaTeX. Respond without reasoning unless requested by the user. Do not include emojis."})
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
            messages1.append({"role": "user", "content": f"Calculate the response: {chatgpt_response1}, if the response exceeds 1600 characters, repeat the same response so that each segment is a maximum of 1500 characters. If it does not exceed the limit, return the response as is. Do not include emojis. Do not repeat the instructions."})
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
            messages2=[{"role":"system", "content": system}]
            messages2.append({"role": "user", "content": f"User's latest request is: {body}. This request doesn't appear to be related to hospitality products. Ask user kindly to resubmit a request that is relevant to the topic. Do not include emojis. Do not explain."})
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
            messages3=[{"role":"system", "content": system}]
            messages3.append({"role": "user", "content": f"User's latest request is: {body}. This request appears to be a greeting or a polite request. Please respond courteously and concisely, based on the greeting or request provided. Do not include emojis. Do not explain."})
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
