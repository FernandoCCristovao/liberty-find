"""Contratos de dados do projeto.

Fonte da verdade em prosa: docs/dados/contratos.md. Mudou um campo aqui, mude lá
e nos testes no mesmo commit.
"""

from __future__ import annotations

from datetime import datetime
from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class Source(StrEnum):
    """ATS com API pública de vagas (ver docs/dados/fontes.md)."""

    GREENHOUSE = "greenhouse"
    LEVER = "lever"
    ASHBY = "ashby"
    WORKABLE = "workable"


class Board(BaseModel):
    """Uma empresa numa fonte, como está em boards.yaml."""

    model_config = ConfigDict(frozen=True, extra="forbid")

    source: Source
    token: str = Field(min_length=1, pattern=r"^[a-z0-9][a-z0-9._-]*$")
    company: str = Field(min_length=1)
    enabled: bool = True


class JobPosting(BaseModel):
    """Vaga normalizada: o mesmo formato para todas as fontes.

    `description_text` serve só para extração e busca internas. Nunca é publicado.
    """

    model_config = ConfigDict(frozen=True, extra="forbid")

    posting_id: str = Field(description="<source>:<board>:<source_job_id>")
    source: Source
    board: str
    company: str
    source_job_id: str
    title: str
    url: str = Field(pattern=r"^https://")
    location: str | None = None
    workplace_type: str | None = Field(
        default=None,
        description="Como a fonte informa (remote, hybrid, onsite); None se não informa",
    )
    country: str | None = None
    department: str | None = None
    language: str | None = None
    description_text: str
    content_hash: str = Field(pattern=r"^[0-9a-f]{64}$")
    published_at: datetime | None = None
    updated_at: datetime | None = None
    collected_at: datetime


# --- Campos extraídos por LLM (Marco 1, tarefa 1.6; detalhes em docs/dados/extracao.md) ---


class RoleFamily(StrEnum):
    AI = "ai"
    DATA_ENGINEERING = "data_engineering"
    ANALYTICS_BI = "analytics_bi"
    ANALYTICS_ENGINEERING = "analytics_engineering"
    AUTOMATION = "automation"
    SOFTWARE = "software"
    OTHER = "other"


class Seniority(StrEnum):
    INTERN = "intern"
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    STAFF_PLUS = "staff_plus"
    MANAGER = "manager"
    NOT_INFORMED = "not_informed"


class WorkModel(StrEnum):
    REMOTE = "remote"
    HYBRID = "hybrid"
    ONSITE = "onsite"
    NOT_INFORMED = "not_informed"


class ContractType(StrEnum):
    CLT = "clt"
    PJ = "pj"
    OTHER = "other"
    NOT_INFORMED = "not_informed"


class EnglishLevel(StrEnum):
    NONE = "none"
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    FLUENT = "fluent"
    NOT_INFORMED = "not_informed"


class Currency(StrEnum):
    BRL = "BRL"
    USD = "USD"
    EUR = "EUR"


class SalaryPeriod(StrEnum):
    MONTH = "month"
    YEAR = "year"
    HOUR = "hour"


class ExtractedFields(BaseModel):
    """O que o LLM devolve para uma vaga. O esquema da ferramenta do Bedrock espelha isto."""

    model_config = ConfigDict(extra="forbid")

    role_family: RoleFamily
    seniority: Seniority
    work_model: WorkModel
    contract_type: ContractType
    english_level: EnglishLevel
    english_required: bool | None = Field(
        description="True se obrigatório; False se desejável; None se não citado"
    )
    salary_min: float | None
    salary_max: float | None
    salary_currency: Currency | None
    salary_period: SalaryPeriod | None
    years_experience_min: int | None = Field(ge=0, le=30)
    stack: list[str] = Field(max_length=15, description="Nomes canônicos em minúsculas")


class ExtractionRecord(ExtractedFields):
    """Uma linha da tabela `extractions`: campos extraídos mais a procedência."""

    posting_id: str
    content_hash: str
    model_id: str
    prompt_version: str
    schema_version: str
    extracted_at: datetime
