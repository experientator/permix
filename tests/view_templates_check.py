import pytest
import tkinter as tk
from unittest.mock import Mock, MagicMock, patch
from src.views.templates_check import TemplatesCheckView, SiteFrame


class TestTemplatesCheckView:
    """Тесты для TemplatesCheckView"""

    @pytest.fixture
    def mock_controller(self):
        controller = Mock()
        controller.delete_selected = Mock()
        controller.handle_add_sites = Mock()
        controller.handle_submit_template = Mock()
        controller.load_template_details = Mock()
        return controller

    @pytest.fixture
    def mock_parent(self):
        return Mock(spec=tk.Tk)

    @pytest.fixture
    def templates_view(self, mock_parent, mock_controller):
        """Создает экземпляр TemplatesCheckView для тестирования"""
        with patch('src.views.templates_check.localization_manager'), \
                patch('src.views.templates_check.AppStyles'):
            view = TemplatesCheckView(mock_parent, mock_controller)
            return view

    def test_initialization(self, templates_view, mock_parent, mock_controller):
        """Тест инициализации окна"""
        assert templates_view.controller == mock_controller
        assert isinstance(templates_view.site_frames, list)
        assert templates_view.site_frames == []

    def test_build_ui_creates_widgets(self, templates_view):
        """Тест создания UI элементов"""
        assert hasattr(templates_view, 'temp_tree')
        assert hasattr(templates_view, 'sites_tree')
        assert hasattr(templates_view, 'entry_name')
        assert hasattr(templates_view, 'entry_dimensionality')
        assert hasattr(templates_view, 'entry_description')
        assert hasattr(templates_view, 'entry_anion_stoich')
        assert hasattr(templates_view, 'btn_add_sites')
        assert hasattr(templates_view, 'btn_submit')

    def test_bind_template_selection(self, templates_view):
        """Тест привязки callback к выбору шаблона"""
        callback = Mock()
        templates_view.bind_template_selection(callback)
        assert templates_view.temp_tree.bind('<<TreeviewSelect>>') is not None

    def test_show_template(self, templates_view):
        """Тест отображения шаблонов в treeview"""
        test_templates = [
            {
                'id': 1,
                'name': 'Test Template 1',
                'anion_stoichiometry': '2',
                'dimensionality': 3,
                'description': 'Test description 1'
            },
            {
                'id': 2,
                'name': 'Test Template 2',
                'anion_stoichiometry': '1',
                'dimensionality': 2,
                'description': 'Test description 2'
            }
        ]
        templates_view.show_template(test_templates)

        items = templates_view.temp_tree.get_children()
        assert len(items) == 2

        first_item_values = templates_view.temp_tree.item(items[0], 'values')
        assert first_item_values == (1, 'Test Template 1', '2', 3, 'Test description 1')

    def test_show_sites(self, templates_view):
        """Тест отображения сайтов в treeview"""

        test_sites = [
            {'type': 'A site', 'stoichiometry': '1', 'valence': '2'},
            {'type': 'B site', 'stoichiometry': '2', 'valence': '3'}
        ]
        templates_view.show_sites(test_sites)
        items = templates_view.sites_tree.get_children()
        assert len(items) == 2

        first_item_values = templates_view.sites_tree.item(items[0], 'values')
        assert first_item_values == ('A site', '1', '2')

    def test_get_selected_template_no_selection(self, templates_view):
        """Тест получения выбранного шаблона когда ничего не выбрано"""
        result = templates_view.get_selected_template()
        assert result is None

    def test_get_selected_template_with_selection(self, templates_view):
        """Тест получения выбранного шаблона"""
        templates_view.temp_tree.insert('', 'end', values=(1, 'Test', '2', 3, 'Desc'))  # 3 вместо '3D'

        items = templates_view.temp_tree.get_children()
        templates_view.temp_tree.selection_set(items[0])

        result = templates_view.get_selected_template()

        assert result == (1, 'Test', '2', 3, 'Desc')  # 3 вместо '3D'

    def test_on_add_sites(self, templates_view, mock_controller):
        """Тест добавления сайтов"""
        templates_view.entry_name.insert(0, 'Test Name')
        templates_view.entry_dimensionality.insert(0, '3')  # Числовая размерность
        templates_view.entry_description.insert(0, 'Test Description')
        templates_view.entry_anion_stoich.insert(0, '2')

        templates_view.site_vars['a_site'].set(1)
        templates_view.site_vars['b_site'].set(0)

        templates_view.on_add_sites()

        expected_data = {
            'name': 'Test Name',
            'dimensionality': '3',
            'description': 'Test Description',
            'anion_stoich': '2',
            'site_types': {
                'a_site': 1,
                'b_site': 0,
                'b_double': 0,
                'spacer': 0
            }
        }
        mock_controller.handle_add_sites.assert_called_once_with(expected_data)

    def test_on_submit_template(self, templates_view, mock_controller):
        """Тест отправки шаблона"""
        mock_frame = Mock(spec=SiteFrame)
        mock_frame.site_type = 'A Site'
        mock_frame.get_data.return_value = ('1', '2')

        templates_view.site_frames = [mock_frame]

        templates_view.on_submit_template()

        expected_data = [
            {
                'type': 'a_site',
                'stoichiometry': '1',
                'valence': '2'
            }
        ]
        mock_controller.handle_submit_template.assert_called_once_with(expected_data)

    def test_on_submit_template_no_data(self, templates_view, mock_controller):
        """Тест отправки шаблона когда нет данных"""
        mock_frame = Mock(spec=SiteFrame)
        mock_frame.site_type = 'A Site'
        mock_frame.get_data.return_value = None

        templates_view.site_frames = [mock_frame]

        templates_view.on_submit_template()
        mock_controller.handle_submit_template.assert_called_once_with([])

    def test_clear_form(self, templates_view):
        """Тест очистки формы"""

        templates_view.entry_name.insert(0, 'Test')
        templates_view.entry_dimensionality.insert(0, '3')
        templates_view.entry_description.insert(0, 'Desc')
        templates_view.entry_anion_stoich.insert(0, '2')

        templates_view.site_vars['a_site'].set(1)

        mock_widget = Mock()
        templates_view.sites_container.winfo_children = Mock(return_value=[mock_widget])

        templates_view.sites_tree.insert('', 'end', values=('A', '1', '2'))

        templates_view.clear_form()

        assert templates_view.entry_name.get() == ''
        assert templates_view.entry_dimensionality.get() == ''
        assert templates_view.entry_description.get() == ''
        assert templates_view.entry_anion_stoich.get() == ''

        for var in templates_view.site_vars.values():
            assert var.get() == 0

        assert templates_view.site_frames == []

        assert templates_view.btn_submit.cget('state') == 'disabled'

    def test_create_site_frames(self, templates_view):
        """Тест создания фреймов сайтов"""

        templates_view.site_vars['a_site'].set(1)
        templates_view.site_vars['b_site'].set(1)
        templates_view.site_vars['b_double'].set(0)
        templates_view.site_vars['spacer'].set(0)

        mock_container = Mock()
        templates_view.sites_container = mock_container
        mock_container.winfo_children.return_value = []

        with patch('src.templates_check_view.SiteFrame') as mock_site_frame:
            mock_frame1 = Mock()
            mock_frame2 = Mock()
            mock_site_frame.side_effect = [mock_frame1, mock_frame2]

            templates_view.create_site_frames()

            mock_container.winfo_children.assert_called_once()

            assert mock_site_frame.call_count == 2
            mock_site_frame.assert_any_call(mock_container, 'A Site')
            mock_site_frame.assert_any_call(mock_container, 'B Site')

            assert templates_view.site_frames == [mock_frame1, mock_frame2]

            templates_view.btn_submit.config.assert_called_with(state='normal')

    def test_create_site_frames_no_sites(self, templates_view):
        """Тест создания фреймов когда нет выбранных сайтов"""
        for var in templates_view.site_vars.values():
            var.set(0)

        mock_container = Mock()
        templates_view.sites_container = mock_container
        mock_container.winfo_children.return_value = []

        templates_view.create_site_frames()

        assert templates_view.site_frames == []

        templates_view.btn_submit.config.assert_called_with(state='disabled')


