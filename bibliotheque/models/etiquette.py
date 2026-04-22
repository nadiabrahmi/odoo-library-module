# -*- coding: utf-8 -*-

from odoo import models, fields, api
from random import randint


class Etiquette(models.Model):
    _name = 'bibliotheque.etiquette'
    _description = 'Etiquettes'
    _rec_name = 'name'
    _sql_constraints = [
        ('reference_unique',
         'unique (reference)',
         'Référence doit être unique'),
    ]

    # choisir un couleur aléatoirement
    def _default_color(self):
        return randint(1, 11)

    name = fields.Char('Etiquette', required=True)
    reference = fields.Char('Code', compute='get_reference')
    nb_livre = fields.Integer('Nombre de livres', compute='get_number_books')
    color = fields.Integer(
        string='Color Index', default=lambda self: self._default_color(),
        help='Tag color. No color means no display in kanban or front-end, to distinguish internal tags from public categorization tags.',
        store=True)

    livres_ids = fields.One2many(comodel_name='bibliotheque.livre', inverse_name='etiquette_id')

    # calculer nombre de livres
    def get_number_books(self):
        for rec in self:
            rec.nb_livre = len(rec.livres_ids)

    # insérer la réference automatiquement
    @api.depends('name')
    def get_reference(self):
        for rec in self:
            rec.reference = ""
            tab = str(rec.name).split()
            for i in tab:
                rec.reference = rec.reference + "" + str(i[0]).upper()

    # accéder aux les livres de chaque etiquette
    def open_livres(self):
        return {
            'name': 'Livres',
            'domain': [('etiquette_id', '=', self.id)],
            'view_type': 'form',
            'res_model': 'bibliotheque.livre',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'type': 'ir.actions.act_window',
        }
