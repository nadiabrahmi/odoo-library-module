import base64
import datetime
import json
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models
from odoo import exceptions
import requests


class ResPartnerInherit(models.Model):
    _inherit = "res.partner"

    birthdate_date = fields.Date("Date d'anniversaire")
    age = fields.Integer(string="Age", readonly=True, compute="_compute_age")
    birthday = fields.Date('Jour d\'anniversaire', compute='get_birthday')
    profession = fields.Selection(
        [('Directeur', 'Directeur'), ('Enseignant', 'Enseignant'), ('Secrétaire', 'Secrétaire'),
         ('Etudiant', 'Etudiant'), ('Stagiaire', 'Stagiaire'), ('Autres', 'Autres')])
    # first_name = fields.Char('Prénom')
    eleve_id = fields.Integer('id')
    matricule = fields.Integer('Matricule',
                               default=lambda self: self.env['ir.sequence'].next_by_code('increment_your_field'))
    classe = fields.Selection([('P1A', 'P1A'), ('P1B', 'P1B'),
                               ('P1C', 'P1C'), ('P1E', 'P1E'), ('P2A', 'P2A'), ('P2B', 'P2B'),
                               ('P2D', 'P2D'), ('P2E', 'P2E'), ('P3A', 'P3A'), ('P3B', 'P3B'),
                               ('P3F', 'P3F'), ('P4A', 'P4A'), ('P4B', 'P4B'), ('soleil', 'Soleil')])

    web_url = fields.Char(string='Image URL', help='Automatically sanitized HTML contents', copy=False, store=True)

    @api.onchange('web_url')
    def set_image(self):
        for record in self:
            link = record.web_url
            if link:
                try:
                    response = requests.get(link.strip(), timeout=2)
                    if response.ok:
                        record.update({
                            'image_1920': base64.b64encode(response.content).replace(b'\n', b''),
                        })
                except:
                    raise Warning("Please provide correct URL or check your image size.!")

    @api.depends("birthdate_date")
    def _compute_age(self):
        for record in self:
            age = 0
            if record.birthdate_date:
                age = relativedelta(fields.Date.today(), record.birthdate_date).years
            record.age = age

    def get_birthday(self):
        for reco in self:
            today = datetime.date.today()
            reco.birthday = reco.birthdate_date
            if reco.birthdate_date:
                reco.birthday = reco.birthday.replace(year=today.year)

    def open_calendar(self):
        return {
            'name': 'Calendrier des anniversaires',
            'res_model': 'res.partner',
            'view_id': False,
            'view_mode': 'calendar',
            'type': 'ir.actions.act_window',
        }

    def open_livres(self):
        return {
            'name': 'Livres',
            'res_model': 'bibliotheque.livre',
            'view_id': False,
            'view_mode': 'tree',
            'type': 'ir.actions.act_window',
        }

    # @api.model_create_multi
    # def create(self, vals):
    #     for val in vals:
    #         if val.get('partner_id') and val.get('name') and val.get('birth_date') and val.get('age'):
    #             obj_id = self.env["res.partner"].browse(vals.get('partner_id')).uom_id.id
    #             val['partner_id'] = obj_id,
    #             val['name'] = obj_id.name,
    #             val['birth_date'] = obj_id.birthday,
    #             val['age'] = obj_id.age
    #     return self.env['birth.event'].create(vals)

    def get_customer(self):
        url = "http://elcab.it-school.be/api/customer?school_id=7"
        access_token = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpYXQiOjE2ODU2NDU4MzgsImV4cCI6MTcwMTQxMzgzOCwicm9sZXMiOlsiUk9MRV9VU0VSIl0sInVzZXJuYW1lIjoiZGV2aWNlLWJpcnRoZGF5IiwidXNlcl9pZCI6NTQ5NSwiZXhwaXJlc19pbiI6IjM2MDAwIn0.c2bGlgBtOvwExltNpnMERwepZS63oGK6PYhuvspT-742wEgkQ_yMbfxUsTGe87P6nf_1sMJcR9ZiMzS0VCphPBehFB2lGFR-Egh9TOtE6a6cKlf-NIF-ZeBp8dWZ59hrJjS8aQrhfHfRRxnIpF4qjTqBVi3TkpmvP4dooxGtdNjqPq_SnR0exFhITMISpEIzjvyu28Sa2s-hBaQuyQ2hTYQ_K7OYwNZUhKnc1xnbkPADeiAb5hOCP4xSyQfNY5iWJgl5kt7NVr6s8YiVVwPKFxYzBh0PtVXNUo2BFGiuicDWCH498-bpjJLT8L3N62ci3m02-C63Adf5SP2bLZaZSw'
        headers = {'Content-type': 'application/json', 'Authorization': 'Bearer %s' % access_token}
        try:
            response = requests.request("GET", url, json=None, headers=headers, timeout=60)
            response.raise_for_status()
        except requests.exceptions.RequestException:
            # _logger.exception("unable to communicate with Mollie: %s", url)
            raise exceptions.ValidationError("Mollie: " + "Could not establish the connection to the API.")
        return response.json().get('data')

        # for data in datas:
        #     self.env['res.partner'].sudo().create(
        #             {'name': str(data.get('data', {'name'})), 'type': 'contact', 'first_name': str(data.get('data', {'firstname'})),
        #                 'birthdate_date': data.get('data', {'birth_date'}), 'eleve_id': data.get('data', {'customer_id'}),
        #                 'company_name': str(data.get('data', {'school'})), 'matricule': data.get('data', {'matricule'})})

    def extract_data(self):
        self.env['res.partner'].sudo().create(
            {'name': 'test test', 'function': 'Etudiant', 'company_type': 'person',
             'birthdate_date': datetime.datetime.strptime('25-11-2023', '%d-%m-%Y').date(),
             'eleve_id': 1000, 'matricule': 3333, 'classe': 'P2D',
             'web_url': 'https://elcab.it-school.be/media/cache/customer_picture_preview/customer/pictures/files/622b58e69a6c6171477031.jpg'})

        # datas = self.get_customer()
        # for data in datas:
        #     self.env['res.partner'].sudo().create(
        #         {'name': str(data.get('name') + " " + data.get('firstname')),
        #          'birthdate_date': datetime.datetime.strptime(str(data.get('birth_date')), '%d-%m-%Y').date(),
        #          'eleve_id': data.get('customer_id'), 'classe': data.get('"school_class": '),
        #          'company_name': str(data.get('school')), 'matricule': data.get('matricule'), 'web_url': str(data.get('photo_url'))})
