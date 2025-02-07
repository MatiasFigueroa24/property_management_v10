# -*- coding: utf-8 -*-
{
    "name": "Factura Electrónica Argentina",
    'version': '10.0',
    'category': 'Localization/Argentina',
    'sequence': 14,
    'author': 'ADHOC SA, Moldeo Interactive,Odoo Community Association (OCA)',
    'license': 'AGPL-3',
    'summary': '',
    'depends': [
        'l10n_ar_afipws',
        # 'l10n_ar_account',
        # TODO improove this, we add this dependency because of demo data only
        # becuase demo data needs de chart account installed, we should
        # take this data tu l10n_ar_chart and set electronic if available
        # we try adding this demo data on l10n_ar_chart but if done, we should
        # add dependency to this module and also duplicate invoice data so
        # it does not use same id
        'l10n_ar_chart',
    ],
    'external_dependencies': {
    },
    'data': [
        'wizard/afip_ws_consult_wizard_view.xml',
        'wizard/afip_ws_currency_rate_wizard_view.xml',
        'views/invoice_view.xml',
        'views/account_journal_document_type_view.xml',
        'views/wsfe_error_view.xml',
        'views/account_journal_view.xml',
        'views/product_uom_view.xml',
        'views/res_currency_view.xml',
        'views/menuitem.xml',
        'res_config_view.xml',
        'views/res_company_view.xml',
        'data/afip.wsfe_error.csv',
        'security/ir.model.access.csv',
    ],
    'demo': [
        'demo/account_journal_expo_demo.yml',
        '../l10n_ar_account/demo/account_customer_expo_invoice_demo.yml',
        'demo/account_journal_demo.yml',
        '../l10n_ar_account/demo/account_customer_invoice_demo.yml',
        'demo/account_journal_demo_without_doc.yml',
    ],
    'test': [
    ],
    'images': [
    ],
    'installable': False,
    'auto_install': False,
    'application': False,
}
