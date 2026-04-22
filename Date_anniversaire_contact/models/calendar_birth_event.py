from odoo import models, fields, api, exceptions

import base64
import requests


class AnnivCalendar(models.Model):
    _name = 'birth.event'

    partner_id = fields.Many2one(comodel_name='res.partner')
    birth_date = fields.Date(related='partner_id.birthday')
    name = fields.Char(related='partner_id.name')
    age = fields.Integer(related='partner_id.age')
    web_url = fields.Char(related='partner_id.web_url')
    image = fields.Binary(string='Image', compute='_compute_image', store=True, attachment=False)

    def load_image_from_url(self, url):
        data = base64.b64encode(requests.get(url.strip()).content).replace(b'\n', b'')
        return data

    @api.depends('web_url')
    def _compute_image(self):
        for record in self:
            image = None
            if record.web_url:
                image = self.load_image_from_url(record.web_url)
                record.update({'image': image, })
