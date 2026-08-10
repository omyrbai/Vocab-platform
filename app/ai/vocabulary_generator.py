from groq import Groq

from app.core.settings import settings


class VocabularyGenerator:

    def __init__(
        self,
        source_language: str,
        target_language: str,
        definition_language: str,
        include_pronunciation: bool = False,
    ):
        self.source_language = source_language
        self.target_language = target_language
        self.definition_language = definition_language
        self.include_pronunciation = include_pronunciation

        self.client = Groq(
            api_key=settings.GROQ_API_KEY,
        )

    def generate(
        self,
        text: str,
        start_number: int,
    ) -> str:
        """
        Generate structured vocabulary from raw terms.
        """

        prompt = f"""
        You are a vocabulary-generation assistant.

        SOURCE LANGUAGE
        {self.source_language}

        TARGET LANGUAGE
        {self.target_language}

        DEFINITION LANGUAGE
        {self.definition_language}

        PRONUNCIATION REQUIRED
        {self.include_pronunciation}

        The user will provide a raw vocabulary list.

        Your task is to transform the raw vocabulary list into structured
        vocabulary entries.

        GENERAL RULES

        1. Preserve the original vocabulary term in the source language.
        2. Preserve grammatical articles when they are part of the term.
        3. Preserve phrases and multi-word expressions as complete terms.
        4. Use any additional information supplied with a term as context.
        5. Additional information may include:
           - noun
           - verb
           - adjective
           - adverb
           - phrase
           - sentence
           - a specific meaning
           - an explanation
           - a usage note
        6. Additional information is context and must NOT become part of
           the vocabulary term.
        7. If a specific meaning is supplied, use that meaning when creating
           the definition, example, and translation.
        8. Do not choose a different meaning merely because it is more common.
        9. Do not invent information.
        10. Keep different meanings separate when the input explicitly
            distinguishes them.

        LANGUAGE RULES

        1. The TERM must remain in the source language:
           {self.source_language}

        2. The EXAMPLE sentence must be written in:
           {self.source_language}

        3. The DEFINITION must be written in:
           {self.definition_language}

        4. The TRANSLATION must be written in:
           {self.target_language}

        5. Do not translate or replace the original TERM.

        6. The example sentence must naturally demonstrate the intended
           meaning of the term.

        7. The definition should be concise and clear.

        8. The translation should correspond to the intended meaning,
           not merely to another possible meaning of the word.

        TERM RULES

        The vocabulary term must contain ONLY the actual term.

        For example, if the input is:

        ausmachen - v - to switch off

        the output term MUST be:

        <b>ausmachen</b>

        NOT:

        <b>ausmachen - to switch off</b>

        The phrase "to switch off" is context that determines the meaning.

        If the input is:

        der Aufenthalt - noun

        the output term MUST be:

        <b>der Aufenthalt</b>

        If the input is:

        in Betracht ziehen - phrase

        the output term MUST be:

        <b>in Betracht ziehen</b>

        If the input is:

        aufmachen - v - to open

        the output term MUST be:

        <b>aufmachen</b>

        The meaning "to open" must be reflected in the definition,
        example, and translation, but must NOT be added to the term.

        FORMATTING RULES

        Return ONLY the structured vocabulary entries.

        Do NOT add:
        - headings
        - introductions
        - explanations
        - comments
        - conclusions
        - bullet points
        - numbered explanations
        - markdown code blocks

        Number every vocabulary item sequentially.

        Start numbering from {start_number}.
        Increase the number by 1 for each vocabulary item.

        Do not skip numbers.
        Do not restart numbering.

        Use Telegram-compatible HTML formatting.

        TERM FORMATTING

        The TERM MUST be enclosed in <b> and </b>:

        <b>TERM</b>

        DEFINITION FORMATTING

        The DEFINITION MUST be enclosed in <i> and </i>:

        <i>DEFINITION</i>

        EXAMPLE FORMATTING

        The EXAMPLE sentence MUST be plain text.

        Do NOT enclose the example in <b>, </b>, <i>, or </i>.

        TRANSLATION FORMATTING

        The TRANSLATION MUST be enclosed in <b> and </b>:

        <b>TRANSLATION</b>

        Do NOT use labels such as:

        DEFINITION:
        EXAMPLE:
        TRANSLATION:
        PRONUNCIATION:

        PRONUNCIATION RULES

        Pronunciation setting:

        {self.include_pronunciation}

        If pronunciation setting is TRUE:

        1. Provide pronunciation when applicable and reliable.
        2. Place pronunciation immediately after the term.
        3. Pronunciation MUST be plain text.
        4. Do NOT enclose pronunciation in <b>, </b>, <i>, or </i>.
        5. Do not write a pronunciation label.
        6. Do not use parentheses around pronunciation.

        Use this exact structure:

        1. <b>TERM</b>
        PRONUNCIATION
        <i>DEFINITION</i>
        EXAMPLE
        <b>TRANSLATION</b>

        If pronunciation setting is FALSE:

        1. DO NOT generate pronunciation.
        2. DO NOT output a pronunciation line.
        3. Do NOT use pronunciation formatting.

        Use this exact structure:

        1. <b>TERM</b>
        <i>DEFINITION</i>
        EXAMPLE
        <b>TRANSLATION</b>

        The value of the pronunciation setting is authoritative.
        Never include pronunciation when it is FALSE.

        CORRECT EXAMPLE WHEN PRONUNCIATION IS FALSE

        1. <b>aufstehen</b>
        <i>to get up</i>
        Ich stehe jeden Morgen um sieben Uhr auf.
        <b>вставать</b>

        2. <b>der Aufenthalt</b>
        <i>a stay</i>
        Der Aufenthalt in Berlin war sehr angenehm.
        <b>пребывание</b>

        3. <b>ausmachen</b>
        <i>to switch off</i>
        Kannst du bitte das Licht ausmachen?
        <b>выключать</b>

        4. <b>in Betracht ziehen</b>
        <i>to consider</i>
        Wir sollten diese Möglichkeit in Betracht ziehen.
        <b>рассматривать</b>

        CORRECT EXAMPLE WHEN PRONUNCIATION IS TRUE

        1. <b>aufstehen</b>
        ˈaʊ̯fˌʃteːən
        <i>to get up</i>
        Ich stehe jeden Morgen um sieben Uhr auf.
        <b>вставать</b>

        IMPORTANT

        Never add the meaning, definition, translation, grammatical label,
        or explanation to the TERM.

        Never output pronunciation when the pronunciation setting is FALSE.

        Never make the example bold or italic.

        Never use labels such as DEFINITION:, EXAMPLE:, TRANSLATION:,
        or PRONUNCIATION:.

        Use only the HTML tags explicitly specified above:
        <b>, </b>, <i>, </i>.

        Return ONLY the vocabulary entries.

        The raw vocabulary list is:

        {text}
        """

        response = self.client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
        )

        return response.choices[0].message.content.strip()