class TestSiteFrame:
    """Тесты для SiteFrame"""

    @pytest.fixture
    def mock_parent(self):
        """Создает mock родительского контейнера"""
        return Mock(spec=tk.Frame)

    @pytest.fixture
    def site_frame(self, mock_parent):
        """Создает экземпляр SiteFrame для тестирования"""
        with patch('src.templates_check_view.localization_manager'), \
                patch('src.templates_check_view.AppStyles'):
            frame = SiteFrame(mock_parent, 'A Site')
            return frame

    def test_initialization(self, site_frame, mock_parent):
        """Тест инициализации SiteFrame"""
        assert site_frame.site_type == 'A Site'
        assert hasattr(site_frame, 'entry_stoich')
        assert hasattr(site_frame, 'entry_valence')

    def test_get_data_with_valid_data(self, site_frame):
        """Тест получения данных с валидными значениями"""
        site_frame.entry_stoich.insert(0, '1')
        site_frame.entry_valence.insert(0, '2')

        result = site_frame.get_data()

        assert result == ('1', '2')

    def test_get_data_with_missing_stoich(self, site_frame):
        """Тест получения данных когда стехиометрия отсутствует"""
        site_frame.entry_valence.insert(0, '2')

        result = site_frame.get_data()

        assert result is None

    def test_get_data_with_missing_valence(self, site_frame):
        """Тест получения данных когда валентность отсутствует"""
        site_frame.entry_stoich.insert(0, '1')

        result = site_frame.get_data()

        assert result is None

    def test_get_data_with_both_empty(self, site_frame):
        """Тест получения данных когда оба поля пустые"""
        result = site_frame.get_data()

        assert result is None

    def test_get_data_with_numeric_values(self, site_frame):
        """Тест получения данных с числовыми значениями"""
        test_cases = [
            ('1', '2'),  # целые числа
            ('1.5', '2.5'),  # дробные числа
            ('0', '0'),  # нули
        ]

        for stoich, valence in test_cases:
            site_frame.entry_stoich.delete(0, tk.END)
            site_frame.entry_valence.delete(0, tk.END)

            site_frame.entry_stoich.insert(0, stoich)
            site_frame.entry_valence.insert(0, valence)

            result = site_frame.get_data()

            assert result == (stoich, valence)


class TestIntegration:
    """Интеграционные тесты с числовой размерностью"""

    def test_template_lifecycle(self, mock_parent, mock_controller):
        """Полный тест жизненного цикла шаблона с числовой размерностью"""
        with patch('src.templates_check_view.localization_manager'), \
                patch('src.templates_check_view.AppStyles'):
            view = TemplatesCheckView(mock_parent, mock_controller)

            templates = [
                {'id': 1, 'name': 'Template 1', 'anion_stoichiometry': '2', 'dimensionality': 3,
                 'description': 'Desc 1'},
                {'id': 2, 'name': 'Template 2', 'anion_stoichiometry': '1', 'dimensionality': 2,
                 'description': 'Desc 2'},
            ]
            view.show_template(templates)

            # Проверяем отображение
            items = view.temp_tree.get_children()
            assert len(items) == 2
            assert view.temp_tree.item(items[0], 'values') == (1, 'Template 1', '2', 3, 'Desc 1')

            view.temp_tree.selection_set(items[0])
            view.on_template_select(Mock())

            mock_controller.load_template_details.assert_called_once_with(1)

            view.clear_form()
            assert view.entry_name.get() == ''
            assert view.entry_dimensionality.get() == ''

