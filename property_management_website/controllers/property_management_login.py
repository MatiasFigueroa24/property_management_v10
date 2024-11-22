# -*- coding: utf-8 -*-
import werkzeug
import logging
import werkzeug.utils
from odoo.http import request
import odoo.addons.website_sale.controllers.main
from odoo import http, SUPERUSER_ID
from odoo.tools.translate import _
from odoo.http import request, serialize_exception as _serialize_exception

db_list = http.db_list
db_monodb = http.db_monodb
from odoo.addons.web.controllers.main import abort_and_redirect, ensure_db
from odoo.addons.auth_signup.models.res_users import SignupError

_logger = logging.getLogger(__name__)


def db_info():
    version_info = odoo.service.common.exp_version()
    return {
        'server_version': version_info.get('server_version'),
        'server_version_info': version_info.get('server_version_info'),
    }


class PropertyManagementLogin(odoo.addons.web.controllers.main.Home):
    @http.route()
    def web_login(self, redirect=None, *args, **kw):
        cr, uid, context, pool = request.cr, request.uid, request.context, request.registry
        ensure_db()
        response = super(PropertyManagementLogin, self).web_login(*args, **kw)
        response.qcontext.update(self.get_auth_signup_config())
        if request.httprequest.method == 'GET' and request.session.uid and request.params.get('redirect'):
            # Redirect if already logged in and redirect param is present
            return http.redirect_with_hash(request.params.get('redirect'))

        if not request.uid:
            request.uid = odoo.sudo()

        values = request.params.copy()
        if not redirect:
            redirect = '/web?' + request.httprequest.query_string
        values['redirect'] = redirect

        try:
            values['databases'] = http.db_list()
        except odoo.exceptions.AccessDenied:
            values['databases'] = None

        if request.httprequest.method == 'POST':
            old_uid = request.uid
            uid = request.session.authenticate(request.session.db, request.params[
                'login'], request.params['password'])

            if uid is not False:
                # code for add from cookie property ids
                product_ids_from_cookies = request.httprequest.cookies.get(
                    'property_id')
                product_ids_from_cookies_str = str(product_ids_from_cookies)
                product_ids_from_cookies_list = product_ids_from_cookies_str.split(
                    ',')

                account_asset_cookie_ids = []
                if product_ids_from_cookies_list[0] == 'None':
                    account_asset_cookie_ids = []
                else:
                    for one_prod_cookie_id in product_ids_from_cookies_list:
                        if not one_prod_cookie_id:
                            continue
                        one_cookie_int_id = int(one_prod_cookie_id)
                        account_asset_cookie_ids.append(one_cookie_int_id)
                user_obj = request.env['res.users']
                partner_obj = request.env['res.partner']
                user = user_obj.browse(int(uid))
                account_asset_frvorite_property_ids = []
                for partner in user:
                    partner_id = partner.partner_id.id
                    partner_one_obj = partner_obj.browse(int(partner_id))
                    for one_asset_id in partner_one_obj.fav_assets_ids:
                        account_asset_frvorite_property_ids.append(
                            one_asset_id.id)

                properties_for_save = [
                    x for x in account_asset_cookie_ids if x not in account_asset_frvorite_property_ids]
                if properties_for_save:
                    for one_property_save in properties_for_save:
                        selected_property = partner_id.write(
                            {'fav_assets_ids': [(4, int(one_property_save))]})

                        # code for redicet homepage when
                backend_users_ids = request.env.ref(
                    'property_management_website.group_property_website_backend').sudo().users.ids
                # if uid not in backend_users_ids:
                #     redirect = '/page/homepage' + request.httprequest.query_string
                #     values['redirect'] = redirect

                # if uid == SUPERUSER_ID:
                #     redirect = '/web' + request.httprequest.query_string
                #     values['redirect'] = redirect

                if uid not in backend_users_ids:
                    if uid == SUPERUSER_ID:
                        pass
                    else:
                        return http.local_redirect('/page/homepage')

                return http.redirect_with_hash(redirect)
            request.uid = old_uid
            values['error'] = "Wrong login/password"

        if request.env.ref('web.login', False):
            return request.render('web.login', values)
        else:
            # probably not an odoo compatible database
            error = 'Unable to login on database %s' % request.session.db
            return werkzeug.utils.redirect('/web/database/selector?error=%s' % error, 303)
        return response

    @http.route()
    def web_auth_signup(self, *args, **kw):
        qcontext = self.get_auth_signup_qcontext()

        if not qcontext.get('token') and not qcontext.get('signup_enabled'):
            raise werkzeug.exceptions.NotFound()

        if 'error' not in qcontext and request.httprequest.method == 'POST':
            try:
                self.do_signup(qcontext)
                return super(PropertyManagementLogin, self).web_login(*args, **kw)
            except (SignupError, AssertionError), e:
                if request.env["res.users"].sudo().search([("login", "=", qcontext.get("login"))]):
                    qcontext["error1"] = _(
                        "Another user is already registered using this email address.")
                else:
                    _logger.error(e.message)
                    qcontext['error1'] = _("Could not create a new account.")
        if qcontext['login']:
            qcontext['login1'] = qcontext.pop('login')
        return http.local_redirect('/web/login', qcontext)
