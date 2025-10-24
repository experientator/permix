from src.models.templates_check import TemplatesCheckModel
from src.views.templates_check import TemplatesCheckView
from src.language.manager import localization_manager
from src.utils.calculation_tests import show_error, show_warning, show_success, ask_confirmation

class TemplatesCheckController:
    def __init__(self, parent):
        self.model = TemplatesCheckModel()
        self.view = TemplatesCheckView(parent, self)
        localization_manager.register_observer(self)

        self.load_templates()
        self.view.bind_template_selection(self.on_template_selected)
        self.load_templates()
        self.current_template_id = None

    def handle_add_sites(self, data):
        if not all([data['name'], data['dimensionality'], data['anion_stoich']]):
            show_error(localization_manager.tr("temp_err1"))
            return None

        try:
            dimensionality = int(data['dimensionality'])
            anion_stoich = int(data['anion_stoich'])
        except ValueError:
            show_error(localization_manager.tr("temp_err2"))
            return None

        template_id, message = self.model.add_template(
            data['name'],
            data['description'],
            anion_stoich,
            dimensionality
        )

        if not template_id:
            show_error(message)
            return None

        self.current_template_id = template_id
        self.view.create_site_frames()

    def handle_submit_template(self, site_data):
        if not self.current_template_id:
            show_error(localization_manager.tr("temp_err3"))
            return None

        for site in site_data:
            try:
                stoichiometry = int(site['stoichiometry'])
                valence = int(site['valence'])
            except ValueError:
                show_error(localization_manager.tr("temp_err4"))
                return None

        for site in site_data:
            success, message = self.model.add_site(
                self.current_template_id,
                int(site['stoichiometry']),
                site['type'],
                site['valence']
            )

            if not success:
                show_error(message)
                return None

        show_success(localization_manager.tr("temp_success"))
        self.load_templates()
        self.view.btn_add_sites.config(state='normal')
        self.current_template_id = None

    def load_templates(self):
        try:
            template = self.model.get_all_templates()
            self.view.show_template(template)
        except Exception as e:
            er = localization_manager.tr("temp_err5")
            show_error( f"{er} {str(e)}")

    def on_template_selected(self, event=None):
        template = self.view.get_selected_template()
        if not template:
            return

        id_phase, name, anion_stoichiometry, dimensionality, description = template
        try:
            site = self.model.get_sites_for_template(id_phase)
            self.view.show_sites(site)
        except Exception as e:
            er = localization_manager.tr("temp_err6")
            show_error(f"{er} {str(e)}")

    def delete_selected(self):
        item_data = self.view.get_selected_template()
        if not item_data:
            show_warning(localization_manager.tr("ion_war"))
            return

        record_id = item_data[0]

        if ask_confirmation(localization_manager.tr("ion_conf")):
            try:
                success = self.model.delete_template(record_id)
                if success:
                    show_success(localization_manager.tr("ion_success"))
                    self.load_templates()
                else:
                    show_error(localization_manager.tr("ion_err7"))
            except Exception as e:
                er = localization_manager.tr("ion_err8")
                show_error(f"{er} {str(e)}")

    def __del__(self):
        self.model.close()