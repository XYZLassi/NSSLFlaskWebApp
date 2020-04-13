import flask

bp = flask.Blueprint('filter', __name__)


@bp.add_app_template_filter
def df(date, fmt=None):
    if fmt:
        return date.strftime(fmt)
    else:
        return date.strftime('%d.%m.%y %H:%M:%S')
