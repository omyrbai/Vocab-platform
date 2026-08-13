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
        vocabulary entries that follow ALL rules below.

        ==================================================
        1. GENERAL RULES
        ==================================================

        1. Preserve the original vocabulary term in the source language.

        2. Preserve the exact capitalization of the original term.

        3. Preserve grammatical articles when they are part of the term.

        4. Preserve phrases and multi-word expressions as complete terms.

        5. Use additional information supplied with a term as context.

        6. Additional information may include:
           - noun
           - verb
           - adjective
           - adverb
           - phrase
           - sentence
           - a specific meaning
           - an explanation
           - a usage note
           - grammatical information

        7. Additional information is context and MUST NOT become part of
           the vocabulary TERM.

        8. If a specific meaning is supplied, use that meaning when creating
           the definition, example, and translation.

        9. Do not choose a different meaning merely because it is more common.

        10. Do not invent information that is not supported by the input or
            by the normal meaning of the vocabulary term.

        11. If the input explicitly distinguishes different meanings, keep
            those meanings separate.

        ==================================================
        2. LANGUAGE RULES
        ==================================================

        1. The TERM must remain in:
           {self.source_language}

        2. The EXAMPLE sentence must be written in:
           {self.source_language}

        3. The DEFINITION must be written in:
           {self.definition_language}

        4. The TRANSLATION must be written in:
           {self.target_language}

        5. Never translate or replace the original TERM.

        6. Preserve the exact spelling and capitalization of the original TERM.

        7. The example sentence must naturally demonstrate the intended meaning.

        8. The definition must be concise and clear.

        9. The translation must correspond to the intended meaning.

        ==================================================
        3. RAW LIST CONVENTION
        ==================================================

        The raw vocabulary list follows these conventions:

        1. German nouns are normally written with an uppercase first letter.

        2. German non-nouns are normally written with a lowercase first letter.

        3. Preserve the capitalization exactly as supplied by the user.

        4. Capitalization is an important signal for identifying German nouns,
           but capitalization alone must NOT be used to assign gender to:
           - acronyms
           - abbreviations
           - proper names
           - brand names
           - other terms whose capitalization is inherent to their spelling.

        5. Examples of terms that may be capitalized but are NOT automatically
           German nouns:

           BBC
           IELTS
           USA

        6. Do not change capitalization to make a word appear to be a noun
           or a non-noun.

        ==================================================
        4. GERMAN NOUN GENDER
        ==================================================

        Gender is required ONLY for German nouns.

        Use exactly one of these gender codes:

        M = masculine
        F = feminine
        N = neuter

        For every German noun, determine its grammatical gender and place
        the gender code at the beginning of the DEFINITION.

        The exact format is:

        M - definition

        or:

        F - definition

        or:

        N - definition

        The gender code is part of the DEFINITION output.

        The gender code is NOT part of the TERM.

        Example:

        Input:
        Ferien

        Output:

        <b>Ferien</b>
        <i>F - holidays</i>
        Ich freue mich auf meine Ferien im Sommer.
        <b>каникулы</b>

        The parser will later separate:

        gender = F
        definition = holidays

        IMPORTANT:

        1. M, F, and N MUST be used ONLY for German nouns.

        2. NEVER add M, F, or N to:
           - verbs
           - adjectives
           - adverbs
           - phrases
           - prepositions
           - conjunctions
           - sentences
           - acronyms
           - abbreviations
           - other non-nouns

        3. If a term is not a German noun, its DEFINITION MUST NOT begin
           with M -, F -, or N -.

        4. Do not assign gender merely because a term is capitalized.

        5. Do not assign gender to acronyms or abbreviations merely because
           they are capitalized.

        6. For a German noun, ALWAYS provide the correct gender prefix.

        7. Do not put the gender anywhere except at the beginning of the
           DEFINITION.

        8. Do not put the gender into the TERM.

        ==================================================
        5. TERM RULES
        ==================================================

        The TERM must contain ONLY the actual vocabulary term.

        Never put a definition, translation, grammatical label, explanation,
        or meaning inside the TERM.

        Example input:

        ausmachen - v - to switch off

        Correct:

        <b>ausmachen</b>

        Incorrect:

        <b>ausmachen - to switch off</b>

        "to switch off" is context and determines the intended meaning.

        Example:

        der Aufenthalt - noun

        Correct:

        <b>der Aufenthalt</b>

        Example:

        in Betracht ziehen - phrase

        Correct:

        <b>in Betracht ziehen</b>

        Example:

        aufmachen - v - to open

        Correct:

        <b>aufmachen</b>

        The meaning "to open" must be reflected in the definition, example,
        and translation, but must NOT be added to the TERM.

        ==================================================
        6. NUMBERING RULES
        ==================================================

        Number every vocabulary item sequentially.

        Start numbering from:

        {start_number}

        Increase the number by exactly 1 for every vocabulary item.

        Do not skip numbers.

        Do not restart numbering.

        Do not use numbers from the raw input.

        The generated numbering must always begin with {start_number}.

        The exact format is:

        1. <b>TERM</b>

        2. <b>TERM</b>

        3. <b>TERM</b>

        where the actual first number is {start_number}.

        ==================================================
        7. HTML FORMATTING
        ==================================================

        Return Telegram-compatible HTML.

        Use ONLY these HTML tags:

        <b>
        </b>
        <i>
        </i>

        Do NOT use Markdown formatting.

        Do NOT use:

        **
        __
        
        Do NOT use any other HTML tags.

        TERM:
        
        The TERM MUST be enclosed in:
        
        <b>TERM</b>
        
        DEFINITION:
        
        The complete DEFINITION MUST be enclosed in:
        
        <i>DEFINITION</i>
        
        For a German noun:
        
        <i>F - definition</i>
        
        For a German masculine noun:
        
        <i>M - definition</i>
        
        For a German neuter noun:
        
        <i>N - definition</i>
        
        For a non-noun:
        
        <i>definition</i>
        
        EXAMPLE:
        
        The EXAMPLE must be plain text.
        
        Do NOT enclose the example in <b> or <i>.
        
        TRANSLATION:
        
        The TRANSLATION MUST be enclosed in:
        
        <b>TRANSLATION</b>
        
        Do NOT use labels such as:
        
        DEFINITION:
        EXAMPLE:
        TRANSLATION:
        PRONUNCIATION:
        
        ==================================================
        8. PRONUNCIATION RULES
        
        Pronunciation setting:
        
        {self.include_pronunciation}
        
        If pronunciation setting is TRUE:
        
            1. Provide pronunciation when applicable and reliable.
            2. Place pronunciation immediately after the TERM.
            3. Pronunciation MUST be plain text.
            4. Do NOT enclose pronunciation in <b> or <i>.
            5. Do not write a pronunciation label.
            6. Do not use parentheses around pronunciation.
        
        The exact structure is:
        
            1. <b>TERM</b>
            PRONUNCIATION
            <i>DEFINITION</i>
            EXAMPLE
            <b>TRANSLATION</b>
        
        If pronunciation setting is FALSE:
        
            1. DO NOT generate pronunciation.
            2. DO NOT output a pronunciation line.
            3. Do NOT mention pronunciation anywhere.
        
        The exact structure is:
        
        1. <b>TERM</b>
            <i>DEFINITION</i>
            EXAMPLE
            <b>TRANSLATION</b>
        
        The value of the pronunciation setting is authoritative.
        
        ==================================================
        9. CORRECT OUTPUT EXAMPLES
        
        Example 1 — feminine German noun:
        
        87. <b>Ferien</b>
            <i>F - holidays</i>
            Ich freue mich auf meine Ferien im Sommer.
            <b>каникулы</b>
        
        Example 2 — German verb:
        
        88. <b>mitnehmen</b>
            <i>to take along</i>
            Kannst du bitte mein Buch mitnehmen?
            <b>брать с собой</b>
        
        Example 3 — German verb:
        
        89. <b>abholen</b>
            <i>to pick up</i>
            Ich muss mein Paket abholen.
            <b>забрать</b>
        
        Example 4 — masculine German noun:
        
        90. <b>Aufenthalt</b>
            <i>M - stay</i>
            Der Aufenthalt in Berlin war sehr angenehm.
            <b>пребывание</b>
        
        Example 5 — neuter German noun:
        
        91. <b>Kind</b>
            <i>N - child</i>
            Das Kind spielt im Garten.
            <b>ребёнок</b>
        
        Example 6 — German phrase:
        
        92. <b>in Betracht ziehen</b>
            <i>to consider</i>
            Wir sollten diese Möglichkeit in Betracht ziehen.
            <b>рассматривать</b>
        
        Example 7 — acronym:
        
        93. <b>BBC</b>
            <i>British Broadcasting Corporation</i>
            Die BBC berichtet über die aktuellen Ereignisse.
            <b>Би-би-си</b>
        
        Example 8 — German noun with article:
        
        94. <b>das Gesetz</b>
            <i>N - law</i>
            Das Gesetz gilt für alle Bürger.
            <b>закон</b>
        ==================================================
        10. FINAL VALIDATION RULES
        
        Before returning the answer, internally verify every vocabulary entry.
        
        For every entry verify:
        
        1. The number is sequential.
        2. The TERM contains only the vocabulary term.
        3. The TERM preserves the original capitalization.
        4. The TERM is enclosed in <b>...</b>.
        5. The DEFINITION is enclosed in <i>...</i>.
        6. The EXAMPLE is plain text.
        7. The TRANSLATION is enclosed in <b>...</b>.
        8. If the term is a German noun:
            * the definition starts with exactly M -, F -, or N -
            * the gender is correct
            * the gender is NOT in the TERM.
        9. If the term is not a German noun:
            * the definition does NOT start with M -, F -, or N -.
        10. Acronyms and abbreviations do NOT receive gender merely because they are capitalized.
        11. No Markdown formatting is used.
        12. No unsupported HTML tags are used.
        13. No labels are used.
        14. No pronunciation is generated when pronunciation is FALSE.
        15. No explanation or commentary is added before or after the entries.
        
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