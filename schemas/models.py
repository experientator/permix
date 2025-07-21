from typing import List, Optional
from sqlmodel import SQLModel, Field, Relationship

#models from known_compositions.db (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)
class PerovskiteBase(SQLModel):
    id: str = Field(primary_key=True)
    display_composition: str
    doi: Optional[str] = None
    type: str = Field(..., regex="^(experimental|theoretical|simulated)$")
    notes: Optional[str] = None
    template_key: Optional[str] = None


class Perovskite(PerovskiteBase, table=True):
    __tablename__ = "perovskites"

    # Свойства материала
    band_gap_eV: Optional[float] = None
    pce_percent: Optional[float] = None
    voc_V: Optional[float] = None
    jsc_mA_cm2: Optional[float] = None
    ff_percent: Optional[float] = None
    stability_notes: Optional[str] = None

    # Отношения
    a_site_components: List["ASiteComponent"] = Relationship(back_populates="perovskite")
    b_site_components: List["BSiteComponent"] = Relationship(back_populates="perovskite")
    anion_mix: List["Anion"] = Relationship(back_populates="perovskite")
    synthesis: Optional["Synthesis"] = Relationship(back_populates="perovskite")
    properties: Optional["Properties"] = Relationship(back_populates="perovskite")


class ASiteComponent(SQLModel, table=True):
    __tablename__ = "a_site_components"

    id: Optional[int] = Field(default=None, primary_key=True)
    perovskite_id: str = Field(foreign_key="perovskites.id")
    symbol: str
    fraction_on_site: float
    valence: int

    perovskite: Perovskite = Relationship(back_populates="a_site_components")


class BSiteComponent(SQLModel, table=True):
    __tablename__ = "b_site_components"

    id: Optional[int] = Field(default=None, primary_key=True)
    perovskite_id: str = Field(foreign_key="perovskites.id")
    symbol: str
    fraction_on_site: float
    valence: int

    perovskite: Perovskite = Relationship(back_populates="b_site_components")


class Anion(SQLModel, table=True):
    __tablename__ = "anions"

    id: Optional[int] = Field(default=None, primary_key=True)
    perovskite_id: str = Field(foreign_key="perovskites.id")
    symbol: str
    fraction: float
    total_anion_stoichiometry: Optional[float] = None

    perovskite: Perovskite = Relationship(back_populates="anion_mix")


class Synthesis(SQLModel, table=True):
    __tablename__ = "synthesis"

    id: Optional[int] = Field(default=None, primary_key=True)
    perovskite_id: str = Field(foreign_key="perovskites.id")
    c_solution_molar: Optional[float] = None
    v_solution_ml: Optional[float] = None
    v_antisolvent_ml: Optional[float] = None
    method_description: Optional[str] = None

    perovskite: Perovskite = Relationship(back_populates="synthesis")
    solvents: List["Solvent"] = Relationship(back_populates="synthesis")
    antisolvents: List["Antisolvent"] = Relationship(back_populates="synthesis")
    k_factors: List["KFactor"] = Relationship(back_populates="synthesis")


class Solvent(SQLModel, table=True):
    __tablename__ = "solvents"

    id: Optional[int] = Field(default=None, primary_key=True)
    synthesis_id: int = Field(foreign_key="synthesis.id")
    symbol: str
    fraction: float

    synthesis: Synthesis = Relationship(back_populates="solvents")


class Antisolvent(SQLModel, table=True):
    __tablename__ = "antisolvents"

    id: Optional[int] = Field(default=None, primary_key=True)
    synthesis_id: int = Field(foreign_key="synthesis.id")
    symbol: str
    fraction: float

    synthesis: Synthesis = Relationship(back_populates="antisolvents")


class KFactor(SQLModel, table=True):
    __tablename__ = "k_factors"

    id: Optional[int] = Field(default=None, primary_key=True)
    synthesis_id: int = Field(foreign_key="synthesis.id")
    compound: str
    factor: float

    synthesis: Synthesis = Relationship(back_populates="k_factors")


class Properties(SQLModel, table=True):
    __tablename__ = "properties"

    id: Optional[int] = Field(default=None, primary_key=True)
    perovskite_id: str = Field(foreign_key="perovskites.id")
    band_gap_eV: Optional[float] = None
    pce_percent: Optional[float] = None
    voc_V: Optional[float] = None
    jsc_mA_cm2: Optional[float] = None
    ff_percent: Optional[float] = None
    stability_notes: Optional[str] = None

    perovskite: Perovskite = Relationship(back_populates="properties")


def create_db_and_tables(engine):
    SQLModel.metadata.create_all(engine)