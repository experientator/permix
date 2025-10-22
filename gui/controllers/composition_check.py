from gui.views.composition_check import CompositionCheckView
from gui.models.composition_check import CompositionCheckModel
from gui.models.favorite_compositions import FavoriteCompositionsModel

class CompositionCheckController:
    def __init__(self, parent):
        self.comp_model = CompositionCheckModel()
        self.fav_model = FavoriteCompositionsModel()
        self.view = CompositionCheckView(parent, self)
        self.id = None
        self.notfav = None
        self.refresh_all()

    def refresh_all(self):
        compositions = self.comp_model.get_all_compositions()
        favorites = self.fav_model.get_all_favorites()

        self.view.display_compositions(compositions)
        self.view.display_favorites(favorites)
        self.view.display_details(None)

    def load_composition_details(self, composition_id):
        details = self.comp_model.get_composition_details(composition_id)
        self.view.display_details(details, is_favorite=False)

    def load_favorite_details(self, favorite_id):
        details = self.fav_model.get_favorite_details(favorite_id)
        self.view.display_details(details, is_favorite=True)

    def get_info_to_ucf(self):
        self.id = self.view.id_to_ucf
        self.notfav = self.view.not_fav_to_ucf

    def delete_selected(self, id_del, not_fav):
        if not_fav:
            self.comp_model.delete_selected(id_del)
        else:
            self.fav_model.delete_selected(id_del)

