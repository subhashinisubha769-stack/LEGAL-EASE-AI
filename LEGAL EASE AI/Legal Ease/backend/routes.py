from fastapi import APIRouter, HTTPException

from backend.schemas import DocumentRequest
from ai_core.gemini_generator import GeminiDocumentGenerator


router = APIRouter()

generator = GeminiDocumentGenerator()


@router.get("/health")
def health_check():
	return {
		"status": "healthy",
		"service": "LegalEase API"
	}


@router.post("/generate")
def generate_document(request: DocumentRequest):
	try:
		generated_text = generator.generate_document(
			document_type=request.document_type,
			parties=request.parties,
			terms=request.terms,
			effective_date=request.effective_date,
			brand_name=request.brand_name,
		)

		return {
			"success": True,
			"document_type": request.document_type,
			"content": generated_text
		}

	except ValueError as error:
		raise HTTPException(
			status_code=400,
			detail=str(error)
		)

	except Exception as error:
		raise HTTPException(
			status_code=500,
			detail=f"Document generation failed: {error}"
		)
