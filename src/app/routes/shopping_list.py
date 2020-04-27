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


@bp.route('/<int:list_id>/changeAmount/<int:item_id>/<int:amount>',
          methods=['GET'])
@nssl_inject
def change_amount(nssl: NSSL, list_id: int, item_id: int, amount: int):
    if amount <= 0:
        flask.flash('Value must be greater than 0')
        return flask.redirect(flask.url_for('ShoppingList.show', item_id=list_id))

    list_response = nssl.get_list(list_id)
    if not list_response.success:
        flask.flash(list_response.error)
        return flask.redirect(flask.url_for('ShoppingList.index'))

    response = nssl.change_list_product(list_id, item_id, new_amount=amount)
    if not response.success:
        flask.flash(response.error)

    return flask.redirect(flask.url_for('ShoppingList.show', item_id=list_id))


@bp.route('/delete/<int:item_id>')
@nssl_inject
def delete(nssl: NSSL, item_id: int):
    response = nssl.delete_list(item_id)
    if not response.success:
        flask.flash(response.error)

    return flask.redirect(flask.url_for('ShoppingList.index', refresh=1))


@bp.route('/<int:list_id>/delete/<int:item_id>')
@nssl_inject
def delete_product(nssl: NSSL, list_id: int, item_id: int):
    response = nssl.delete_product_from_list(list_id, item_id)
    if not response.success:
        flask.flash(response.error)

    return flask.redirect(flask.url_for('ShoppingList.show', item_id=list_id))


@bp.route('/<int:list_id>/changeAmount/<int:item_id>/edit',
          methods=['GET', 'POST'])
@nssl_inject
def edit_product(nssl: NSSL, list_id: int, item_id: int):
    from ..forms.shopping_list import EditProductForm

    list_response = nssl.get_list(list_id)
    if not list_response.success:
        flask.flash(list_response.error)
        return flask.redirect(flask.url_for('ShoppingList.index'))
    shopping_List = list_response.data

    item = shopping_List.get_product(item_id)
    if item is None:
        flask.flash('No item found')
        return flask.redirect(flask.url_for('ShoppingList.show', item_id=list_id))

    form = EditProductForm()
    if form.validate_on_submit():
        response = nssl.change_list_product(list_id, item_id,
                                            new_amount=form.amount.data,
                                            new_name=form.name.data)
        if not response.success:
            flask.flash(response.error)
        else:
            return flask.redirect(flask.url_for('ShoppingList.show', item_id=list_id))

    if flask.request.method == 'GET':
        form.name.data = item.name
        form.amount.data = item.amount

    return flask.render_template('shopping_list/product.edit.html',
                                 shopping_list=shopping_List,
                                 product=item,
                                 form=form)
