import os
from typing import Optional

from dotenv import load_dotenv


load_dotenv()


class GeminiDocumentGenerator:
	def __init__(self):
		self.api_key = os.getenv("GEMINI_API_KEY", "").strip()
		self.model_name = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
		self.demo_mode = os.getenv("DEMO_MODE", "false").lower() == "true"
		self.client = None

	def _get_client(self):
		if self.client is None:
			if not self.api_key:
				raise ValueError(
					"GEMINI_API_KEY is missing. Add your Gemini API key to .env "
					"or set DEMO_MODE=true."
				)

			from google import genai

			self.client = genai.Client(api_key=self.api_key)

		return self.client

	def _create_prompt(
		self,
		document_type: str,
		parties: str,
		terms: str,
		effective_date: str,
		brand_name: str,
	) -> str:
		prompt = f"""
You are LegalEase, an AI assistant that creates
professional legal document drafts.

Create a complete editable draft.

DOCUMENT TYPE:
{document_type}

PARTIES:
{parties}

EFFECTIVE DATE:
{effective_date}

TERMS AND CONDITIONS:
{terms}

BRAND / ORGANIZATION:
{brand_name}

INSTRUCTIONS:

1. Create a professional legal-document draft.
2. Use clear headings.
3. Use numbered clauses.
4. Include the supplied parties.
5. Include the supplied effective date.
6. Include the supplied terms accurately.
7. Do not invent personal information.
8. Do not invent addresses.
9. Do not invent payment amounts.
10. Do not invent laws or legal citations.
11. If important information is missing, use placeholders such as [INSERT DETAILS].
12. Include appropriate sections such as Title, Parties, Purpose, Definitions when
necessary, Obligations, Terms and conditions, Confidentiality when appropriate,
Payment when appropriate, Termination when appropriate, Dispute resolution when
appropriate, and Signatures.
13. Use professional but understandable language.
14. Return plain text.
15. Do not use Markdown code blocks.
16. End with:

REVIEW NOTICE

This document is an AI-generated draft.
It is not legal advice and should be reviewed
by a qualified legal professional for the
applicable jurisdiction before use.

Generate the complete document.
"""
		return prompt.strip()

	def _demo_document(
		self,
		document_type: str,
		parties: str,
		terms: str,
		effective_date: str,
		brand_name: str,
	) -> str:
		term_list = [term.strip() for term in terms.split(";") if term.strip()]
		if not term_list:
			term_list = ["[INSERT TERMS]"]

		formatted_terms = "\n".join(
			f"{index}. {term}"
			for index, term in enumerate(term_list, start=1)
		)

		return f"""
{document_type.upper()}

{brand_name}

Effective Date: {effective_date}


1. PARTIES

{parties}


2. PURPOSE

This document records the general agreement
between the parties identified above.


3. TERMS AND CONDITIONS

{formatted_terms}


4. GENERAL PROVISIONS

The parties should review all provisions
applicable to their specific transaction.


5. TERMINATION

The parties should define the applicable
termination requirements and notice period.


6. SIGNATURES


PARTY 1

Name: ______________________________

Signature: _________________________

Date: ______________________________



PARTY 2

Name: ______________________________

Signature: _________________________

Date: ______________________________


REVIEW NOTICE

This is a demonstration document generated
without an external AI model.

It is not legal advice and should be reviewed
by a qualified legal professional before use.
""".strip()

	def generate_document(
		self,
		document_type: str,
		parties: str,
		terms: str,
		effective_date: str,
		brand_name: str = "LegalEase",
	) -> str:
		if not document_type.strip():
			raise ValueError("Document type is required.")
		if not parties.strip():
			raise ValueError("Parties are required.")
		if not terms.strip():
			raise ValueError("Terms are required.")
		if not effective_date.strip():
			raise ValueError("Effective date is required.")

		if self.demo_mode:
			return self._demo_document(
				document_type,
				parties,
				terms,
				effective_date,
				brand_name,
			)

		client = self._get_client()
		prompt = self._create_prompt(
			document_type,
			parties,
			terms,
			effective_date,
			brand_name,
		)
		response = client.models.generate_content(
			model=self.model_name,
			contents=prompt,
		)
		generated_text: Optional[str] = getattr(response, "text", None)

		if not generated_text:
			raise RuntimeError("Gemini returned an empty response.")

		return generated_text.strip()
