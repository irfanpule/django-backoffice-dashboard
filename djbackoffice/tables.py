import django_tables2 as tables


class SimpleTable(tables.Table):
    """
    Class to add action each of row
    """
    actions = tables.TemplateColumn(
        template_name="djbackoffice/partials/action_row_table.html"
    )

    class Meta:
        show_header = True
