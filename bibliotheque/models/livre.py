# -*- coding: utf-8 -*-
from datetime import datetime

from odoo import models, fields, api, exceptions, tools

try:
    import qrcode
except ImportError:
    qrcode = None
try:
    import base64
except ImportError:
    base64 = None
from io import BytesIO


class Livre(models.Model):
    _name = 'bibliotheque.livre'
    _description = 'Livres de la bibliothèque'
    _sql_constraints = [
        ('Code_etiquette_unique',
         'unique(Code, etiquette_id)',
         'Référence doit etre unique'),
    ]
    _inherit = 'mail.thread'
    _rec_name = 'titre'

    @api.model
    def year_selection(self):
        year = 2000  # start year
        year_list = []
        while year != 2023:  # end year
            year_list.append((str(year), str(year)))
            year += 1
        return year_list

    # def _get_default_image(self):
    #     image_path = get_resource_path('bibliotheque', 'static/src/img', 'default_image.png')
    #     with tools.file_open(image_path, 'rb') as f:
    #         return base64.b64encode(f.read())

    # photo = fields.Binary("Image par défaut", attachment=True, store=True, default=_get_default_image)
    titre = fields.Char('Titre')
    etiquette_id = fields.Many2one(comodel_name='bibliotheque.etiquette', required=True)
    eti_ref = fields.Char(related='etiquette_id.reference')
    color = fields.Integer(related='etiquette_id.color')
    Code = fields.Integer('Numéro', required=True)
    reference = fields.Char('Référence', compute='get_reference_book')
    quantite = fields.Integer('Exemplaires', default=1)
    quantite_dispo = fields.Integer('Quantité disponible', compute='get_number_book_dispo')
    description = fields.Text('Description')
    edition = fields.Char('Edition')
    emprunteurs_ids = fields.One2many(comodel_name='bibliotheque.emprunte', inverse_name='livre_id')
    somme_livres_adhere = fields.Integer(compute='get_number_book_adh')
    qr_code = fields.Binary("QR Code", compute='get_qr_code', attachment=True)
    url_qr_code = fields.Char(compute="get_qr_code")

    def generate_qr(self, txt=''):
        qr_code = qrcode.QRCode(version=4, box_size=4, border=1)
        qr_code.add_data(txt)
        qr_code.make(fit=True)
        qr_img = qr_code.make_image()
        im = qr_img._img.convert("RGB")
        buffered = BytesIO()
        im.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue()).decode('ascii')
        return img_str

    @api.model
    def get_qr_code(self):
        for rec in self:
            base_url = rec.env['ir.config_parameter'].get_param('web.base.url')
            if not 'localhost' in base_url:
                if 'http://' in base_url:
                    base_url = base_url.replace('http://', 'https://')
            base_url = base_url + '/web#id=' + str(rec.id) + '&model=bibliotheque.livre&view_type=form&cids='
            base64_qr = rec.env['bibliotheque.livre'].generate_qr(base_url)
            rec.qr_code = base64_qr
            rec.url_qr_code = base_url

    # calculer nombre de livres disponibless
    @api.depends('quantite', 'emprunteurs_ids', 'somme_livres_adhere')
    def get_number_book_dispo(self):
        for rec in self:
            rec.quantite_dispo = rec.quantite - len(rec.emprunteurs_ids) + rec.somme_livres_adhere

    # calculer nombre de livres retourné
    def get_number_book_adh(self):
        som = 0
        for record in self:
            for rec in record.emprunteurs_ids:
                if rec.is_adhere:
                    som = som + 1
            record.somme_livres_adhere = som

    # ajouter référence
    def get_reference_book(self):
        for liv in self:
            ref = liv.eti_ref + '' + str(liv.Code)
            liv.reference = ref

    # @api.constrains('Code')
    # def check_reference(self):
    #     livres = self.env['bibliotheque.livre']
    #     for rec in self:
    #         for livre in livres:
    #             if rec.Code in

    @api.constrains('emprunteurs_ids')
    def check_emprunte(self):
        if self.quantite_dispo < 0:
            raise exceptions.ValidationError('quantité épuisé !!')

    def emprunter(self):
        self.ensure_one()
        ctx = {
            'default_model': 'bibliotheque.emprunte',
            'default_livre_id': self.id,
            'default_etiquete': self.etiquette_id,
            'default_composition_model': 'comment',
        }
        return {
            'type': 'ir.actions.act_window',
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'bibliotheque.emprunte',
            'target': 'new',
            'context': ctx,
        }
