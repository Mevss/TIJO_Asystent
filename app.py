from flask import Flask, render_template, request
from google import genai
import os

app = Flask(__name__)

client = genai.Client(api_key="")


@app.route("/", methods=["GET", "POST"])
def home():
    response_text = ""
    if request.method == "POST":
        user_input = request.form.get("user_input")
        language = request.form.get("language")
        functionality = request.form.get("functionality")
        length = request.form.get("length")

        uploaded_file = request.files.get('file')
        file_content = ""

        if uploaded_file and uploaded_file.filename != '':
            try:
                file_extension = uploaded_file.filename.split('.')[-1].lower()
                if file_extension in ['py', 'txt', 'js', 'html', 'css', 'json', 'xml', 'md']:
                    file_content = uploaded_file.read().decode('utf-8')
                    file_content = f"\n\nZawartość pliku '{uploaded_file.filename}':\n```{file_extension}\n{file_content}\n```"
                else:
                    file_content = f"\n\nPlik '{uploaded_file.filename}' ma nieobsługiwany format."
            except Exception as e:
                file_content = f"\n\nBłąd podczas odczytu pliku: {str(e)}"

        prompt_templates = {
            "polish": {
                "unit_tests": "Jesteś ekspertem od testowania oprogramowania. Twoim zadaniem jest wygenerowanie testów jednostkowych dla poniższego fragmentu kodu. Skup się na pokryciu kluczowych ścieżek i przypadków brzegowych.",
                "code_quality": "Jesteś światowej klasy starszym programistą i ekspertem od jakości kodu. Przeanalizuj poniższy fragment kodu pod kątem naruszeń zasad SOLID, prawa Demeter, typowych błędów i złych praktyk. Zaproponuj konkretne poprawki.",
                "test_cases": "Jesteś doświadczonym analitykiem QA. Twoim zadaniem jest wygenerowanie listy przypadków testowych (test cases) dla funkcjonalności opisanej w poniższym tekście. Twórz je w formacie: ID, Tytuł, Opis, Kroki do wykonania, Dane wejściowe, Oczekiwany rezultat. Prezentuj je w formie czytelnej listy.",
            },
            "english": {
                "unit_tests": "You are a software testing expert. Your task is to generate unit tests for the code fragment below. Focus on covering key paths and edge cases.",
                "code_quality": "You are a world-class senior programmer and code quality expert. Analyze the code fragment below for SOLID principle violations, Law of Demeter violations, common bugs, and bad practices. Suggest specific improvements.",
                "test_cases": "You are an experienced QA analyst. Your task is to generate a list of test cases for the functionality described in the text below. Create them in this format: ID, Title, Description, Test steps, Test data, Expected result. Present them in a readable list format.",
            }
        }

        length_modifiers = {
            "polish": {
                "short": "Odpowiadaj zwięźle i konkretnie, bez zbędnych wyjaśnień. Skup się tylko na najważniejszych punktach. Wypisz kod.",
                "long": "Odpowiadaj szczegółowo z dokładnymi wyjaśnieniami. Opisz dokładnie co jest złe, dlaczego i jak to poprawić. Wypisz kod."
            },
            "english": {
                "short": "Respond concisely and to the point, without unnecessary explanations. Focus only on the most important points. Write the code.",
                "long": "Respond in detail with thorough explanations. Describe exactly what is wrong, why, and how to fix it. Write the code."
            }
        }

        lang_templates = prompt_templates.get(language, prompt_templates["polish"])
        lang_length_modifiers = length_modifiers.get(language, length_modifiers["polish"])

        role_prompt = lang_templates.get(functionality, "Jesteś pomocnym asystentem." if language == "polish" else "You are a helpful assistant.")

        length_modifier = lang_length_modifiers.get(length, "")

        final_prompt = f"{role_prompt} {length_modifier}\n\nOto dane wejściowe od użytkownika:\n```\n{user_input}\n```{file_content}"

        response = client.models.generate_content(
            model="gemini-2.0-flash", contents=final_prompt
        )
        response_text = response.text

    return render_template("index.html", response_text=response_text)


if __name__ == "__main__":
    app.run()
