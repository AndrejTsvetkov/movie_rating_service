from flask_admin.contrib.sqla import ModelView


class MovieView(ModelView):
    column_hide_backrefs = True
    can_edit = False

    form_create_rules = ['title', 'release_year']


class UserView(ModelView):
    can_create = False
    can_edit = False
    can_delete = False

    can_view_details = True
    column_list = ['id', 'login']
    column_details_list = ['login', 'reviews']


class ReviewView(ModelView):
    can_create = False
    can_edit = True
    can_delete = False

    form_edit_rules = ['review_text']
