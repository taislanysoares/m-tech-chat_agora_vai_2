import json
import os
import webbrowser  # Importa a biblioteca para abrir sites
import speech_recognition as sr  # Para reconhecimento de voz
import pyttsx3  # Para resposta de voz

def falar(texto):
    engine = pyttsx3.init()
    engine.say(texto)
    engine.runAndWait()

def ouvir_comando():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Diga algo...")
        try:
            audio = recognizer.listen(source)
            comando = recognizer.recognize_google(audio, language="pt-BR")
            print(f"Você disse: {comando}")
            return comando.lower()
        except sr.UnknownValueError:
            print("Não entendi o que você disse. Tente novamente.")
            return ""
        except sr.RequestError as e:
            print(f"Erro ao acessar o serviço de reconhecimento de voz: {e}")
            return ""

def carregar_faq():
    if os.path.exists("faq.json"):
        with open("faq.json", "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return {}

def salvar_faq(faq):
    with open("faq.json", "w", encoding="utf-8") as f:
        json.dump(faq, f, ensure_ascii=False, indent=4)

def treinar_bot(faq):
    print("Modo de treinamento iniciado. Diga 'sair' para sair.")
    while True:
        pergunta = input("Pergunta: ").strip()
        if pergunta.lower() == "sair":
            break
        resposta = input("Resposta: ").strip()
        if not pergunta or not resposta:
            print("Pergunta ou resposta inválida! Tente novamente.")
            continue
        faq[pergunta] = resposta
        print("Treinamento concluído!")
    salvar_faq(faq)

def chatbot(faq):
    print("Chatbot: Olá! Sou seu assistente virtual. Pergunte algo ou diga 'sair' para encerrar.")
    while True:
        entrada_usuario = input("Você: ").strip()
        if entrada_usuario.lower() in ["sair", "tchau", "adeus"]:
            print("Chatbot: Até logo! Espero ter ajudado.")
            break
        elif entrada_usuario in faq:
            print(f"Chatbot: {faq[entrada_usuario]}")
        elif any(frase in entrada_usuario.lower() for frase in ["bater o ponto", "preciso bater o ponto", "abre o ponto pra mim", "tenho que bater o ponto", "bater ponto"]):
            print("Chatbot: Abrindo o site para bater o ponto...")
            webbrowser.open("http://192.168.1.80:4000")  # Substitua pelo URL do site real
        elif "voz" in entrada_usuario.lower():
            print("Chatbot: Você quer usar comando de voz? Diga o site que deseja abrir.")
            falar("Você quer usar comando de voz? Diga o site que deseja abrir.")
            comando = ouvir_comando()
            if "abra o youtube" in comando:
                print("Chatbot: Abrindo o YouTube...")
                falar("Abrindo o YouTube")
                webbrowser.open("https://www.youtube.com")
            elif "abrir" in comando:
                site = comando.replace("abrir", "").strip()
                if " " in site:
                    site = site.replace(" ", "")
                if not site.endswith(".com"):
                    site += ".com"
                print(f"Abrindo {site}...")
                falar(f"Abrindo {site}")
                webbrowser.open(f"http://{site}")
            else:
                print("Chatbot: Não consegui identificar o site. Tente novamente.")
                falar("Não consegui identificar o site. Tente novamente.")
        else:
            print("Chatbot: Hmm, eu ainda não sei responder isso. Você pode me ensinar?")
            treinar_bot(faq)

def principal():
    faq = carregar_faq()
    while True:
        print("\nEscolha uma opção:")
        print("1. Iniciar chat")
        print("2. Treinar chatbot")
        print("3. Sair")
        escolha = input("Escolha: ").strip()
        if escolha == "1":
            chatbot(faq)
        elif escolha == "2":
            treinar_bot(faq) 
        elif escolha == "3":
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    principal()
