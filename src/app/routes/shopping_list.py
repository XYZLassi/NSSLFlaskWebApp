import flask
import flask_login
from nssl import NSSL

from ..injector import nssl_inject

bp = flask.Blueprint("ShoppingList", __name__, url_prefix='/shoppingList')


@bp.route('/', methods=['GET', 'POST'])
@flask_login.login_required
@nssl_inject
def index(nssl: NSSL):
    from ..forms.shopping_list import NewShoppingListForm
    force = flask.request.args.get('refresh', False) == '1'

    form = NewShoppingListForm()
    if form.validate_on_submit():
        result = nssl.add_list(form.name.data)
        if not result.success:
            flask.flash(result.error)
        return flask.redirect(flask.url_for('ShoppingList.index', refresh=1))

    response = nssl.get_shopping_lists(force=force)
    if not response.success:
        flask.flash(response.error)
    lists = response.data.lists

    return flask.render_template('shopping_list/index.html',
                                 title='Shopping Lists',
                                 form=form,
                                 shopping_lists=lists)


@bp.route('/<int:item_id>', methods=['GET', 'POST'])
@flask_login.login_required
@nssl_inject
def show(nssl: NSSL, item_id: int):
    from ..forms.shopping_list import AddProductForm
    response = nssl.get_list(item_id)
    if not response.success:
        flask.flash(response.error)

    shopping_list = response.data

    if shopping_list is None:
        return flask.redirect(flask.url_for('ShoppingList.index'))

    form = AddProductForm()
    if form.validate_on_submit():
        response = nssl.add_product_to_list(item_id,
                                            form.name.data, form.amount.data,
                                            gtin=form.gtin.data)

        if not response.success:
            flask.flash(response.error)

        return flask.redirect(
            flask.url_for('ShoppingList.show', item_id=shopping_list.id))

    return flask.render_template('shopping_list/show.html',
                                 form=form,
                                 shopping_list=shopping_list)


@bp.route('/edit/<int:item_id>', methods=['GET', 'POST'])
@nssl_inject
def edit(nssl: NSSL, item_id: int):
    from ..forms.shopping_list import EditShoppingListForm

    response = nssl.get_list(item_id)
    if not response.success:
        flask.flash(response.error)
        return flask.redirect(flask.url_for('ShoppingList.index'))

    shopping_list = response.data
    form = EditShoppingListForm()
    if form.validate_on_submit():
        response = nssl.rename_list(item_id, form.name.data)

        if not response.success:
            flask.flash(response.error)
        else:
            shopping_list = response.data

    form.name.data = shopping_list.name

    return flask.render_template('shopping_list/edit.html',
                                 form=form,
                                 shopping_list=shopping_list)


@bp.route('/delete/<int:item_id>')
@nssl_inject
def delete(nssl: NSSL, item_id: int):
    response = nssl.delete_list(item_id)
    if not response.success:
        flask.flash(response.error)

    return flask.redirect(flask.url_for('ShoppingList.index', refresh=1))
