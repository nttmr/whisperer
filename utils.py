import whisper
import openai

# Make sure to set up your OpenAI API key before using the run_prompt function

from tempfile import NamedTemporaryFile

def transcriptor(uploaded_file, model_size, language):
    """
    Transcribes the audio using the Whisper model.

    Args:
    - uploaded_file (UploadedFile): The uploaded audio file from the user.
    - model_size (str): The chosen model size (e.g., "Small", "Medium", "Large").
    - language (str): The chosen language for transcription (e.g., "English", "Spanish").

    Returns:
    - str: The raw text transcription of the audio.
    """
    with NamedTemporaryFile(suffix="mp3") as temp:
        temp.write(uploaded_file.getvalue())
        temp.seek(0)
        # Load the Whisper model based on the selected size
        model = whisper.load_model(model_size)

        # Transcribe the audio using the Whisper model
        result = model.transcribe(temp.name, language=language, fp16=False, verbose=True)

        return result["text"]

def run_prompt(prompt):
    """
    Executes a prompt using the OpenAI ChatCompletion API.

    Args:
    - prompt (str): The prompt text to be sent to the OpenAI API.

    Returns:
    - str: The response from the OpenAI model.
    """
    # Create the message structure for the API
    messages = [{'role': 'user', 'content': prompt}]

    # Execute the prompt using the OpenAI API
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    text = response['choices'][0]['message']['content']
    return text


def structurer(raw_transcription, structure_pref):
    """
    Structures the transcription according to the user's preference.

    Args:
    - raw_transcription (str): The raw text transcription from the `transcriptor` function.
    - structure_pref (str): The user's chosen structure preference (e.g., "Article", "Simple Note").

    Returns:
    - str: The structured transcription.
    """

    # Step 1: Extract important topics from the raw transcription
    topics_prompt = f"From the following text, extract a list of important topics: {raw_transcription}"
    topics = run_prompt(topics_prompt)

    # Step 2: Transform and merge similar topics to generate an outline
    outline_prompt = f"Transform and merge the following topics to generate an outline for a {structure_pref.lower()}: {topics}"
    outline = run_prompt(outline_prompt)

    # Step 3: Reconstruct the raw transcription based on the generated outline
    map_prompt = "Given the following raw transcription and outline, generate text that follows the structure given in the outline:"
    structuring_prompt = f"{map_prompt}\n\nRaw Transcription: {raw_transcription}\n\nOutline: {outline}"
    structured_transcription = run_prompt(structuring_prompt)

    return structured_transcription


def formatter(structured_transcription, format_pref):
    """
    Formats the structured transcription based on user preferences.

    Args:
    - structured_transcription (str): The structured transcription from the `structurer` function.
    - format_pref (list): List of chosen formatting preferences (e.g., ["All lowercase", "Spellcheck"]).

    Returns:
    - str: The formatted transcription.
    """
    formatted_text = structured_transcription

    # Apply formatting
    if "All lowercase" in format_pref:
        formatted_text = formatted_text.lower()

    # Placeholder logic for spellcheck and correct orthography.
    # For now, we will assume the text is already correctly spelled and has correct orthography.
    if "Spellcheck" in format_pref:
        pass
    if "Correct orthography" in format_pref:
        pass

    return formatted_text
