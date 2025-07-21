class CompositionInformation(object):
    def __init__(self, doi, type, notes):
        self.doi = doi
        self.type = type
        self.notes = notes

class CompositionStructure(object):
    instances = []
    def __init__(self, site, symbol, fraction, valence):
        self.site = site
        self.symbol = symbol
        self.fraction = fraction
        self.valence = valence
        self.__class__.instances.append(self)

    @property
    def valence(self):
        return self._valence

    @valence.setter
    def valence(self, value):
        if not isinstance(value, int):
            raise ValueError("Валентность должна быть целым числом")
        self._valence = value

    @property
    def fraction(self):
        return self._fraction

    @fraction.setter
    def fraction(self, value):
        self._fraction = value
        self._check_fraction_sum("A_site")
        self._check_fraction_sum("B_site")
        self._check_fraction_sum("B_double_site")
        self._check_fraction_sum("Anion")

    def _check_fraction_sum(self, check_parameter):
        instances = [obj for obj in self.__class__.instances if obj.site == "check_parameter"]
        total_fraction = sum(obj.fraction for obj in instances)

        if not (0.999 <= total_fraction <= 1.001):
            raise ValueError(
                f"Сумма fraction для элементов одного типа должна быть равна 1"
            )

    def __del__(self):
        if self in self.__class__.instances:
            self.__class__.instances.remove(self)

class Solvents(object):
    instances = []
    def __init__(self, type, symbol, fraction):
        self.type = type
        self.symbol = symbol
        self.fraction = fraction
        self.__class__.instances.append(self)

    @property
    def fraction(self):
        return self._fraction

    @fraction.setter
    def fraction(self, value):
        self._fraction = value
        self._check_fraction_sum("Solvent")
        self._check_fraction_sum("Antisolvent")

    def _check_fraction_sum(self, check_parameter):
        instances = [obj for obj in self.__class__.instances if obj.site == "check_parameter"]
        total_fraction = sum(obj.fraction for obj in instances)

        if not (0.999 <= total_fraction <= 1.001):
            raise ValueError(
                f"Сумма fraction для растворителей (антирастворителей) должна быть равна 1"
            )

    def __del__(self):
        if self in self.__class__.instances:
            self.__class__.instances.remove(self)

class Properties(object):
    def __init__(self, v_antisolvent, band_gap, pce_percent, voc, jsc, ff_percent, stability_notes):
        self.v_antisolvent = v_antisolvent
        self.band_gap = band_gap
        self.pce_percent = pce_percent
        self.voc = voc
        self.jsc = jsc
        self.ff_percent = ff_percent
        self.stability_notes = stability_notes