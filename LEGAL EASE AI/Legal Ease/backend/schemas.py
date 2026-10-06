from pydantic import BaseModel, Field


class DocumentRequest(BaseModel):
	document_type: str = Field(
		...,
		min_length=2,
		max_length=120
	)

	parties: str = Field(
		...,
		min_length=2,
		max_length=4000
	)

	terms: str = Field(
		...,
		min_length=2,
		max_length=12000
	)

	effective_date: str = Field(
		...,
		min_length=2,
		max_length=100
	)

	brand_name: str = Field(
		default="LegalEase",
		max_length=120
	)
