import django_tables2 as tables


class SimpleTable(tables.Table):
    """
    Class to add action each of row
    """
    actions = tables.TemplateColumn(
        template_name="djlakang/partials/action_row_table.html"
    )
